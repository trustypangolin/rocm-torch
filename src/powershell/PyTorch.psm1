$PyTorchMatrix = @(
    @{ Version = "2.12a"; Type = "nightly"; PythonVersions = @("3.11","3.12","3.13"); OSSupport = "Win,Linux"; Notes = "May be unstable" },
    @{ Version = "2.11";  Type = "stable";  PythonVersions = @("3.11","3.12","3.13"); OSSupport = "Win,Linux"; Notes = "" },
    @{ Version = "2.10";  Type = "stable";  PythonVersions = @("3.11","3.12","3.13"); OSSupport = "Win,Linux"; Notes = "" },
    @{ Version = "2.9";   Type = "stable";  PythonVersions = @("3.11","3.12","3.13"); OSSupport = "Win,Linux"; Notes = "" }
)

function Get-PyTorchCompat {
    param([string]$Version)
    $base = $Version -replace 'a$', '' -replace '\.0a0$', ''
    foreach ($entry in $PyTorchMatrix) {
        $entryBase = $entry.Version -replace 'a$', ''
        if ($entryBase -eq $base) {
            return $entry
        }
    }
    return $null
}

function Validate-PyTorchVersion {
    param([string]$Version, [string]$PythonVersion, [string]$OS)
    $compat = Get-PyTorchCompat -Version $Version
    if (-not $compat) {
        return $false
    }
    $osShort = if ($OS -eq "Windows") { "Win" } else { "Lnx" }
    if ($compat.OSSupport -notcontains $osShort -and $compat.OSSupport -notcontains "Win,Linux") {
        return $false
    }
    return $compat.PythonVersions -contains $PythonVersion
}

function Get-PyTorchVersionForROCm {
    param([string]$ROCmVersion)
    switch -Regex ($ROCmVersion) {
        "^7\.2"  { return "2.9.1" }
        "^7\.1"  { return "2.9.0" }
        "^6\.4"  { return "2.8.0a0" }
        "^7\.13" { return "2.12.0a0" }
        "^7\.12" { return "2.11" }
        default  { return "2.11" }
    }
}

function Get-PyTorchDisplayTable {
    $headers = @("Version", "Type", "Python", "OS", "Notes")
    $rows = @()
    foreach ($entry in $PyTorchMatrix) {
        $rows += @(
            @(
                $entry.Version,
                $entry.Type,
                ($entry.PythonVersions -join ", "),
                $entry.OSSupport,
                $entry.Notes
            )
        )
    }
    return @{ Headers = $headers; Rows = $rows }
}
