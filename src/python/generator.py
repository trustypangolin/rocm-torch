from pathlib import Path
from typing import Optional

from utils import write_log, confirm_overwrite


def generate_index_based(entry: dict, py_tag: str) -> str:
    pre_flag = "--pre\n" if entry["pytorch"].endswith("a0") else ""
    suffix = entry["rocm_suffix"]
    return (
        f"--index-url https://rocm.nightlies.amd.com/v2/gfx1151/\n"
        f"{pre_flag}"
        f"torch=={entry['pytorch']}+rocm{suffix}\n"
        f"torchvision=={entry['torchvision']}\n"
        f"torchaudio=={entry['torchaudio']}\n"
        f"rocm=={suffix}\n"
        f"rocm-sdk-core=={suffix}\n"
        f"rocm-sdk-devel=={suffix}\n"
        f"rocm-sdk-libraries-gfx1151=={suffix}"
    ).strip()


def generate_direct_url(entry: dict, py_tag: str, os_tag: str) -> Optional[str]:
    if py_tag != "py312":
        return None
    base_url = entry["base_url"]
    lines = ["# ROCm SDK (install first)"]
    for key in [
        "rocm_sdk_core",
        "rocm_sdk_devel",
        "rocm_sdk_libraries_custom",
        "rocm_tarball",
    ]:
        val = entry.get(key, "")
        if val:
            lines.append(f"{base_url}{val}")
    lines.append("")
    lines.append("# PyTorch packages")
    for key in ["torch", "torchaudio", "torchvision"]:
        val = entry.get(key, "")
        if val:
            lines.append(f"{base_url}{val}")
    return "\n".join(lines).strip()


def get_output_file_name(entry: dict, py_tag: str, os_tag: str, output_dir: str) -> str:
    is_direct_stable = entry.get("type") == "stable" and "driver_required" in entry
    if is_direct_stable:
        rocm_ver = entry.get("rocm_rel", "unknown")
        py_ver = _format_python_version(py_tag)
        base_name = f"requirements-stable-win-{rocm_ver}-{py_ver}.txt"
    else:
        rocm_suffix = entry.get("rocm_suffix", "unknown")
        rocm_ver = _extract_rocm_major(rocm_suffix)
        torch_ver = _extract_torch_version(entry.get("pytorch", "unknown"))
        rev_date = _extract_revision_date(rocm_suffix)
        base_name = f"requirements-nightly-win-rocm{rocm_ver}-torch{torch_ver}-{rev_date}-{py_tag}.txt"
    if output_dir and output_dir != ".":
        return str(Path(output_dir) / base_name)
    return base_name


def _extract_rocm_major(rocm_suffix: str) -> str:
    if "a" in rocm_suffix:
        parts = rocm_suffix.split("a")
        base = parts[0].rstrip(".")
        dot_parts = base.split(".")
        if len(dot_parts) >= 2:
            return f"{dot_parts[0]}.{dot_parts[1]}"
        return base
    return rocm_suffix


def _format_python_version(py_tag: str) -> str:
    digits = py_tag.replace("py", "")
    if len(digits) >= 3:
        return f"{digits[0]}.{digits[1:]}"
    return digits


def _extract_torch_version(version: str) -> str:
    if version.endswith("a0"):
        return version[:-2]
    return version


def _extract_revision_date(rocm_suffix: str) -> str:
    idx = rocm_suffix.find("a")
    if idx == -1:
        return rocm_suffix
    return rocm_suffix[idx:]


def write_requirements_file(
    content: str, file_path: str, dry_run: bool = False, auto_overwrite: bool = False
) -> bool:
    if dry_run:
        print(f"[DRY RUN] Would write: {file_path}")
        print("---")
        print(content)
        print("---")
        return True
    path = Path(file_path)
    if path.parent and str(path.parent) != ".":
        path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if auto_overwrite or confirm_overwrite(file_path):
            pass
        else:
            write_log(f"Skipping: {file_path}", "WARN")
            return False
    path.write_text(content, encoding="utf-8")
    write_log(f"Written: {file_path}", "SUCCESS")
    return True


def generate_all_for_selection(
    entry: dict,
    py_tags: list,
    os_tags: list,
    output_dir: str,
    dry_run: bool = False,
    auto_overwrite: bool = False,
) -> list:
    from os_target import get_os_target

    generated = []
    for py_tag in py_tags:
        supported = entry.get("python_versions", [])
        if supported and py_tag not in supported:
            write_log(
                f"{entry['label']} does not support Python {py_tag}, skipping", "WARN"
            )
            continue
        is_direct_stable = entry.get("type") == "stable" and "driver_required" in entry
        if is_direct_stable:
            if "linux" in [t.lower() for t in os_tags]:
                write_log(
                    f"Stable release {entry['label']} is Windows only, skipping Linux",
                    "WARN",
                )
            if py_tag != "py312":
                write_log(
                    f"Stable release {entry['label']} only supports Python 3.12, skipping {py_tag}",
                    "WARN",
                )
                continue
            os_tag = "win"
            file_path = get_output_file_name(entry, py_tag, os_tag, output_dir)
            content = generate_direct_url(entry, py_tag, os_tag)
            if content is None:
                continue
            result = write_requirements_file(
                content, file_path, dry_run, auto_overwrite
            )
            if result:
                driver = entry.get("driver_required", "N/A")
                note = f"Requires driver {driver}" if driver != "N/A" else ""
                generated.append(
                    {
                        "file": Path(file_path).name,
                        "pytorch": entry.get("pytorch_version", ""),
                        "torchvision": entry.get("torchvision_version", ""),
                        "torchaudio": entry.get("torchaudio_version", ""),
                        "rocm": entry.get("rocm_rel", ""),
                        "os": "Windows",
                        "python": py_tag.replace("py", ""),
                        "notes": note,
                    }
                )
        else:
            for os_name in os_tags:
                os_info = get_os_target(os_name)
                if not os_info:
                    continue
                os_tag = os_info["tag"]
                file_path = get_output_file_name(entry, py_tag, os_tag, output_dir)
                content = generate_index_based(entry, py_tag)
                result = write_requirements_file(
                    content, file_path, dry_run, auto_overwrite
                )
                if result:
                    generated.append(
                        {
                            "file": Path(file_path).name,
                            "pytorch": entry.get("pytorch", ""),
                            "torchvision": entry.get("torchvision", ""),
                            "torchaudio": entry.get("torchaudio", ""),
                            "rocm": entry.get("rocm_suffix", ""),
                            "os": "Cross-OS (index)",
                            "python": py_tag.replace("py", ""),
                            "notes": entry.get("notes", ""),
                        }
                    )
    return generated
