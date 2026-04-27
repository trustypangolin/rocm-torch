function Read-UserChoice {
    param([string]$Prompt, [array]$ValidChoices)
    while ($true) {
        $choice = Read-Host $Prompt
        if ($ValidChoices -contains $choice) {
            return $choice
        }
        Write-Host "Invalid choice. Valid options: $($ValidChoices -join ', ')" -ForegroundColor Yellow
    }
}

function Show-OSMenu {
    Write-Host "`nTarget OS:" -ForegroundColor Cyan
    Write-Host "  [1] Windows (default)"
    Write-Host "  [2] Linux (Debian/Ubuntu)"
    Write-Host "  [3] Both (generate for each)"
    Write-Host ""
    $choice = Read-UserChoice "Enter choice" @("1", "2", "3")
    switch ($choice) {
        "1" { return @("Windows") }
        "2" { return @("Linux") }
        "3" { return @("Windows", "Linux") }
    }
}

function Show-PythonMenu {
    Write-Host "`nPython version(s) to generate for:" -ForegroundColor Cyan
    Write-Host "  [1] 3.11 (stable support)"
    Write-Host "  [2] 3.12 (recommended)"
    Write-Host "  [3] 3.13"
    Write-Host "  [4] 3.14 (experimental)"
    Write-Host "  [a] All supported (3.11-3.13)"
    Write-Host "  [c] Current Python version"
    Write-Host ""
    $choice = Read-UserChoice "Enter choice" @("1", "2", "3", "4", "a", "c")
    switch ($choice) {
        "1" { return @("py311") }
        "2" { return @("py312") }
        "3" { return @("py313") }
        "4" { return @("py314") }
        "a" { return @("py311", "py312", "py313") }
        "c" {
            $tag = Get-CurrentPythonVersion
            return @($tag)
        }
    }
}

function Show-StableMenu {
    Write-Host "`nUse supported stable releases from repo.radeon.com? (y/n)" -ForegroundColor Cyan
    Write-Host "These require matching AMD Adrenalin driver versions."
    Write-Host "Note: Stable is Windows + Python 3.12 only."
    Write-Host ""
    $choice = Read-UserChoice "Enter choice" @("y", "n")
    return ($choice -eq "y")
}

function Show-StableOptions {
    param([array]$StableReleases)
    Write-Host "`nSelect stable release:" -ForegroundColor Cyan
    Write-Host ""
    for ($i = 0; $i -lt $StableReleases.Count; $i++) {
        $rel = $StableReleases[$i]
        Write-Host ("  [{0}] {1} - PyTorch {2}, Driver {3}" -f ($i + 1), $rel.Label, $rel.PyTorchVersion, $rel.DriverRequired)
    }
    Write-Host "  [a] All stable releases"
    Write-Host ""
    $validChoices = @(1..$StableReleases.Count | ForEach-Object { [string]$_ }) + @("a")
    $choice = Read-UserChoice "Enter choice" $validChoices
    if ($choice -eq "a") {
        return $StableReleases
    }
    $idx = [int]$choice - 1
    return @($StableReleases[$idx])
}

function Show-NightlyPrompt {
    Write-Host "`nUse latest nightly release from rocm.nightlies.amd.com? (y/n)" -ForegroundColor Cyan
    Write-Host "  [y] Yes - use latest available build"
    Write-Host "  [n] No  - select from all available versions"
    Write-Host ""
    $choice = Read-UserChoice "Enter choice" @("y", "n")
    return ($choice -eq "y")
}

function Show-FullMenu {
    param([array]$NightlyVersions, [array]$StableReleases)
    Write-Host "`nSelect a version to generate requirements for:" -ForegroundColor Cyan
    Write-Host ""

    $fmt = "  {0,-4} {1,-18} {2,-10} {3,-12} {4,-12} {5,-20} {6,-14} {7,-8} {8}"
    Write-Host ($fmt -f "#", "Label", "PyTorch", "torchvision", "torchaudio", "ROCm Suffix", "Python", "OS", "Notes")
    Write-Host ($fmt -f "-", "---", "---", "---", "---", "---", "---", "---", "---")

    $idx = 1
    $allEntries = @()
    foreach ($entry in $NightlyVersions) {
        $pyRange = "3.11-3.13"
        $os = "Win, Lnx"
        $pytorchDisplay = $entry.PyTorch -replace '\.0a0$', 'a0'
        $tvDisplay = $entry.Torchvision -replace '\.0a0$', 'a0'
        $taDisplay = $entry.Torchaudio -replace '\.0a0$', 'a0'
        Write-Host ($fmt -f $idx, $entry.Label, $pytorchDisplay, $tvDisplay, $taDisplay, $entry.RocmSuffix, $pyRange, $os, $entry.Notes)
        $allEntries += @{ Entry = $entry; Index = $idx }
        $idx++
    }

    foreach ($rel in $StableReleases) {
        $label = "$($rel.Label) (stable)"
        $os = "Win"
        $notes = if ($rel.DriverRequired -ne "N/A") { "Driver $($rel.DriverRequired)" } else { "" }
        Write-Host ($fmt -f $idx, $label, $rel.PyTorchVersion, $rel.TorchvisionVersion, $rel.TorchaudioVersion, $rel.RocmRel, "3.12 only", $os, $notes)
        $allEntries += @{ Entry = $rel; Index = $idx }
        $idx++
    }

    Write-Host ""
    $validChoices = @(1..($allEntries.Count) | ForEach-Object { [string]$_ }) + @("all")
    $choice = Read-UserChoice "Enter number (or 'all' to generate all)" $validChoices
    if ($choice -eq "all") {
        return $allEntries | ForEach-Object { $_.Entry }
    }
    $num = [int]$choice
    $selected = $allEntries | Where-Object { $_.Index -eq $num }
    if ($selected) {
        return @($selected.Entry)
    }
    return @($NightlyVersions[0])
}

function Show-OutputSummary {
    param([array]$GeneratedFiles)
    if ($GeneratedFiles.Count -eq 0) { return }
    Write-Host "`n=== Generated Requirements Files ===" -ForegroundColor Green
    $fmt = "  {0,-45} {1,-10} {2,-10} {3,-10} {4,-15} {5,-8} {6}"
    Write-Host ($fmt -f "File", "PyTorch", "tv", "ta", "ROCm", "Python", "Notes")
    Write-Host ($fmt -f "----", "-------", "--", "--", "----", "------", "-----")
    foreach ($f in $GeneratedFiles) {
        $notes = if ($f.Notes) { $f.Notes } else { "" }
        Write-Host ($fmt -f $f.File, $f.PyTorch, $f.Torchvision, $f.Torchaudio, $f.ROCm, $f.Python, $notes)
    }
    Write-Host "`nTotal: $($GeneratedFiles.Count) file(s) generated" -ForegroundColor Green
}
