#!/usr/bin/env python3
"""THE DAILY GLOBE entrypoint (Python 3.13, standard library only).

The front-page image is drawn offline by tools/build_image.py and shipped
as entry.png beside this file; this program copies it to the output
directory, byte for byte, so both grading runs write identical bytes.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
DST = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"),
                    "entry.png")

os.makedirs(os.path.dirname(DST), exist_ok=True)
shutil.copyfile(SRC, DST)
print("wrote", DST, os.path.getsize(DST), "bytes")
