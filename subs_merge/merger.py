import argparse
from copy import deepcopy
from pathlib import Path
from pysubs2 import SSAFile, SSAEvent, SSAStyle
from pysubs2.formats import FILE_EXTENSION_TO_FORMAT_IDENTIFIER

FILE_EXTENSIONS = tuple(FILE_EXTENSION_TO_FORMAT_IDENTIFIER.keys())


def events_overlap(event_1: SSAEvent, event_2: SSAEvent) -> bool:
    return event_1.end >= event_2.start and event_1.start <= event_2.end


def event_contains_multiple_lines(event: SSAEvent) -> bool:
    return event.plaintext.count("\n") > 0


class Merger:
    original_file: SSAFile
    additional_file: SSAFile
    all_styles: dict[str, SSAStyle]
    all_events: list[SSAEvent]
    new_file: SSAFile
    default_style_name: str | None
    add_default_style_name: str
    new_file_path: Path

    def __init__(
        self,
        original_file_path: Path,
        additional_file_path: Path,
        new_file_name: str | None = None,
    ):
        self.original_file = SSAFile.load(str(original_file_path))
        self.additional_file = SSAFile.load(str(additional_file_path))
        self.default_style_name = None
        self.add_default_style_name = ""
        self._build_styles()
        self._build_events()
        self._build_new_file()
        self.new_file_path = (
            original_file_path.parent
            / f"{new_file_name or f'{original_file_path.stem}.merged'}.ass"
        )

    def _build_styles(self) -> None:
        self.all_styles = deepcopy(self.original_file.styles)
        for event in self.original_file.events:
            if event.type == "Dialogue":
                if f"{event.style}Add" not in self.all_styles:
                    if not self.default_style_name and event.style == "Default":
                        self.default_style_name = event.style
                        self.add_default_style_name = f"{event.style}Add"
                    new_style = deepcopy(self.original_file.styles[event.style])
                    new_style_marginv = new_style.marginv + new_style.fontsize + 10
                    new_style.marginv = int(new_style_marginv)
                    self.all_styles[f"{event.style}Add"] = new_style
        print(f"Copied/Created {len(self.all_styles)} styles")

    def _build_events(self) -> None:
        additional_events = []
        for _event in self.additional_file.events:
            event = deepcopy(_event)
            if event.type == "Dialogue":
                event.style = self.add_default_style_name
                if self.should_fix_margins(event):
                    base_style = self.all_styles[event.style]
                    event.marginv = int(base_style.marginv + base_style.fontsize + 10)
                additional_events.append(event)

        self.all_events = sorted(
            [*self.original_file.events, *additional_events], key=lambda x: x.start
        )
        print(f"Built {len(self.all_events)} events")

    def _build_new_file(self) -> None:
        new_file = SSAFile()
        new_file.info = deepcopy(self.original_file.info)
        new_file.aegisub_project = deepcopy(self.original_file.aegisub_project)
        new_file.fonts_opaque = deepcopy(self.original_file.fonts_opaque)
        new_file.graphics_opaque = deepcopy(self.original_file.graphics_opaque)
        new_file.fps = deepcopy(self.original_file.fps)
        new_file.format = deepcopy(self.original_file.format)
        new_file.styles = self.all_styles
        self.new_file = new_file

    def should_fix_margins(self, additional_event: SSAEvent):
        for event in sorted(self.original_file.events, key=lambda x: x.start):
            if event.start > additional_event.end:
                return False
            if events_overlap(
                event, additional_event
            ) and event_contains_multiple_lines(event):
                return True
        return False

    def merge(self):
        print("Merging events...")
        for event in self.all_events:
            self.new_file.append(event)
        self.new_file.save(str(self.new_file_path))
        return self.new_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    # parser.add_argument('command', choices=['extract', 'merge'], help="the command to run")
    parser.add_argument("original_file_path", help="The original subtitle file")
    parser.add_argument(
        "additional_file_path", help="The additional subtitle file to merge in"
    )
    args = parser.parse_args()

    orig_path = Path(args.original_file_path)
    add_path = Path(args.additional_file_path)
    merger = Merger(orig_path, add_path)
    merger.merge()
