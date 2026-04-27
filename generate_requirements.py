#!/usr/bin/env python3
"""ROCm + PyTorch Requirements Generator (Cross-OS + Python Versions)."""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src" / "python"))

from utils import write_log, setup_logging
from os_target import get_os_target, get_all_os_targets
from python_version import get_python_versions, get_current_python_version
from rocm import get_stable_releases, get_nightly_versions, get_latest_nightly
from generator import generate_all_for_selection
from menu import (
    show_os_menu,
    show_python_menu,
    show_stable_menu,
    show_stable_options,
    show_nightly_prompt,
    show_full_menu,
    show_output_summary,
)


def main():
    parser = argparse.ArgumentParser(
        description="Generate ROCm + PyTorch requirements files"
    )
    parser.add_argument(
        "--output-dir", default=".", help="Output directory for requirements files"
    )
    parser.add_argument(
        "--os-target",
        default="",
        choices=["windows", "linux", "both", ""],
        help="Target OS",
    )
    parser.add_argument(
        "--python-version",
        default="",
        help="Python version(s): 3.11, 3.12, 3.13, 3.14, all, or current",
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Skip prompts, generate all files",
    )
    parser.add_argument(
        "--stable-only", action="store_true", help="Only generate stable release files"
    )
    parser.add_argument(
        "--nightly-only",
        action="store_true",
        help="Only generate nightly version files",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Print without writing files"
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    setup_logging(args.verbose)
    write_log("ROCm + PyTorch Requirements Generator", "SUCCESS")

    if args.non_interactive:
        os_selection = args.os_target.lower() if args.os_target else "windows"
        if os_selection == "both":
            os_targets = ["Windows", "Linux"]
        elif os_selection == "linux":
            os_targets = ["Linux"]
        else:
            os_targets = ["Windows"]

        py_selection = args.python_version.lower() if args.python_version else "all"
        py_tags = get_python_versions(py_selection)

        all_generated = []
        if args.stable_only or not args.nightly_only:
            stable_releases = get_stable_releases()
            for rel in stable_releases:
                result = generate_all_for_selection(
                    rel, py_tags, os_targets, args.output_dir, args.dry_run
                )
                all_generated.extend(result)

        if args.nightly_only or not args.stable_only:
            nightly_versions = get_nightly_versions()
            for entry in nightly_versions:
                result = generate_all_for_selection(
                    entry, py_tags, os_targets, args.output_dir, args.dry_run
                )
                all_generated.extend(result)

        show_output_summary(all_generated)
    else:
        os_selection = show_os_menu()
        if os_selection == "both":
            os_targets = ["Windows", "Linux"]
        elif os_selection == "linux":
            os_targets = ["Linux"]
        else:
            os_targets = ["Windows"]

        py_selection = show_python_menu()
        py_tags = get_python_versions(py_selection)

        all_generated = []
        if not args.nightly_only:
            want_stable = show_stable_menu()
            if want_stable:
                stable_releases = get_stable_releases()
                stable_selections = show_stable_options(stable_releases)
                for rel in stable_selections:
                    result = generate_all_for_selection(
                        rel, py_tags, os_targets, args.output_dir, args.dry_run
                    )
                    all_generated.extend(result)

        if not args.stable_only:
            if not args.nightly_only:
                use_latest = show_nightly_prompt()
                if use_latest:
                    latest = get_latest_nightly()
                    if latest:
                        result = generate_all_for_selection(
                            latest, py_tags, os_targets, args.output_dir, args.dry_run
                        )
                        all_generated.extend(result)
                else:
                    nightly_versions = get_nightly_versions()
                    stable_releases = get_stable_releases()
                    entries = show_full_menu(nightly_versions, stable_releases)
                    for entry in entries:
                        result = generate_all_for_selection(
                            entry, py_tags, os_targets, args.output_dir, args.dry_run
                        )
                        all_generated.extend(result)

        show_output_summary(all_generated)


if __name__ == "__main__":
    main()
