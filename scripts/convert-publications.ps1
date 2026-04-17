$oldDir = "C:\Users\rt3105\Documents\GitHub\starter-academic\content\en\publication"
$newDir = "C:\Users\rt3105\Documents\GitHub\prime-fox\content\en\publications"

$dirs = Get-ChildItem $oldDir -Directory | Where-Object { $_.Name -ne '_index.md' }

foreach ($d in $dirs) {
    $src = Join-Path $d.FullName "index.md"
    if (!(Test-Path $src)) { continue }
    
    $raw = Get-Content $src -Raw -Encoding UTF8
    
    # Split frontmatter and body
    if ($raw -match '(?s)^---\r?\n(.*?)\r?\n---\r?\n?(.*)$') {
        $fm = $Matches[1]
        $body = $Matches[2].Trim()
    } else {
        Write-Host "SKIP: $($d.Name) - no frontmatter"
        continue
    }

    # Extract fields
    $title = if ($fm -match '(?m)^title:\s*"(.*?)"') { $Matches[1] } 
             elseif ($fm -match "(?m)^title:\s*'(.*?)'") { $Matches[1] }
             else { "" }
    
    # Extract publication - may span multiple lines
    $pub = ""
    if ($fm -match '(?m)^publication:\s*"(.*?)"') { $pub = $Matches[1] }
    elseif ($fm -match "(?m)^publication:\s*'(.*?)'") { $pub = $Matches[1] }
    elseif ($fm -match '(?ms)^publication:\s*"(.*?)"') { $pub = $Matches[1] }
    # Strip HTML <a> tags from publication field  
    $pub = $pub -replace '<a [^>]*>', '' -replace '</a>', ''
    $pub = $pub.Trim()
    
    # Extract authors - use [^\n] to avoid matching across lines
    $authorLines = @()
    if ($fm -match '(?m)^authors:\s*\r?\n((?:[^\S\n]*-[^\n]*\r?\n)*)') {
        $authorBlock = $Matches[1]
        $authorLines = ($authorBlock -split '\r?\n') | ForEach-Object {
            $_.Trim()
        } | Where-Object { $_ -match '^- ' -and $_ -notmatch '^- "?\d' -and $_ -notmatch '^- name:' }
    }
    
    $date = if ($fm -match '(?m)^date:\s*"(.*?)"') { $Matches[1] } else { "" }
    $doi = if ($fm -match '(?m)^doi:\s*"(.*?)"') { $Matches[1] } else { "" }
    $abstract = ""
    # Extract abstract - content between quotes after abstract:
    $abstractIdx = $fm.IndexOf("`nabstract:")
    if ($abstractIdx -ge 0) {
        $afterAbstract = $fm.Substring($abstractIdx + 1)
        if ($afterAbstract -match '(?s)abstract:\s*"(.*?)"(?:\r?\n\r?\n|\r?\n[a-z_]|\r?\n$)') {
            $abstract = $Matches[1]
        } elseif ($afterAbstract -match '(?s)abstract:\s*"(.*?)"$') {
            $abstract = $Matches[1]
        }
    }
    
    # Extract existing named links
    $linkEntries = @()
    $linksIdx = $fm.IndexOf("`nlinks:")
    if ($linksIdx -ge 0) {
        $afterLinks = $fm.Substring($linksIdx + 1)
        # Get lines until we hit a non-indented line
        $linkLines = @()
        $started = $false
        foreach ($ll in ($afterLinks -split '\r?\n')) {
            if ($ll -match '^links:') { $started = $true; continue }
            if ($started) {
                if ($ll -match '^\s+- ' -or $ll -match '^\s+\w') {
                    if ($ll -notmatch '^\s*#') { $linkLines += $ll }
                } elseif ($ll.Trim() -eq '') { continue }
                else { break }
            }
        }
        $linkBlock = $linkLines -join "`n"
        $linkPairs = $linkBlock -split '(?=\s+- name:)'
        foreach ($lp in $linkPairs) {
            if ($lp -match 'name:\s*(.+)') {
                $lname = $Matches[1].Trim().Trim('"').Trim("'")
                if ($lp -match 'url:\s*"?(.*?)"?\s*$' ) {
                    $lurl = $Matches[1].Trim().Trim('"').Trim("'")
                    if ($lurl -and $lurl -ne '#') {
                        $linkEntries += @{ name = $lname; url = $lurl }
                    }
                }
            }
        }
    }
    
    # Extract url_* fields and convert to named links
    if ($fm -match '(?m)^url_code:\s*[''"]?(https?://[^\s''"]+)') {
        $linkEntries += @{ name = "Code"; url = $Matches[1] }
    }
    if ($fm -match '(?m)^url_dataset:\s*[''"]?(https?://[^\s''"]+)') {
        $linkEntries += @{ name = "Dataset"; url = $Matches[1] }
    }
    if ($fm -match '(?m)^url_video:\s*[''"]?(https?://[^\s''"]+)') {
        $linkEntries += @{ name = "Video"; url = $Matches[1] }
    }
    if ($fm -match '(?m)^url_pdf:\s*[''"]?(https?://[^\s''"]+)') {
        # Only add if not already in links as "PDF"
        $hasPdf = $linkEntries | Where-Object { $_.name -eq "PDF" }
        if (!$hasPdf) {
            $linkEntries += @{ name = "PDF"; url = $Matches[1] }
        }
    }
    if ($fm -match '(?m)^url_project:\s*[''"]?(https?://[^\s''"]+)') {
        $linkEntries += @{ name = "Project"; url = $Matches[1] }
    }
    
    # Extract author_notes if present
    $authorNotes = ""
    if ($fm -match '(?ms)^author_notes:\s*\r?\n((?:\s+- .*\r?\n?)*)') {
        $authorNotes = $Matches[0].Trim()
    }
    
    # Build new frontmatter
    $newFm = "---`n"
    $newFm += "title: `"$title`"`n"
    $newFm += "authors:`n"
    foreach ($a in $authorLines) {
        $newFm += "  $a`n"
    }
    if ($authorNotes) {
        $newFm += "$authorNotes`n"
    }
    $newFm += "date: `"$date`"`n"
    $newFm += "publication_types: [`"article-journal`"]`n"
    $newFm += "publication: `"$pub`"`n"
    $newFm += "abstract: `"$abstract`"`n"
    $newFm += "featured: true`n"
    $newFm += "add_badge: true`n"
    if ($doi) {
        $newFm += "hugoblox:`n"
        $newFm += "  ids:`n"
        $newFm += "    doi: `"$doi`"`n"
    }
    if ($linkEntries.Count -gt 0) {
        $newFm += "links:`n"
        foreach ($le in $linkEntries) {
            $newFm += "  - name: $($le.name)`n"
            $newFm += "    url: `"$($le.url)`"`n"
        }
    }
    $newFm += "---`n"

    # Create output directory and file
    $outDir = Join-Path $newDir $d.Name
    New-Item -ItemType Directory -Path $outDir -Force | Out-Null
    
    $content = $newFm
    if ($body) {
        $content += "`n$body`n"
    }
    
    Set-Content -Path (Join-Path $outDir "index.md") -Value $content -Encoding UTF8 -NoNewline
    Write-Host "OK: $($d.Name)"
}

Write-Host "`nDone! Processed $($dirs.Count) publications"
