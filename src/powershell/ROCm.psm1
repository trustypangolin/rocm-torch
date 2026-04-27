$Script:CuratedDir = Join-Path $PSScriptRoot "..\curated"

$Script:StableKeyMap = @{
    "rocm_rel" = "RocmRel"
    "base_url" = "BaseUrl"
    "torch" = "Torch"
    "torchaudio" = "TorchAudio"
    "torchvision" = "TorchVision"
    "rocm_sdk_core" = "RocmSdkCore"
    "rocm_sdk_devel" = "RocmSdkDevel"
    "rocm_sdk_libraries_custom" = "RocmSdkLibs"
    "rocm_tarball" = "RocmTarball"
    "pytorch_version" = "PyTorchVersion"
    "torchvision_version" = "TorchvisionVersion"
    "torchaudio_version" = "TorchaudioVersion"
    "driver_required" = "DriverRequired"
    "type" = "Type"
    "os" = "OS"
    "python_versions" = "PythonVersions"
    "label" = "Label"
}

$Script:NightlyKeyMap = @{
    "pytorch" = "PyTorch"
    "torchvision" = "Torchvision"
    "torchaudio" = "Torchaudio"
    "type" = "Type"
    "label" = "Label"
    "rocm_suffix" = "RocmSuffix"
    "python_versions" = "PythonVersions"
    "notes" = "Notes"
}

function Script:Convert-JsonToHashtable {
    param([pscustomobject]$Obj, [hashtable]$KeyMap)
    $ht = @{}
    foreach ($prop in $Obj.PSObject.Properties) {
        $jsonKey = $prop.Name
        $key = if ($KeyMap.ContainsKey($jsonKey)) { $KeyMap[$jsonKey] } else { $jsonKey.Substring(0, 1).ToUpper() + $jsonKey.Substring(1) }
        $value = $prop.Value
        if ($value -is [System.Array]) {
            $value = @($value)
        }
        $ht[$key] = $value
    }
    return $ht
}

function Script:Load-StableReleases {
    $path = Join-Path $Script:CuratedDir "stable_releases.json"
    $json = Get-Content $path -Raw | ConvertFrom-Json
    return @($json | ForEach-Object { Convert-JsonToHashtable -Obj $_ -KeyMap $Script:StableKeyMap })
}

function Script:Load-NightlyVersions {
    param([string]$Path)
    if (-not $Path) {
        $Path = Join-Path $Script:CuratedDir "nightly_versions.json"
    }
    $json = Get-Content $Path -Raw | ConvertFrom-Json
    return @($json | ForEach-Object { Convert-JsonToHashtable -Obj $_ -KeyMap $Script:NightlyKeyMap })
}

$StableReleases = Load-StableReleases

$LatestPath = Join-Path $Script:CuratedDir "latest_versions.json"
$FallbackPath = Join-Path $Script:CuratedDir "nightly_versions.json"
if (Test-Path $LatestPath) {
    $NightlyVersions = Load-NightlyVersions -Path $LatestPath
} elseif (Test-Path $FallbackPath) {
    $NightlyVersions = Load-NightlyVersions -Path $FallbackPath
} else {
    $NightlyVersions = @()
}

function Get-StableReleases {
    return $StableReleases
}

function Get-NightlyVersions {
    return $NightlyVersions
}

function Get-ReleaseByLabel {
    param([string]$Label)
    foreach ($rel in $StableReleases) {
        if ($rel.Label -eq $Label) {
            return $rel
        }
    }
    foreach ($rel in $NightlyVersions) {
        if ($rel.Label -eq $Label) {
            return $rel
        }
    }
    return $null
}

function Get-LatestNightly {
    if ($NightlyVersions.Count -gt 0) {
        return $NightlyVersions[0]
    }
    return $null
}

function Filter-StableByOS {
    param([string]$OS)
    return $StableReleases | Where-Object { $_.OS -eq $OS }
}

function Filter-NightlyByPython {
    param([string]$PyTag)
    return $NightlyVersions | Where-Object { $_.PythonVersions -contains $PyTag }
}
