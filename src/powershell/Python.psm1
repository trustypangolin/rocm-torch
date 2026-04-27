$PythonVersions = @(
    @{ Major = 3; Minor = 11; Tag = "py311"; CPTag = "cp311"; Supported = $true;  Notes = "Stable support" },
    @{ Major = 3; Minor = 12; Tag = "py312"; CPTag = "cp312"; Supported = $true;  Notes = "Recommended" },
    @{ Major = 3; Minor = 13; Tag = "py313"; CPTag = "cp313"; Supported = $true;  Notes = "" },
    @{ Major = 3; Minor = 14; Tag = "py314"; CPTag = "cp314"; Supported = $false; Notes = "Experimental, limited availability" }
)

function Get-PythonVersions {
    param([string]$Selection)
    switch ($Selection) {
        "3.11"  { return @("py311") }
        "3.12"  { return @("py312") }
        "3.13"  { return @("py313") }
        "3.14"  { return @("py314") }
        "all"   { return @("py311", "py312", "py313") }
        "current" {
            $tag = Get-CurrentPythonVersion
            return @($tag)
        }
        default { return @("py312") }
    }
}

function Get-CurrentPythonVersion {
    try {
        $version = python --version 2>&1
        $match = [regex]::Match($version, 'Python (\d+\.\d+)')
        if ($match.Success) {
            $ver = $match.Groups[1].Value
            return "py" + $ver.Replace(".", "")
        }
    } catch {
    }
    return "py312"
}

function Validate-PythonForRelease {
    param([string]$PyTag, [array]$SupportedVersions)
    return $SupportedVersions -contains $PyTag
}

function Get-PythonDisplayString {
    param([array]$Versions)
    if ($Versions.Count -eq 0) { return "None" }
    if ($Versions.Count -eq 1) { return $Versions[0] -replace 'py', '3.' }
    $first = $Versions[0] -replace 'py(\d)(\d+)', '$1.$2'
    $last = $Versions[-1] -replace 'py(\d)(\d+)', '$1.$2'
    return "$first-$last"
}

function Get-PythonTagFromVersion {
    param([string]$Version)
    $normalized = $Version.Replace(".", "")
    return "py$normalized"
}
