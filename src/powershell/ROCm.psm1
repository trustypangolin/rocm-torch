$StableReleases = @(
    @{
        Label = "7.2.1"
        RocmRel = "7.2.1"
        BaseUrl = "https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/"
        Torch = "torch-2.9.1+rocm7.2.1-cp312-cp312-win_amd64.whl"
        TorchAudio = "torchaudio-2.9.1+rocm7.2.1-cp312-cp312-win_amd64.whl"
        TorchVision = "torchvision-0.24.1+rocm7.2.1-cp312-cp312-win_amd64.whl"
        RocmSdkCore = "rocm_sdk_core-7.2.1-py3-none-win_amd64.whl"
        RocmSdkDevel = "rocm_sdk_devel-7.2.1-py3-none-win_amd64.whl"
        RocmSdkLibs = "rocm_sdk_libraries_custom-7.2.1-py3-none-win_amd64.whl"
        RocmTarball = "rocm-7.2.1.tar.gz"
        PyTorchVersion = "2.9.1"
        TorchvisionVersion = "0.24.1"
        TorchaudioVersion = "2.9.1"
        DriverRequired = "26.2.2"
        Type = "stable"
        OS = "Windows"
        PythonVersions = @("py312")
    },
    @{
        Label = "7.2"
        RocmRel = "7.2"
        BaseUrl = "https://repo.radeon.com/rocm/windows/rocm-rel-7.2/"
        Torch = "torch-2.9.1+rocmsdk20260116-cp312-cp312-win_amd64.whl"
        TorchAudio = "torchaudio-2.9.1+rocmsdk20260116-cp312-cp312-win_amd64.whl"
        TorchVision = "torchvision-0.24.1+rocmsdk20260116-cp312-cp312-win_amd64.whl"
        RocmSdkCore = "rocm_sdk_core-7.2.0.dev0-py3-none-win_amd64.whl"
        RocmSdkDevel = "rocm_sdk_devel-7.2.0.dev0-py3-none-win_amd64.whl"
        RocmSdkLibs = "rocm_sdk_libraries_custom-7.2.0.dev0-py3-none-win_amd64.whl"
        RocmTarball = "rocm-7.2.0.dev0.tar.gz"
        PyTorchVersion = "2.9.1"
        TorchvisionVersion = "0.24.1"
        TorchaudioVersion = "2.9.1"
        DriverRequired = "26.1.1"
        Type = "stable"
        OS = "Windows"
        PythonVersions = @("py312")
    },
    @{
        Label = "7.1.1"
        RocmRel = "7.1.1"
        BaseUrl = "https://repo.radeon.com/rocm/windows/rocm-rel-7.1.1/"
        Torch = "torch-2.9.0+rocmsdk20251116-cp312-cp312-win_amd64.whl"
        TorchAudio = "torchaudio-2.9.0+rocmsdk20251116-cp312-cp312-win_amd64.whl"
        TorchVision = "torchvision-0.24.0+rocmsdk20251116-cp312-cp312-win_amd64.whl"
        RocmSdkCore = "rocm_sdk_core-0.1.dev0-py3-none-win_amd64.whl"
        RocmSdkDevel = "rocm_sdk_devel-0.1.dev0-py3-none-win_amd64.whl"
        RocmSdkLibs = "rocm_sdk_libraries_custom-0.1.dev0-py3-none-win_amd64.whl"
        RocmTarball = "rocm-0.1.dev0.tar.gz"
        PyTorchVersion = "2.9.0"
        TorchvisionVersion = "0.24.0"
        TorchaudioVersion = "2.9.0"
        DriverRequired = "N/A"
        Type = "stable"
        OS = "Windows"
        PythonVersions = @("py312")
    },
    @{
        Label = "6.4.4"
        RocmRel = "6.4.4"
        BaseUrl = "https://repo.radeon.com/rocm/windows/rocm-rel-6.4.4/"
        Torch = "torch-2.8.0a0+gitfc14c65-cp312-cp312-win_amd64.whl"
        TorchAudio = ""
        TorchVision = "torchvision-0.24.0a0+c85f008-cp312-cp312-win_amd64.whl"
        RocmSdkCore = ""
        RocmSdkDevel = ""
        RocmSdkLibs = ""
        RocmTarball = ""
        PyTorchVersion = "2.8.0a0"
        TorchvisionVersion = "0.24.0a0"
        TorchaudioVersion = "N/A"
        DriverRequired = "N/A"
        Type = "stable"
        OS = "Windows"
        PythonVersions = @("py312")
    }
)

$NightlyVersions = @(
    @{ PyTorch = "2.12.0a0"; Torchvision = "0.26.0a0"; Torchaudio = "2.12.0a0"; Type = "nightly"; Label = "2.12-nightly"; RocmSuffix = "7.13.0a20260426"; PythonVersions = @("py311","py312","py313"); Notes = "May be unstable" },
    @{ PyTorch = "2.11";     Torchvision = "0.25";     Torchaudio = "2.11";     Type = "stable";  Label = "2.11";     RocmSuffix = "7.13.0a20260426"; PythonVersions = @("py311","py312","py313"); Notes = "" },
    @{ PyTorch = "2.10";     Torchvision = "0.25";     Torchaudio = "2.10";     Type = "stable";  Label = "2.10";     RocmSuffix = "7.12.0";          PythonVersions = @("py311","py312","py313"); Notes = "" },
    @{ PyTorch = "2.9";      Torchvision = "0.24";     Torchaudio = "2.9";      Type = "stable";  Label = "2.9";      RocmSuffix = "7.12.0";          PythonVersions = @("py311","py312","py313"); Notes = "" }
)

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
