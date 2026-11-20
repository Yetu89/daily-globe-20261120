"""Entrypoint: place the built front page where the harness expects it.

Standard library only. The image itself is produced by
tools/build_image.py and committed here as entry.png; this script
copies it into /output/entry.png.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST_DIR = "/output"
DST = os.path.join(DST_DIR, "entry.png")


def main():
    os.makedirs(DST_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)
    print("wrote", DST)


if __name__ == "__main__":
    main()
