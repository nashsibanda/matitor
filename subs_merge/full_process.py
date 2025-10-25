from tempfile import TemporaryDirectory
from pathlib import Path

from pysubs2.formats import get_file_extension
from subs_merge.extractor import Extractor
from subs_merge.merger import Merger


def run_full_process(
    mkv_file_path_str: str, additional_subtitle_file_path_str: str
) -> Path:
    mkv_file_path = Path(mkv_file_path_str)
    additional_subtitle_file_path = Path(additional_subtitle_file_path_str)
    with TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        extractor = Extractor(mkv_file_path_str)
        original_subtitle_file_path = extractor.extract(temp_dir_path)
        merger = Merger(
            Path(original_subtitle_file_path), additional_subtitle_file_path
        )
        merged_subtitle_file = merger.merge()
        extension = get_file_extension(merged_subtitle_file.format)
        merged_subtitle_file_path = (
            mkv_file_path.parent / f"{mkv_file_path.stem}{extension}"
        )
        merged_subtitle_file.save(merged_subtitle_file_path)
        print(f"Saved {merged_subtitle_file_path}")
        return merged_subtitle_file_path
