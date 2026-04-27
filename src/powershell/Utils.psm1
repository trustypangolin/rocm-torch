function Write-Log {
    param(
        [string]$Message,
        [ValidateSet("INFO", "WARN", "ERROR", "SUCCESS")]
        [string]$Level = "INFO"
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $prefix = "[$timestamp] [$Level]"
    switch ($Level) {
        "INFO"    { Write-Host "$prefix $Message" -ForegroundColor White }
        "WARN"    { Write-Host "$prefix $Message" -ForegroundColor Yellow }
        "ERROR"   { Write-Host "$prefix $Message" -ForegroundColor Red }
        "SUCCESS" { Write-Host "$prefix $Message" -ForegroundColor Green }
    }
}

function Test-Network {
    param([string]$Url)
    try {
        $response = Invoke-WebRequest -Uri $Url -Method Head -TimeoutSec 10 -UseBasicParsing
        return $response.StatusCode -eq 200
    } catch {
        return $false
    }
}

function Confirm-Overwrite {
    param([string]$FilePath)
    if (Test-Path $FilePath) {
        $choice = Read-Host "File '$FilePath' already exists. Overwrite? (y/n)"
        return $choice -eq "y"
    }
    return $true
}

function Validate-DriverVersion {
    param([string]$RequiredVersion)
    if ($RequiredVersion -eq "N/A") {
        return @{ Valid = $true; Message = "No driver version required" }
    }
    try {
        $installed = Get-CimInstance -ClassName Win32_PnPSignedDriver |
            Where-Object { $_.DeviceName -like "*AMD*" -and $_.DriverVersion } |
            Select-Object -First 1 -ExpandProperty DriverVersion
        if (-not $installed) {
            return @{ Valid = $false; Message = "No AMD driver found" }
        }
        $required = $RequiredVersion -split '\.' | ForEach-Object { [int]$_ }
        $actual = $installed -split '\.' | ForEach-Object { [int]$_ }
        for ($i = 0; $i -lt [Math]::Min($required.Count, $actual.Count); $i++) {
            if ($actual[$i] -gt $required[$i]) { return @{ Valid = $true; Message = "Driver $installed >= $RequiredVersion" } }
            if ($actual[$i] -lt $required[$i]) { return @{ Valid = $false; Message = "Driver $installed < $RequiredVersion" } }
        }
        return @{ Valid = $true; Message = "Driver $installed matches $RequiredVersion" }
    } catch {
        return @{ Valid = $false; Message = "Could not check driver version: $_" }
    }
}

function Test-AdminPrivileges {
    $identity = [Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()
    return $identity.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Format-Table {
    param(
        [string[]]$Headers,
        [object[]]$Rows
    )
    if ($Rows.Count -eq 0) { return "" }
    $colWidths = @()
    for ($i = 0; $i -lt $Headers.Count; $i++) {
        $max = $Headers[$i].Length
        foreach ($row in $Rows) {
            $val = [string]$row[$i]
            if ($val.Length -gt $max) { $max = $val.Length }
        }
        $colWidths += $max
    }
    $headerLine = ""
    for ($i = 0; $i -lt $Headers.Count; $i++) {
        $headerLine += "{0,-$($colWidths[$i])} " -f $Headers[$i]
    }
    $sepLine = ""
    for ($i = 0; $i -lt $Headers.Count; $i++) {
        $sepLine += ("-" * $colWidths[$i]) + " "
    }
    $lines = @($headerLine, $sepLine)
    foreach ($row in $Rows) {
        $line = ""
        for ($i = 0; $i -lt $Headers.Count; $i++) {
            $line += "{0,-$($colWidths[$i])} " -f [string]$row[$i]
        }
        $lines += $line
    }
    return $lines -join "`n"
}
