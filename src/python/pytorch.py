from typing import Optional

PYTORCH_MATRIX = [
    {
        "version": "2.12a",
        "type": "nightly",
        "python_versions": ["3.11", "3.12", "3.13"],
        "os_support": "win,linux",
        "notes": "May be unstable",
    },
    {
        "version": "2.11",
        "type": "stable",
        "python_versions": ["3.11", "3.12", "3.13"],
        "os_support": "win,linux",
        "notes": "",
    },
    {
        "version": "2.10",
        "type": "stable",
        "python_versions": ["3.11", "3.12", "3.13"],
        "os_support": "win,linux",
        "notes": "",
    },
    {
        "version": "2.9",
        "type": "stable",
        "python_versions": ["3.11", "3.12", "3.13"],
        "os_support": "win,linux",
        "notes": "",
    },
]


def get_pytorch_compat(version: str) -> Optional[dict]:
    base = version.rstrip("a").replace(".0a0", "")
    for entry in PYTORCH_MATRIX:
        entry_base = entry["version"].rstrip("a")
        if entry_base == base:
            return entry
    return None


def validate_pytorch_version(version: str, python_version: str, os_name: str) -> bool:
    compat = get_pytorch_compat(version)
    if not compat:
        return False
    os_lower = compat["os_support"].lower()
    if "win" not in os_lower and "linux" not in os_lower:
        return False
    return python_version in compat["python_versions"]


def get_pytorch_version_for_rocm(rocm_version: str) -> str:
    mapping = {
        "7.2": "2.9.1",
        "7.1": "2.9.0",
        "6.4": "2.8.0a0",
        "7.13": "2.12.0a0",
        "7.12": "2.11",
    }
    for prefix, pt_version in mapping.items():
        if rocm_version.startswith(prefix):
            return pt_version
    return "2.11"


def get_pytorch_display_table() -> dict:
    headers = ["Version", "Type", "Python", "OS", "Notes"]
    rows = []
    for entry in PYTORCH_MATRIX:
        rows.append(
            [
                entry["version"],
                entry["type"],
                ", ".join(entry["python_versions"]),
                entry["os_support"],
                entry["notes"],
            ]
        )
    return {"headers": headers, "rows": rows}
