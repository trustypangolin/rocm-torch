import json
from pathlib import Path
from typing import List, Optional

_CURATED_DIR = Path(__file__).parent.parent / "curated"


def _load_json(name: str) -> list:
    with open(_CURATED_DIR / name, encoding="utf-8") as f:
        return json.load(f)


STABLE_RELEASES = _load_json("stable_releases.json")

_LATEST_PATH = _CURATED_DIR / "latest_versions.json"
if _LATEST_PATH.exists():
    LATEST_VERSIONS = _load_json("latest_versions.json")
else:
    LATEST_VERSIONS = _load_json("nightly_versions.json")


def get_stable_releases() -> list:
    return STABLE_RELEASES


def get_nightly_versions() -> list:
    return LATEST_VERSIONS


def get_release_by_label(label: str) -> Optional[dict]:
    for rel in STABLE_RELEASES + LATEST_VERSIONS:
        if rel.get("label") == label:
            return rel
    return None


def get_latest_nightly() -> Optional[dict]:
    if LATEST_VERSIONS:
        return LATEST_VERSIONS[0]
    return None


def filter_stable_by_os(os_name: str) -> list:
    return [r for r in STABLE_RELEASES if r.get("os", "").lower() == os_name.lower()]


def filter_nightly_by_python(py_tag: str) -> list:
    return [v for v in LATEST_VERSIONS if py_tag in v.get("python_versions", [])]
