#!/usr/bin/env python3
"""Dump UI hierarchy emulator dan cetak node yang punya teks + koordinat tengahnya."""
import re
import subprocess
import sys

ADB = "/home/isyarharun/Android/Sdk/platform-tools/adb"


def sh(*args):
    return subprocess.run([ADB, *args], capture_output=True, text=True).stdout


def nodes():
    sh("shell", "uiautomator", "dump", "/sdcard/ui.xml")
    xml = sh("shell", "cat", "/sdcard/ui.xml")
    out = []
    for m in re.finditer(r'<node[^>]*>', xml):
        tag = m.group(0)
        text = re.search(r'text="([^"]*)"', tag)
        desc = re.search(r'content-desc="([^"]*)"', tag)
        bounds = re.search(r'bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', tag)
        if not bounds:
            continue
        label = (text.group(1) if text else "") or (desc.group(1) if desc else "")
        if not label.strip():
            continue
        x1, y1, x2, y2 = map(int, bounds.groups())
        out.append((label.strip(), (x1 + x2) // 2, (y1 + y2) // 2))
    return out


if __name__ == "__main__":
    needle = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    for label, cx, cy in nodes():
        if needle in label.lower():
            print(f"{cx:>5} {cy:>5}  {label}")
