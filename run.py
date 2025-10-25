# /// script
# requires-python = ">=3.13"
# dependencies = ["pysubs2>=1.8.0", "pymkv2>=2.1.2"]
# ///

import argparse
from pathlib import Path
import sys

from subs_merge.batch import batch_extract
from subs_merge.gui import (
    NoFileSelectedError,
    run_batch_process_gui,
    run_extract_gui,
    run_merge_gui,
    run_full_process_gui,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        choices=["extract", "merge", "full", "batch", "batch-cli"],
        help="The command to run",
    )
    cli_group = parser.add_argument_group("cli", "CLI arguments")
    cli_group.add_argument(
        "-d",
        "--directory-path",
        default=Path.cwd(),
        type=Path,
        help="The directory to process (for batch-cli command)",
    )
    args = parser.parse_args()
    try:
        if args.command == "extract":
            run_extract_gui()
        elif args.command == "merge":
            run_merge_gui()
        elif args.command == "full":
            run_full_process_gui()
        elif args.command == "batch":
            run_batch_process_gui()
        elif args.command == "batch-cli":
            if args.directory_path is None:
                print("Error: --directory-path is required for batch-cli command")
                return 1
            batch_extract(args.directory_path)
    except NoFileSelectedError as e:
        print(f"Error: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
