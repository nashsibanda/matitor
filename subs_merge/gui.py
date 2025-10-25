from pathlib import Path
import tkinter as tk
from tkinter import filedialog

from subs_merge.batch import batch_extract
from subs_merge.full_process import run_full_process
from subs_merge.merger import FILE_EXTENSIONS as SUBTITLE_FILE_EXTENSIONS, Merger
from subs_merge.extractor import Extractor


class NoFileSelectedError(Exception):
    """Raised when no file is selected in the file dialog.

    Attributes:
        title: The title of the file dialog.
    """

    def __init__(self, title: str):
        self.title = title
        super().__init__(f"No file selected for '{title}'")


def create_root(title: str):
    root = tk.Tk()
    root.lift()
    root.wm_title(title)
    root.wm_attributes("-topmost", 1)
    return root


def file_dialog(
    root: tk.Tk,
    title: str,
    filetypes: tuple[str, str] | None = None,
    initialdir: Path | None = None,
) -> str:
    initialdir = initialdir or Path.home()
    filetypes_arr = []
    if filetypes:
        filetypes_arr.append(filetypes)
    filetypes_arr.append(("All Files", "*.*"))

    start = str(initialdir.absolute())

    file_path = filedialog.askopenfilename(
        parent=root,
        title=title,
        filetypes=filetypes_arr,
        initialdir=start,
    )
    if not file_path:
        raise NoFileSelectedError(title)
    return file_path


def directory_dialog(
    root: tk.Tk,
    title: str,
    initialdir: Path | None = None,
) -> str:
    initialdir = initialdir or Path.home()
    start = str(initialdir.absolute())

    directory_path = filedialog.askdirectory(
        parent=root,
        title=title,
        initialdir=start,
    )
    if not directory_path:
        raise NoFileSelectedError(title)
    return directory_path


def run_merge_gui():
    root = create_root("Subtitle Merger")
    original_file_path = file_dialog(
        root=root,
        title="Select the ORIGINAL subtitle file",
        filetypes=(
            "Subtitles",
            " ".join([f"*.{ext}" for ext in SUBTITLE_FILE_EXTENSIONS]),
        ),
    )
    print(f"Original Subtitle File: {Path(original_file_path).name}")
    orig_path = Path(original_file_path)
    additional_file_path = filedialog.askopenfilename(
        root=root,
        title="Select the ADDITIONAL subtitle file to add",
        filetypes=(
            "Subtitles",
            " ".join([f"*.{ext}" for ext in SUBTITLE_FILE_EXTENSIONS]),
        ),
        initialdir=orig_path.parent,
    )
    print(f"Additional Subtitle File: {Path(additional_file_path).name}")

    add_path = Path(additional_file_path)
    merger = Merger(orig_path, add_path)
    merged_subtitle_file_path = merger.merge()
    print(f"Saved {merged_subtitle_file_path}")

    root.destroy()


def run_extract_gui():
    root = create_root("Subtitle Extractor")
    mkv_file_path = file_dialog(
        root=root,
        title="Select the MKV file to extract subtitles from",
        filetypes=("MKV Files", "*.mkv"),
    )
    print(f"MKV File: {Path(mkv_file_path).name}")
    extractor = Extractor(mkv_file_path)
    extractor.extract()
    root.destroy()


def run_full_process_gui():
    root = create_root("Subtitle Merger")
    mkv_file_path = file_dialog(
        root=root,
        title="Select the MKV file to extract subtitles from",
        filetypes=("MKV Files", "*.mkv"),
    )
    print(f"MKV File: {Path(mkv_file_path).name}")
    additional_subtitle_file_path = file_dialog(
        root=root,
        title="Select the additional subtitle file to add",
        filetypes=("Subtitles", "*.ass"),
        initialdir=Path(mkv_file_path).parent,
    )
    print(f"Additional Subtitle File: {Path(additional_subtitle_file_path).name}")
    run_full_process(mkv_file_path, additional_subtitle_file_path)
    root.destroy()


def run_batch_process_gui():
    root = create_root("Subtitle Batch Processor")
    directory_path = directory_dialog(
        root=root,
        title="Select the directory to process",
    )
    print(f"Directory: {directory_path}")
    batch_extract(Path(directory_path))
    root.destroy()
