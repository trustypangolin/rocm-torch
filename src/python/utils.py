import logging
import sys
import platform
from pathlib import Path
from typing import Tuple

try:
    import urllib.request

    HAS_URLLIB = True
except ImportError:
    HAS_URLLIB = False

logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def write_log(message: str, level: str = "INFO") -> None:
    colors = {
        "INFO": "\033[97m",
        "WARN": "\033[93m",
        "ERROR": "\033[91m",
        "SUCCESS": "\033[92m",
    }
    reset = "\033[0m"
    color = colors.get(level, "")
    print(f"{color}[{level}] {message}{reset}")


def test_network(url: str) -> bool:
    if not HAS_URLLIB:
        return False
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception:
        return False


def confirm_overwrite(file_path: str) -> bool:
    if Path(file_path).exists():
        choice = input(f"File '{file_path}' already exists. Overwrite? (y/n): ")
        return choice.lower() == "y"
    return True


def validate_driver_version(required_version: str) -> Tuple[bool, str]:
    if required_version == "N/A":
        return (True, "No driver version required")
    if platform.system() != "Windows":
        return (False, "Driver check only available on Windows")
    try:
        import subprocess

        result = subprocess.run(
            ["wmic", "path", "Win32_VideoController", "get", "DriverVersion"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            return (False, "Could not query driver version")
        lines = result.stdout.strip().split("\n")
        if len(lines) < 2:
            return (False, "No driver version found")
        installed = lines[1].strip()
        required_parts = [int(x) for x in required_version.split(".")]
        actual_parts = [int(x) for x in installed.split(".")]
        for i in range(min(len(required_parts), len(actual_parts))):
            if actual_parts[i] > required_parts[i]:
                return (True, f"Driver {installed} >= {required_version}")
            if actual_parts[i] < required_parts[i]:
                return (False, f"Driver {installed} < {required_version}")
        return (True, f"Driver {installed} matches {required_version}")
    except Exception as e:
        return (False, f"Could not check driver version: {e}")


def test_admin_privileges() -> bool:
    if platform.system() == "Windows":
        import ctypes

        try:
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        except Exception:
            return False
    else:
        import os

        return os.geteuid() == 0


def format_table(headers: list, rows: list) -> str:
    if not rows:
        return ""
    col_widths = []
    for i in range(len(headers)):
        max_w = len(headers[i])
        for row in rows:
            val = str(row[i])
            if len(val) > max_w:
                max_w = len(val)
        col_widths.append(max_w)
    lines = []
    header_line = " ".join(
        f"{headers[i]:<{col_widths[i]}}" for i in range(len(headers))
    )
    lines.append(header_line)
    sep_line = " ".join("-" * col_widths[i] for i in range(len(headers)))
    lines.append(sep_line)
    for row in rows:
        line = " ".join(f"{str(row[i]):<{col_widths[i]}}" for i in range(len(headers)))
        lines.append(line)
    return "\n".join(lines)
