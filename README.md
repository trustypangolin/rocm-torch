# ROCm + PyTorch Requirements Generator

Generate `requirements-*.txt` files for multiple PyTorch + ROCm + Python version combinations, targeting Windows or Linux (Debian/Ubuntu).

## Quick Start

### PowerShell (Windows)
```powershell
.\generate-requirements.ps1
```

### Python (Cross-platform)
```bash
python generate_requirements.py
```

Both scripts provide the same functionality with an identical interactive menu flow.

## Architecture

```
generate-requirements.ps1          # PowerShell entry point
generate_requirements.py           # Python entry point
src/
├── powershell/
│   ├── Utils.psm1                 # Logging, validation, table formatting
│   ├── OS.psm1                    # OS target definitions (Windows/Linux)
│   ├── Python.psm1                # Python version matrix
│   ├── ROCm.psm1                  # Stable + nightly release data
│   ├── PyTorch.psm1               # PyTorch compatibility matrix
│   ├── Menu.psm1                  # Interactive menu system
│   └── Generator.psm1             # Requirements file generation
└── python/
    ├── utils.py                   # Logging, validation, table formatting
    ├── os_target.py               # OS target definitions
    ├── python_version.py          # Python version matrix
    ├── rocm.py                    # Stable + nightly release data
    ├── pytorch.py                 # PyTorch compatibility matrix
    ├── menu.py                    # Interactive menu system
    └── generator.py               # Requirements file generation
```

## Interactive Mode (Default)

Run either script without arguments to walk through the menu:

```
1. Target OS: Windows, Linux, or Both
2. Python version(s): 3.11, 3.12, 3.13, 3.14, all, or current
3. Use stable releases? (requires matching AMD driver, Windows + Python 3.12 only)
4. Use latest nightly? Or select from full version table
```

## Non-Interactive Mode

### PowerShell
```powershell
# Generate all files for Windows + Python 3.12
.\generate-requirements.ps1 -NonInteractive -OSTarget windows -PythonVersion 3.12

# Generate only stable releases
.\generate-requirements.ps1 -NonInteractive -StableOnly

# Generate only nightly releases for all supported Python versions
.\generate-requirements.ps1 -NonInteractive -NightlyOnly -PythonVersion all

# Preview without writing files
.\generate-requirements.ps1 -NonInteractive -DryRun

# Generate everything for both OSes
.\generate-requirements.ps1 -NonInteractive -OSTarget both -PythonVersion all
```

### Python
```bash
# Generate all files for Windows + Python 3.12
python generate_requirements.py --non-interactive --os-target windows --python-version 3.12

# Generate only stable releases
python generate_requirements.py --non-interactive --stable-only

# Generate only nightly releases for all supported Python versions
python generate_requirements.py --non-interactive --nightly-only --python-version all

# Preview without writing files
python generate_requirements.py --non-interactive --dry-run

# Generate everything for both OSes
python generate_requirements.py --non-interactive --os-target both --python-version all

# Verbose logging
python generate_requirements.py --non-interactive --verbose
```

## Parameters

| Parameter | PowerShell | Python | Default | Description |
|-----------|-----------|--------|---------|-------------|
| Output directory | `-OutputDir` | `--output-dir` | `.` | Where to write requirements files |
| OS target | `-OSTarget` | `--os-target` | `windows` | `windows`, `linux`, or `both` |
| Python version | `-PythonVersion` | `--python-version` | `3.12` | `3.11`, `3.12`, `3.13`, `3.14`, `all` |
| Non-interactive | `-NonInteractive` | `--non-interactive` | - | Skip prompts, generate all |
| Stable only | `-StableOnly` | `--stable-only` | - | Only stable releases |
| Nightly only | `-NightlyOnly` | `--nightly-only` | - | Only nightly releases |
| Dry run | `-DryRun` | `--dry-run` | - | Preview without writing |
| Verbose | N/A | `--verbose` | - | Enable debug logging (Python only) |

## Install Methods

### Index-based (Nightly / Cross-OS)
Uses `--index-url https://rocm.nightlies.amd.com/v2/gfx1151/` — pip auto-selects the correct wheel for your OS and Python version. A single file works on both Windows and Linux.

```
--index-url https://rocm.nightlies.amd.com/v2/gfx1151/
--pre
torch==2.12.0a0+rocm7.13.0a20260426
torchvision==0.26.0a0+rocm7.13.0a20260426
torchaudio==2.12.0a0+rocm7.13.0a20260426
rocm==7.13.0a20260426
rocm-sdk-core==7.13.0a20260426
rocm-sdk-libraries-gfx1151==7.13.0a20260426
```

### Direct URL (Stable / Windows Only)
Uses explicit wheel URLs from `repo.radeon.com`. Windows + Python 3.12 only, requires matching AMD driver.

```
# ROCm SDK (install first)
https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/rocm_sdk_core-7.2.1-py3-none-win_amd64.whl
...
# PyTorch packages
https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/torch-2.9.1+rocm7.2.1-cp312-cp312-win_amd64.whl
...
```

## Supported Versions

### Nightly (via index-url)
| PyTorch | Python | OS | Notes |
|---------|--------|----|-------|
| 2.12a | 3.11-3.13 | Win, Linux | May be unstable |
| 2.11 | 3.11-3.13 | Win, Linux | |
| 2.10 | 3.11-3.13 | Win, Linux | |
| 2.9 | 3.11-3.13 | Win, Linux | |

### Stable (direct URL)
| Release | PyTorch | Driver | OS | Python |
|---------|---------|--------|----|--------|
| 7.2.1 | 2.9.1 | 26.2.2 | Windows | 3.12 |
| 7.2 | 2.9.1 | 26.1.1 | Windows | 3.12 |
| 7.1.1 | 2.9.0 | N/A | Windows | 3.12 |
| 6.4.4 | 2.8.0a0 | N/A | Windows | 3.12 |

## Updating

To add a new nightly release, append to the `$NightlyVersions` array in `src/powershell/ROCm.psm1` (or `NIGHTLY_VERSIONS` in `src/python/rocm.py`):

```powershell
@{ PyTorch = "2.13"; Torchvision = "0.26"; Torchaudio = "2.13"; Type = "stable"; Label = "2.13"; RocmSuffix = "7.14.0"; PythonVersions = @("py311","py312","py313"); Notes = "" }
```
