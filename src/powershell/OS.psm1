$OSTargets = @{
    Windows = @{
        Tag = "win"
        Platform = "win_amd64"
        IndexBase = "https://rocm.nightlies.amd.com/v2/gfx1151/"
        StableBase = "https://repo.radeon.com/rocm/windows/rocm-rel-{0}/"
    }
    Linux = @{
        Tag = "linux"
        Platform = "linux_x86_64"
        IndexBase = "https://rocm.nightlies.amd.com/v2/gfx1151/"
        StableBase = $null
    }
}

function Get-OSTarget {
    param([string]$Name)
    $normalized = $Name.Substring(0, 1).ToUpper() + $Name.Substring(1).ToLower()
    if ($OSTargets.ContainsKey($normalized)) {
        return $OSTargets[$normalized]
    }
    return $null
}

function Validate-OS {
    param([string]$OS, [string]$ReleaseType)
    if ($ReleaseType -eq "stable" -and $OS -eq "Linux") {
        return $false
    }
    return $OSTargets.ContainsKey($OS.Substring(0, 1).ToUpper() + $OS.Substring(1).ToLower())
}

function Get-AllOSTargets {
    return $OSTargets
}

function Get-OSDisplayName {
    param([string]$OS)
    switch ($OS.ToLower()) {
        "windows" { return "Windows" }
        "linux"   { return "Linux (Debian/Ubuntu)" }
        default   { return $OS }
    }
}
