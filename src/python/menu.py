def read_user_choice(prompt: str, valid_choices: list) -> str:
    while True:
        choice = input(f"{prompt}: ").strip().lower()
        valid_lower = [str(v).lower() for v in valid_choices]
        if choice in valid_lower:
            return choice
        print(
            f"Invalid choice. Valid options: {', '.join(str(v) for v in valid_choices)}"
        )


def show_os_menu() -> str:
    print("\nTarget OS:")
    print("  [1] Windows (default)")
    print("  [2] Linux (Debian/Ubuntu)")
    print("  [3] Both (generate for each)")
    choice = read_user_choice("Enter choice", ["1", "2", "3"])
    mapping = {"1": "windows", "2": "linux", "3": "both"}
    return mapping.get(choice, "windows")


def show_python_menu() -> str:
    print("\nPython version(s) to generate for:")
    print("  [1] 3.11 (stable support)")
    print("  [2] 3.12 (recommended)")
    print("  [3] 3.13")
    print("  [4] 3.14 (experimental)")
    print("  [a] All supported (3.11-3.13)")
    print("  [c] Current Python version")
    choice = read_user_choice("Enter choice", ["1", "2", "3", "4", "a", "c"])
    mapping = {
        "1": "3.11",
        "2": "3.12",
        "3": "3.13",
        "4": "3.14",
        "a": "all",
        "c": "current",
    }
    return mapping.get(choice, "3.12")


def show_stable_menu() -> bool:
    print("\nUse supported stable releases from repo.radeon.com? (y/n)")
    print("These require matching AMD Adrenalin driver versions.")
    print("Note: Stable is Windows + Python 3.12 only.")
    choice = read_user_choice("Enter choice", ["y", "n"])
    return choice == "y"


def show_stable_options(stable_releases: list) -> list:
    print("\nSelect stable release:")
    for i, rel in enumerate(stable_releases, 1):
        driver = rel.get("driver_required", "N/A")
        pt = rel.get("pytorch_version", "?")
        print(f"  [{i}] {rel['label']} - PyTorch {pt}, Driver {driver}")
    print("  [a] All stable releases")
    valid = [str(i) for i in range(1, len(stable_releases) + 1)] + ["a"]
    choice = read_user_choice("Enter choice", valid)
    if choice == "a":
        return stable_releases
    return [stable_releases[int(choice) - 1]]


def show_nightly_prompt() -> bool:
    print("\nUse latest nightly release from rocm.nightlies.amd.com? (y/n)")
    print("  [y] Yes - use latest available build")
    print("  [n] No  - select from all available versions")
    choice = read_user_choice("Enter choice", ["y", "n"])
    return choice == "y"


def show_full_menu(nightly_versions: list, stable_releases: list) -> list:
    print("\nSelect a version to generate requirements for:")
    print()
    headers = [
        "#",
        "Label",
        "PyTorch",
        "torchvision",
        "torchaudio",
        "ROCm Suffix",
        "Python",
        "OS",
        "Notes",
    ]
    all_entries = []
    rows = []
    idx = 1
    for entry in nightly_versions:
        pytorch_display = entry["pytorch"].replace(".0a0", "a0")
        tv_display = entry["torchvision"].replace(".0a0", "a0")
        ta_display = entry["torchaudio"].replace(".0a0", "a0")
        rows.append(
            [
                str(idx),
                entry["label"],
                pytorch_display,
                tv_display,
                ta_display,
                entry["rocm_suffix"],
                "3.11-3.13",
                "Win, Lnx",
                entry.get("notes", ""),
            ]
        )
        all_entries.append({"entry": entry, "index": idx})
        idx += 1
    for rel in stable_releases:
        driver = rel.get("driver_required", "N/A")
        notes = f"Driver {driver}" if driver != "N/A" else ""
        rows.append(
            [
                str(idx),
                f"{rel['label']} (stable)",
                rel.get("pytorch_version", "?"),
                rel.get("torchvision_version", "?"),
                rel.get("torchaudio_version", "?"),
                rel.get("rocm_rel", "?"),
                "3.12 only",
                "Win",
                notes,
            ]
        )
        all_entries.append({"entry": rel, "index": idx})
        idx += 1
    from utils import format_table

    print(format_table(headers, rows))
    valid = [str(i) for i in range(1, len(all_entries) + 1)] + ["all"]
    choice = read_user_choice("Enter number (or 'all' to generate all)", valid)
    if choice == "all":
        return [e["entry"] for e in all_entries]
    num = int(choice)
    selected = [e for e in all_entries if e["index"] == num]
    if selected:
        return [selected[0]["entry"]]
    return [nightly_versions[0]] if nightly_versions else []


def show_output_summary(files: list) -> None:
    if not files:
        return
    print("\n=== Generated Requirements Files ===")
    headers = ["File", "PyTorch", "tv", "ta", "ROCm", "Python", "Notes"]
    rows = []
    for f in files:
        rows.append(
            [
                f.get("file", ""),
                f.get("pytorch", ""),
                f.get("torchvision", ""),
                f.get("torchaudio", ""),
                f.get("rocm", ""),
                f.get("python", ""),
                f.get("notes", ""),
            ]
        )
    from utils import format_table

    print(format_table(headers, rows))
    print(f"\nTotal: {len(files)} file(s) generated")
