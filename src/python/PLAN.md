# Python Modules - `src/python/`

## Overview
This directory contains Python modules (`.py` files) for the ROCm + PyTorch requirements generator. Each module handles a single concern and is imported by the main script (`generate_requirements.py` at project root).

## Module Structure

| File | Purpose | Lines (est.) |
|------|---------|-------------|
| `os_target.py` | OS target definitions and validation | ~60 |
| `python_version.py` | Python version matrix and helpers | ~80 |
| `rocm.py` | ROCm release definitions (stable + nightly) | ~150 |
| `pytorch.py` | PyTorch compatibility matrix | ~70 |
| `menu.py` | Interactive menu system | ~200 |
| `generator.py` | Requirements file generation logic | ~120 |
| `utils.py` | Shared utilities (logging, validation, etc.) | ~100 |

## Import Pattern
Main script adds `src/python` to `sys.path` and imports all modules:
```python
sys.path.insert(0, str(Path(__file__).parent / "src" / "python"))
from utils import *
from os_target import *
# ... import other modules
```

## Design Principles
- **No cross-module imports** (except utils) - main script orchestrates everything
- **Functions return data**, not print output (keeps them testable)
- **Data is hardcoded** in modules (not fetched at runtime) for reliability
- **Consistent naming** - snake_case for Python, type hints on all functions
- **Dataclasses where appropriate** for structured data (optional, dicts also fine)

## Module Details

### os_target.py
OS target configurations and validation.

**Data**: `OS_TARGETS` dict mapping `windows`/`linux` to platform configs (tag, platform wheel tag, index URL, stable base URL).

**Functions**:
- `get_os_target(name: str) -> dict` - Look up OS config by name
- `validate_os(os_name: str, release_type: str) -> bool` - Validate OS + release type (reject linux + stable)
- `get_all_os_targets() -> dict` - Return all available OS targets
- `get_os_display_name(os_name: str) -> str` - Human-readable OS name for menus

### python_version.py
Python version matrix and helpers.

**Data**: `PYTHON_VERSIONS` list of version dicts (major, minor, tag, cp_tag, supported, notes).

**Functions**:
- `get_python_versions(selection: str) -> list` - Parse user selection and return matching version tags
- `get_current_python_version() -> str` - Detect running Python version via `sys.version_info`
- `validate_python_for_release(py_tag: str, supported_versions: list) -> bool` - Check if Python version is supported by a release
- `get_python_display_string(versions: list) -> str` - Format version range for menus (e.g., "3.11-3.13")
- `get_python_tag_from_version(version: str) -> str` - Convert "3.12" → "py312"

### rocm.py
ROCm release definitions - the most frequently updated module.

**Data**:
- `STABLE_RELEASES` - List of stable release dicts (wheel URLs, driver requirements, Python support)
- `NIGHTLY_VERSIONS` - List of nightly version dicts (PyTorch versions, ROCm suffixes, Python support)

**Functions**:
- `get_stable_releases() -> list` - Return all stable releases
- `get_nightly_versions() -> list` - Return all nightly versions
- `get_release_by_label(label: str) -> dict | None` - Look up release by label
- `get_latest_nightly() -> dict` - Return the top/nightly entry
- `filter_stable_by_os(os_name: str) -> list` - Filter stable releases by OS compatibility
- `filter_nightly_by_python(py_tag: str) -> list` - Filter nightly versions by Python support

### pytorch.py
PyTorch version compatibility matrix.

**Data**: `PYTORCH_MATRIX` - List of dicts mapping PyTorch versions to supported Python versions, OS support, and stability notes.

**Functions**:
- `get_pytorch_compat(version: str) -> dict | None` - Get compatibility info for a PyTorch version
- `validate_pytorch_version(version: str, python_version: str, os_name: str) -> bool` - Validate combination
- `get_pytorch_version_for_rocm(rocm_version: str) -> str` - Map ROCm version to PyTorch version
- `get_pytorch_display_table() -> str` - Format compatibility table for menus

### menu.py
Interactive menu system - the UI layer.

**Functions**:
- `show_os_menu() -> str` - Display OS target options, return selected
- `show_python_menu() -> str` - Display Python version options, return selected
- `show_stable_menu() -> dict` - Display stable releases with driver requirements
- `show_nightly_menu() -> dict` - Display nightly versions with stability notes
- `show_full_menu() -> dict` - Combined table of all options
- `read_user_choice(prompt: str, valid_choices: list) -> str` - Generic input validation helper
- `show_output_summary(files: list)` - Display generated files table

### generator.py
Requirements file generation logic.

**Functions**:
- `generate_index_based(entry: dict, py_tag: str) -> str` - Generate content for nightly/index-based installs
- `generate_direct_url(entry: dict, py_tag: str, os_tag: str) -> str` - Generate content for stable/direct-URL installs
- `write_requirements_file(content: str, file_path: str, dry_run: bool = False) -> bool` - Write content to file
- `get_output_file_name(entry: dict, py_tag: str, os_tag: str, output_dir: str) -> str` - Build output file path
- `generate_all_for_selection(entry: dict, py_tags: list, os_tags: list, output_dir: str, dry_run: bool) -> list` - Orchestrate file generation

### utils.py
Shared utilities used across modules.

**Functions**:
- `setup_logging(verbose: bool = False)` - Configure logging
- `write_log(message: str, level: str = "INFO")` - Colored console output with timestamp
- `test_network(url: str) -> bool` - Check if URL is reachable (uses `urllib` or `requests`)
- `confirm_overwrite(file_path: str) -> bool` - Prompt user if file exists
- `validate_driver_version(required_version: str) -> tuple[bool, str]` - Windows: check installed AMD driver version
- `test_admin_privileges() -> bool` - Check if running as admin
- `format_table(headers: list, rows: list) -> str` - Pretty-print tables for console output
