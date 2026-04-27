from typing import List, Optional
import sys

PYTHON_VERSIONS = [
    {
        "major": 3,
        "minor": 11,
        "tag": "py311",
        "cp_tag": "cp311",
        "supported": True,
        "notes": "Stable support",
    },
    {
        "major": 3,
        "minor": 12,
        "tag": "py312",
        "cp_tag": "cp312",
        "supported": True,
        "notes": "Recommended",
    },
    {
        "major": 3,
        "minor": 13,
        "tag": "py313",
        "cp_tag": "cp313",
        "supported": True,
        "notes": "",
    },
    {
        "major": 3,
        "minor": 14,
        "tag": "py314",
        "cp_tag": "cp314",
        "supported": False,
        "notes": "Experimental, limited availability",
    },
]


def get_python_versions(selection: str) -> List[str]:
    mapping = {
        "3.11": ["py311"],
        "3.12": ["py312"],
        "3.13": ["py313"],
        "3.14": ["py314"],
        "all": ["py311", "py312", "py313"],
    }
    if selection.lower() == "current":
        tag = get_current_python_version()
        return [tag]
    return mapping.get(selection.lower(), ["py312"])


def get_current_python_version() -> str:
    major = sys.version_info.major
    minor = sys.version_info.minor
    return f"py{major}{minor}"


def validate_python_for_release(py_tag: str, supported_versions: list) -> bool:
    return py_tag in supported_versions


def get_python_display_string(versions: list) -> str:
    if not versions:
        return "None"
    if len(versions) == 1:
        return versions[0].replace("py", "3.")
    first = versions[0].replace("py", "3.")[:3]
    last = versions[-1].replace("py", "3.")[:3]
    return f"{first}-{last}"


def get_python_tag_from_version(version: str) -> str:
    normalized = version.replace(".", "")
    return f"py{normalized}"
