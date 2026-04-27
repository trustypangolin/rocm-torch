import json
from pathlib import Path
from typing import List, Optional

_CURATED_DIR = Path(__file__).parent.parent / "curated"


def _load_json(name: str) -> list:
    with open(_CURATED_DIR / name, encoding="utf-8") as f:
        return json.load(f)


STABLE_RELEASES = _load_json("stable_releases.json")
NIGHTLY_VERSIONS = _load_json("nightly_versions.json")


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
