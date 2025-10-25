# /// script
# requires-python = ">=3.13"
# dependencies = ["pysubs2>=1.8.0", "pymkv2>=2.1.2"]
# ///

import argparse
import sys

from subs_merge.gui import (
    NoFileSelectedError,
    run_extract_gui,
    run_merge_gui,
    run_full_process_gui,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command", choices=["extract", "merge", "full"], help="The command to run"
    )
    args = parser.parse_args()
    try:
        if args.command == "extract":
            run_extract_gui()
        elif args.command == "merge":
            run_merge_gui()
        elif args.command == "full":
            run_full_process_gui()
    except NoFileSelectedError as e:
        print(f"Error: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
