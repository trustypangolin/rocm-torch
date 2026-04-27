#!/usr/bin/env python3
"""Fetch ROCm nightlies index and find highest common revisions for torch packages."""

import re
import json
import urllib.request
from collections import defaultdict
from urllib.parse import unquote

BASE_URL = "https://rocm.nightlies.amd.com/v2/gfx1151/"
REQUIRED_PY_TAGS = {"312"}


def fetch_url(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def parse_wheel_links(html, platform="win_amd64"):
    pattern = r'href="([^"]+\.whl)"'
    raw_links = re.findall(pattern, html)
    decoded = [unquote(link.lstrip("../")) for link in raw_links]
    return [w for w in decoded if platform in w]


def extract_rocm_suffix(filename):
    match = re.search(r"\+rocm([^-]+)-", filename)
    return match.group(1) if match else None


def extract_python_tag(filename):
    match = re.search(r"-cp(\d{3})-", filename)
    return match.group(1) if match else None


def extract_base_version(filename, pkg_name):
    pattern = rf"^{re.escape(pkg_name)}-([^-+]+)(\+rocm[^-]+)?-"
    match = re.match(pattern, filename)
    return match.group(1) if match else "unknown"


def find_common_revisions():
    packages = {}
    for pkg in ["torch", "torchvision", "torchaudio"]:
        html = fetch_url(f"{BASE_URL}{pkg}/")
        wheels = parse_wheel_links(html)
        print(f"  {pkg}: {len(wheels)} wheels found")
        packages[pkg] = wheels

    by_suffix_py = defaultdict(
        lambda: {"torch": [], "torchvision": [], "torchaudio": []}
    )
    for pkg, wheels in packages.items():
        for w in wheels:
            suffix = extract_rocm_suffix(w)
            py_tag = extract_python_tag(w)
            if suffix and py_tag:
                by_suffix_py[(suffix, py_tag)][pkg].append(w)

    # Find (suffix, py_tag) combos where all 3 exist
    valid = {}
    for (suffix, py_tag), pkgs in by_suffix_py.items():
        if pkgs["torch"] and pkgs["torchvision"] and pkgs["torchaudio"]:
            valid[(suffix, py_tag)] = pkgs

    # Group by suffix, collect all valid py_tags
    by_suffix = defaultdict(lambda: {"py_tags": set(), "pkgs": {}})
    for (suffix, py_tag), pkgs in valid.items():
        by_suffix[suffix]["py_tags"].add(py_tag)
        by_suffix[suffix]["pkgs"][py_tag] = pkgs

    # Filter to suffixes that have ALL required py_tags
    def extract_date(suffix):
        m = re.search(r"a(\d{8})", suffix)
        return m.group(1) if m else "0"

    filtered = {}
    for suffix, info in by_suffix.items():
        if REQUIRED_PY_TAGS.issubset(info["py_tags"]):
            filtered[suffix] = info

    sorted_suffixes = sorted(filtered.keys(), key=extract_date, reverse=True)
    return {s: filtered[s] for s in sorted_suffixes}


def main():
    print("Fetching package listings...")
    common = find_common_revisions()
    print(f"\nFound {len(common)} common revisions (with cp312)")

    top3 = []
    for i, suffix in enumerate(list(common.keys())[:3]):
        info = common[suffix]
        # Use cp312 packages as the reference
        pkgs = info["pkgs"]["312"]
        if not pkgs:
            continue

        torch_wheel = pkgs["torch"][0]
        tv_wheel = pkgs["torchvision"][0]
        ta_wheel = pkgs["torchaudio"][0]

        torch_ver = extract_base_version(torch_wheel, "torch")
        tv_ver = extract_base_version(tv_wheel, "torchvision")
        ta_ver = extract_base_version(ta_wheel, "torchaudio")

        is_nightly = "a0" in torch_ver
        if is_nightly:
            torch_base = torch_ver.rstrip("a0")
            label = f"{torch_base}-nightly"
            pkg_type = "nightly"
        else:
            label = torch_ver
            pkg_type = "stable"

        py_version_tags = []
        for cp in sorted(info["py_tags"]):
            py_version_tags.append(f"py{cp}")

        entry = {
            "pytorch": torch_ver,
            "torchvision": tv_ver,
            "torchaudio": ta_ver,
            "type": pkg_type,
            "label": label,
            "rocm_suffix": suffix,
            "python_versions": sorted(set(py_version_tags)),
            "notes": "Auto-generated from index" if pkg_type == "nightly" else "",
        }
        top3.append(entry)
        print(f"\n#{i + 1}: {label}")
        print(f"  ROCm suffix: {suffix}")
        print(f"  torch: {torch_ver}")
        print(f"  torchvision: {tv_ver}")
        print(f"  torchaudio: {ta_ver}")
        print(f"  Python versions: {', '.join(sorted(set(py_version_tags)))}")

    output_path = "G:\\Ai\\custom\\src\\curated\\latest_versions.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(top3, f, indent=4)
    print(f"\nWrote {len(top3)} entries to {output_path}")


if __name__ == "__main__":
    main()
