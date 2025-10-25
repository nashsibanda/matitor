import argparse
from pathlib import Path

from subs_merge.full_process import run_full_process
from subs_merge.extractor import Extractor
from subs_merge.merger import FILE_EXTENSIONS


def _get_subtitle_files(directory_path: Path, file_stem: str) -> list[Path]:
    subtitle_files = []
    for ext in FILE_EXTENSIONS:
        subtitle_files_for_ext = list(directory_path.glob(f"*{ext}"))
        subtitle_files_for_stem = [
            file for file in subtitle_files_for_ext if file.stem.startswith(file_stem)
        ]
        if len(subtitle_files_for_stem) > 0:
            subtitle_files.extend(subtitle_files_for_stem)
    print(f"🚨🚨🚨 ==>> subtitle_files: {subtitle_files}")
    return subtitle_files


def batch_extract(directory_path: Path) -> None:
    globs = list(directory_path.glob("*.mkv"))
    if len(globs) == 0:
        raise ValueError("No MKV files found in the directory")
    first_file_path = globs[0]
    first_extractor = Extractor(first_file_path)
    first_track = first_extractor._ask_for_choice()
    if first_track.language is None:
        raise ValueError("Unable to determine language of subtitles..")
    for file_path in globs:
        print(f"🚨🚨🚨 ==>> file_path.stem: {file_path.stem}")
        subtitle_files = _get_subtitle_files(directory_path, file_path.stem)
        if len(subtitle_files) == 0:
            raise ValueError(f"No subtitle files found for {file_path.name}")
        if len(subtitle_files) > 1:
            raise ValueError(f"Multiple subtitle files found for {file_path.name}")
        subtitle_file_path = subtitle_files[0]
        run_full_process(
            mkv_file_path_str=str(file_path),
            additional_subtitle_file_path_str=str(subtitle_file_path),
            derive_track_from=first_track,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory_path", type=Path, help="The directory to process")
    args = parser.parse_args()
    batch_extract(args.directory_path)
