from typing import List, Optional

STABLE_RELEASES = [
    {
        "label": "7.2.1",
        "rocm_rel": "7.2.1",
        "base_url": "https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/",
        "torch": "torch-2.9.1+rocm7.2.1-cp312-cp312-win_amd64.whl",
        "torchaudio": "torchaudio-2.9.1+rocm7.2.1-cp312-cp312-win_amd64.whl",
        "torchvision": "torchvision-0.24.1+rocm7.2.1-cp312-cp312-win_amd64.whl",
        "rocm_sdk_core": "rocm_sdk_core-7.2.1-py3-none-win_amd64.whl",
        "rocm_sdk_devel": "rocm_sdk_devel-7.2.1-py3-none-win_amd64.whl",
        "rocm_sdk_libraries_custom": "rocm_sdk_libraries_custom-7.2.1-py3-none-win_amd64.whl",
        "rocm_tarball": "rocm-7.2.1.tar.gz",
        "pytorch_version": "2.9.1",
        "torchvision_version": "0.24.1",
        "torchaudio_version": "2.9.1",
        "driver_required": "26.2.2",
        "type": "stable",
        "os": "Windows",
        "python_versions": ["py312"],
    },
    {
        "label": "7.2",
        "rocm_rel": "7.2",
        "base_url": "https://repo.radeon.com/rocm/windows/rocm-rel-7.2/",
        "torch": "torch-2.9.1+rocmsdk20260116-cp312-cp312-win_amd64.whl",
        "torchaudio": "torchaudio-2.9.1+rocmsdk20260116-cp312-cp312-win_amd64.whl",
        "torchvision": "torchvision-0.24.1+rocmsdk20260116-cp312-cp312-win_amd64.whl",
        "rocm_sdk_core": "rocm_sdk_core-7.2.0.dev0-py3-none-win_amd64.whl",
        "rocm_sdk_devel": "rocm_sdk_devel-7.2.0.dev0-py3-none-win_amd64.whl",
        "rocm_sdk_libraries_custom": "rocm_sdk_libraries_custom-7.2.0.dev0-py3-none-win_amd64.whl",
        "rocm_tarball": "rocm-7.2.0.dev0.tar.gz",
        "pytorch_version": "2.9.1",
        "torchvision_version": "0.24.1",
        "torchaudio_version": "2.9.1",
        "driver_required": "26.1.1",
        "type": "stable",
        "os": "Windows",
        "python_versions": ["py312"],
    },
    {
        "label": "7.1.1",
        "rocm_rel": "7.1.1",
        "base_url": "https://repo.radeon.com/rocm/windows/rocm-rel-7.1.1/",
        "torch": "torch-2.9.0+rocmsdk20251116-cp312-cp312-win_amd64.whl",
        "torchaudio": "torchaudio-2.9.0+rocmsdk20251116-cp312-cp312-win_amd64.whl",
        "torchvision": "torchvision-0.24.0+rocmsdk20251116-cp312-cp312-win_amd64.whl",
        "rocm_sdk_core": "rocm_sdk_core-0.1.dev0-py3-none-win_amd64.whl",
        "rocm_sdk_devel": "rocm_sdk_devel-0.1.dev0-py3-none-win_amd64.whl",
        "rocm_sdk_libraries_custom": "rocm_sdk_libraries_custom-0.1.dev0-py3-none-win_amd64.whl",
        "rocm_tarball": "rocm-0.1.dev0.tar.gz",
        "pytorch_version": "2.9.0",
        "torchvision_version": "0.24.0",
        "torchaudio_version": "2.9.0",
        "driver_required": "N/A",
        "type": "stable",
        "os": "Windows",
        "python_versions": ["py312"],
    },
    {
        "label": "6.4.4",
        "rocm_rel": "6.4.4",
        "base_url": "https://repo.radeon.com/rocm/windows/rocm-rel-6.4.4/",
        "torch": "torch-2.8.0a0+gitfc14c65-cp312-cp312-win_amd64.whl",
        "torchaudio": "",
        "torchvision": "torchvision-0.24.0a0+c85f008-cp312-cp312-win_amd64.whl",
        "rocm_sdk_core": "",
        "rocm_sdk_devel": "",
        "rocm_sdk_libraries_custom": "",
        "rocm_tarball": "",
        "pytorch_version": "2.8.0a0",
        "torchvision_version": "0.24.0a0",
        "torchaudio_version": "N/A",
        "driver_required": "N/A",
        "type": "stable",
        "os": "Windows",
        "python_versions": ["py312"],
    },
]

NIGHTLY_VERSIONS = [
    {
        "pytorch": "2.12.0a0",
        "torchvision": "0.26.0a0",
        "torchaudio": "2.12.0a0",
        "type": "nightly",
        "label": "2.12-nightly",
        "rocm_suffix": "7.13.0a20260426",
        "python_versions": ["py311", "py312", "py313"],
        "notes": "May be unstable",
    },
    {
        "pytorch": "2.11",
        "torchvision": "0.25",
        "torchaudio": "2.11",
        "type": "stable",
        "label": "2.11",
        "rocm_suffix": "7.13.0a20260426",
        "python_versions": ["py311", "py312", "py313"],
        "notes": "",
    },
    {
        "pytorch": "2.10",
        "torchvision": "0.25",
        "torchaudio": "2.10",
        "type": "stable",
        "label": "2.10",
        "rocm_suffix": "7.12.0",
        "python_versions": ["py311", "py312", "py313"],
        "notes": "",
    },
    {
        "pytorch": "2.9",
        "torchvision": "0.24",
        "torchaudio": "2.9",
        "type": "stable",
        "label": "2.9",
        "rocm_suffix": "7.12.0",
        "python_versions": ["py311", "py312", "py313"],
        "notes": "",
    },
]


def get_stable_releases() -> list:
    return STABLE_RELEASES


def get_nightly_versions() -> list:
    return NIGHTLY_VERSIONS


def get_release_by_label(label: str) -> Optional[dict]:
    for rel in STABLE_RELEASES + NIGHTLY_VERSIONS:
        if rel.get("label") == label:
            return rel
    return None


def get_latest_nightly() -> Optional[dict]:
    if NIGHTLY_VERSIONS:
        return NIGHTLY_VERSIONS[0]
    return None


def filter_stable_by_os(os_name: str) -> list:
    return [r for r in STABLE_RELEASES if r.get("os", "").lower() == os_name.lower()]


def filter_nightly_by_python(py_tag: str) -> list:
    return [v for v in NIGHTLY_VERSIONS if py_tag in v.get("python_versions", [])]
