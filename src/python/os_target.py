from typing import Optional

OS_TARGETS = {
    "Windows": {
        "tag": "win",
        "platform": "win_amd64",
        "index_base": "https://rocm.nightlies.amd.com/v2/gfx1151/",
        "stable_base": "https://repo.radeon.com/rocm/windows/rocm-rel-{0}/",
    },
    "Linux": {
        "tag": "linux",
        "platform": "linux_x86_64",
        "index_base": "https://rocm.nightlies.amd.com/v2/gfx1151/",
        "stable_base": None,
    },
}


def get_os_target(name: str) -> Optional[dict]:
    normalized = name.capitalize()
    return OS_TARGETS.get(normalized)


def validate_os(os_name: str, release_type: str) -> bool:
    if release_type == "stable" and os_name.lower() == "linux":
        return False
    return os_name.capitalize() in OS_TARGETS


def get_all_os_targets() -> dict:
    return OS_TARGETS


def get_os_display_name(os_name: str) -> str:
    names = {
        "windows": "Windows",
        "linux": "Linux (Debian/Ubuntu)",
    }
    return names.get(os_name.lower(), os_name)
