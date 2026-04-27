# PowerShell Modules - `src/powershell/`

## Overview
This directory contains PowerShell modules (`.psm1` files) for the ROCm + PyTorch requirements generator. Each module handles a single concern and is imported by the main script (`generate-requirements.ps1` at project root).

## Module Structure

| File | Purpose | Lines (est.) |
|------|---------|-------------|
| `OS.psm1` | OS target definitions and validation | ~60 |
| `Python.psm1` | Python version matrix and helpers | ~80 |
| `ROCm.psm1` | ROCm release definitions (stable + nightly) | ~150 |
| `PyTorch.psm1` | PyTorch compatibility matrix | ~70 |
| `Menu.psm1` | Interactive menu system | ~200 |
| `Generator.psm1` | Requirements file generation logic | ~120 |
| `Utils.psm1` | Shared utilities (logging, validation, etc.) | ~100 |

## Import Pattern
Main script imports all modules using `$PSScriptRoot`-relative paths:
```powershell
$ModulePath = Join-Path $PSScriptRoot "src\powershell"
Import-Module (Join-Path $ModulePath "Utils.psm1")
# ... import other modules
```

## Design Principles
- **No cross-module imports** (except Utils) - main script orchestrates everything
- **Functions return data**, not print output (keeps them testable)
- **Data is hardcoded** in the modules (not fetched at runtime) for reliability
- **Consistent naming** - PascalCase for PowerShell functions, `Get-`/`Validate-`/`Show-` prefixes

## Module Details

### OS.psm1
OS target configurations and validation.

**Data**: `$OSTargets` hashtable mapping `Windows`/`Linux` to platform configs (tag, platform wheel tag, index URL, stable base URL).

**Functions**:
- `Get-OSTarget` - Look up OS config by name
- `Validate-OS` - Validate OS + release type combination (reject Linux + stable)
- `Get-AllOSTargets` - Return all available OS targets
- `Get-OSDisplayName` - Human-readable OS name for menus

### Python.psm1
Python version matrix and helpers.

**Data**: `$PythonVersions` array of version definitions (major, minor, tag, cp_tag, supported, notes).

**Functions**:
- `Get-PythonVersions` - Parse user selection and return matching version tags
- `Get-CurrentPythonVersion` - Detect running Python version
- `Validate-PythonForRelease` - Check if Python version is supported by a release
- `Get-PythonDisplayString` - Format version range for menus
- `Get-PythonTagFromVersion` - Convert "3.12" → "py312"

### ROCm.psm1
ROCm release definitions - the most frequently updated module.

**Data**:
- `$StableReleases` - Array of stable release configs (wheel URLs, driver requirements, Python support)
- `$NightlyVersions` - Array of nightly version configs (PyTorch versions, ROCm suffixes, Python support)

**Functions**:
- `Get-StableReleases` - Return all stable releases
- `Get-NightlyVersions` - Return all nightly versions
- `Get-ReleaseByLabel` - Look up release by label
- `Get-LatestNightly` - Return the top/nightly entry
- `Filter-StableByOS` - Filter stable releases by OS compatibility
- `Filter-NightlyByPython` - Filter nightly versions by Python support

### PyTorch.psm1
PyTorch version compatibility matrix.

**Data**: `$PyTorchMatrix` - Array mapping PyTorch versions to supported Python versions, OS support, and stability notes.

**Functions**:
- `Get-PyTorchCompat` - Get compatibility info for a PyTorch version
- `Validate-PyTorchVersion` - Validate PyTorch + Python + OS combination
- `Get-PyTorchVersionForROCm` - Map ROCm version to PyTorch version
- `Get-PyTorchDisplayTable` - Format compatibility table for menus

### Menu.psm1
Interactive menu system - the UI layer.

**Functions**:
- `Show-OSMenu` - Display OS target options, return selected
- `Show-PythonMenu` - Display Python version options, return selected
- `Show-StableMenu` - Display stable releases with driver requirements
- `Show-NightlyMenu` - Display nightly versions with stability notes
- `Show-FullMenu` - Combined table of all options
- `Read-UserChoice` - Generic input validation helper
- `Show-OutputSummary` - Display generated files table

### Generator.psm1
Requirements file generation logic.

**Functions**:
- `Generate-IndexBased` - Generate content for nightly/index-based installs
- `Generate-DirectURL` - Generate content for stable/direct-URL installs
- `Write-RequirementsFile` - Write content to file with overwrite handling
- `Get-OutputFileName` - Build output file path from naming convention
- `Generate-AllForSelection` - Orchestrate file generation for a set of options

### Utils.psm1
Shared utilities used across modules.

**Functions**:
- `Write-Log` - Colored console output with timestamp (INFO/WARN/ERROR/SUCCESS)
- `Test-Network` - Check if URL is reachable
- `Confirm-Overwrite` - Prompt user if file exists
- `Validate-DriverVersion` - Windows: check installed AMD driver version
- `Test-AdminPrivileges` - Check if running as admin
- `Format-Table` - Pretty-print tables for console output
