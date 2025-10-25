#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["pymkv2>=2.1.2","pysubs2>=1.8.0"]
# ///

"""Extract subtitles from a Matroska file."""

import argparse

from subs_merge.extractor import Extractor


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    # parser.add_argument('command', choices=['extract', 'merge'], help="the command to run")
    parser.add_argument("mkv_file", help="the .mkv to extract an .srt from")
    args = parser.parse_args()

    Extractor(args.mkv_file).extract()
