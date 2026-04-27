function Generate-IndexBased {
    param([hashtable]$Entry, [string]$PyTag)
    $preFlag = ""
    if ($Entry.PyTorch -match "a0$") {
        $preFlag = "--pre`n"
    }
    $Content = @"
--index-url https://rocm.nightlies.amd.com/v2/gfx1151/
$preFlag
torch==$($Entry.PyTorch)+rocm$($Entry.RocmSuffix)
torchvision==$($Entry.Torchvision)+rocm$($Entry.RocmSuffix)
torchaudio==$($Entry.Torchaudio)+rocm$($Entry.RocmSuffix)
rocm==$($Entry.RocmSuffix)
rocm-sdk-core==$($Entry.RocmSuffix)
rocm-sdk-libraries-gfx1151==$($Entry.RocmSuffix)
"@
    return $Content.Trim()
}

function Generate-DirectURL {
    param([hashtable]$Entry, [string]$PyTag, [string]$OSTag)
    if ($PyTag -ne "py312") {
        return $null
    }
    $lines = @("# ROCm SDK (install first)")
    foreach ($key in @("RocmSdkCore", "RocmSdkDevel", "RocmSdkLibs", "RocmTarball")) {
        $val = $Entry[$key]
        if ($val -and $val -ne "") {
            $lines += "$($Entry.BaseUrl)$val"
        }
    }
    $lines += ""
    $lines += "# PyTorch packages"
    foreach ($key in @("Torch", "TorchAudio", "TorchVision")) {
        $val = $Entry[$key]
        if ($val -and $val -ne "") {
            $lines += "$($Entry.BaseUrl)$val"
        }
    }
    return ($lines -join "`n").Trim()
}

function Get-OutputFileName {
    param([hashtable]$Entry, [string]$PyTag, [string]$OSTag, [string]$OutputDir)
    $label = $Entry.Label
    $isDirectStable = ($Entry.Type -eq "stable" -and $Entry.ContainsKey("DriverRequired"))
    if ($isDirectStable) {
        $baseName = "requirements-$label-stable-$OSTag-$PyTag.txt"
    } else {
        $typeSuffix = if ($Entry.Type -eq "nightly") { "-nightly" } else { "" }
        $baseName = "requirements-$label$typeSuffix-$PyTag.txt"
    }
    if ($OutputDir -and $OutputDir -ne ".") {
        return Join-Path $OutputDir $baseName
    }
    return $baseName
}

function Write-RequirementsFile {
    param([string]$Content, [string]$FilePath, [switch]$DryRun)
    if ($DryRun) {
        Write-Host "[DRY RUN] Would write: $FilePath"
        Write-Host "---"
        Write-Host $Content
        Write-Host "---"
        return $true
    }
    $dir = Split-Path $FilePath -Parent
    if ($dir -and $dir -ne "." -and -not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    if (Test-Path $FilePath) {
        $overwrite = Confirm-Overwrite -FilePath $FilePath
        if (-not $overwrite) {
            Write-Log "Skipping: $FilePath" -Level "WARN"
            return $false
        }
    }
    $Content | Out-File -FilePath $FilePath -Encoding utf8
    Write-Log "Written: $FilePath" -Level "SUCCESS"
    return $true
}

function Generate-AllForSelection {
    param(
        [hashtable]$Entry,
        [string[]]$PyTags,
        [string[]]$OSTargetList,
        [string]$OutputDir,
        [switch]$DryRun
    )
    $generated = @()
    foreach ($pyTag in $PyTags) {
        if ($Entry.PythonVersions -and ($Entry.PythonVersions -notcontains $pyTag)) {
            $ver = $pyTag -replace 'py', '3.'
            Write-Log "$($Entry.Label) does not support Python $pyTag, skipping" -Level "WARN"
            continue
        }
        if ($Entry.Type -eq "stable" -and $Entry.ContainsKey("DriverRequired")) {
            if ("Linux" -in $OSTargetList) {
                Write-Log "Stable release $($Entry.Label) is Windows only, skipping Linux" -Level "WARN"
            }
            if ($pyTag -ne "py312") {
                Write-Log "Stable release $($Entry.Label) only supports Python 3.12, skipping $pyTag" -Level "WARN"
                continue
            }
            $osTag = "win"
            $filePath = Get-OutputFileName -Entry $Entry -PyTag $pyTag -OSTag $osTag -OutputDir $OutputDir
            $content = Generate-DirectURL -Entry $Entry -PyTag $pyTag -OSTag $osTag
            if ($null -eq $content) { continue }
            $result = Write-RequirementsFile -Content $content -FilePath $filePath -DryRun:$DryRun
            if ($result) {
                $driverNote = if ($Entry.DriverRequired -ne "N/A") { "Requires driver $($Entry.DriverRequired)" } else { "" }
                $generated += @{
                    File = (Split-Path $filePath -Leaf)
                    PyTorch = $Entry.PyTorchVersion
                    Torchvision = $Entry.TorchvisionVersion
                    Torchaudio = $Entry.TorchaudioVersion
                    ROCm = $Entry.RocmRel
                    OS = "Windows"
                    Python = ($pyTag -replace 'py', '')
                    Notes = $driverNote
                }
            }
        } else {
            foreach ($osName in $OSTargetList) {
                $osInfo = Get-OSTarget -Name $osName
                $filePath = Get-OutputFileName -Entry $Entry -PyTag $pyTag -OSTag $osInfo.Tag -OutputDir $OutputDir
                $content = Generate-IndexBased -Entry $Entry -PyTag $pyTag
                $result = Write-RequirementsFile -Content $content -FilePath $filePath -DryRun:$DryRun
                if ($result) {
                    $generated += @{
                        File = (Split-Path $filePath -Leaf)
                        PyTorch = $Entry.PyTorch
                        Torchvision = $Entry.Torchvision
                        Torchaudio = $Entry.Torchaudio
                        ROCm = $Entry.RocmSuffix
                        OS = "Cross-OS (index)"
                        Python = ($pyTag -replace 'py', '')
                        Notes = $Entry.Notes
                    }
                }
            }
        }
    }
    return $generated
}
