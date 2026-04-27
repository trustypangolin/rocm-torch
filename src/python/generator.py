from pathlib import Path
from typing import Optional

from utils import write_log, confirm_overwrite


def generate_index_based(entry: dict, py_tag: str) -> str:
    pre_flag = "--pre\n" if entry["pytorch"].endswith("a0") else ""
    return (
        f"--index-url https://rocm.nightlies.amd.com/v2/gfx1151/\n"
        f"{pre_flag}"
        f"torch=={entry['pytorch']}+rocm{entry['rocm_suffix']}\n"
        f"torchvision=={entry['torchvision']}+rocm{entry['rocm_suffix']}\n"
        f"torchaudio=={entry['torchaudio']}+rocm{entry['rocm_suffix']}\n"
        f"rocm=={entry['rocm_suffix']}\n"
        f"rocm-sdk-core=={entry['rocm_suffix']}\n"
        f"rocm-sdk-libraries-gfx1151=={entry['rocm_suffix']}"
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
    label = entry["label"]
    is_direct_stable = entry.get("type") == "stable" and "driver_required" in entry
    if is_direct_stable:
        base_name = f"requirements-{label}-stable-{os_tag}-{py_tag}.txt"
    else:
        type_suffix = "-nightly" if entry.get("type") == "nightly" else ""
        base_name = f"requirements-{label}{type_suffix}-{py_tag}.txt"
    if output_dir and output_dir != ".":
        return str(Path(output_dir) / base_name)
    return base_name


def write_requirements_file(
    content: str, file_path: str, dry_run: bool = False
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
        if not confirm_overwrite(file_path):
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
            result = write_requirements_file(content, file_path, dry_run)
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
                result = write_requirements_file(content, file_path, dry_run)
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
