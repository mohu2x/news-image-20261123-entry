#!/usr/bin/env python3
"""news-image-20261123 entry: write the day's news poster to /output/entry.png.

The poster (asset.png, rendered from the headlines of Monday 23 November 2026)
ships in this repository; the program simply copies it, byte for byte, so both
harness runs produce identical output.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "asset.png")
OUT = "/output/entry.png"


def main() -> None:
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    shutil.copyfile(SRC, OUT)


if __name__ == "__main__":
    main()
