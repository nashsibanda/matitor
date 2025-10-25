#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["pymkv2>=2.1.2"]
# ///

"""Extract subtitles from a Matroska file."""

import argparse
from pathlib import Path

from pymkv import MKVFile, MKVTrack

from pymkv.TypeTrack import get_track_extension as pymkv_get_track_extension

TrackId = int

ADDITIONAL_EXTENSIONS = {
    "SubStationAlpha": "ssa",
}


def get_track_extension(track: MKVTrack) -> str | None:
    base_extension = pymkv_get_track_extension(track)
    if base_extension is None and (codec_id := track.track_codec) is not None:
        return ADDITIONAL_EXTENSIONS.get(codec_id, base_extension)
    return base_extension


class Extractor:
    mkv_file: MKVFile
    file_path: Path
    subtitle_tracks: dict[TrackId, MKVTrack]

    def __init__(self, mkv_file_path: str):
        self.file_path = Path(mkv_file_path)
        self.mkv_file = MKVFile(mkv_file_path)
        self.subtitle_tracks = {
            track.track_id: track
            for track in self.mkv_file.tracks
            if track.track_type == "subtitles"
        }

    def _get_track_info_string(self, track: MKVTrack) -> str:
        return f"ID: {track.track_id} - Lang: {track.language} - Track Name: {track.track_name} - Codec: {track.track_codec}"

    def extract(self):
        selected_track = self._ask_for_choice()
        self._extract_track(selected_track)

    def _ask_for_choice(self):
        for track in self.subtitle_tracks.values():
            print(self._get_track_info_string(track))

        selected_track_id = None
        while selected_track_id is None:
            raw_selected_track = input(
                "Please enter the ID of the track to be extracted: "
            )
            if (
                raw_selected_track.isdigit()
                and (selected_track := int(raw_selected_track)) in self.subtitle_tracks
            ):
                selected_track_id = selected_track
            else:
                print("Please enter a valid track ID.")
        print(
            f"Selected track: {self._get_track_info_string(self.subtitle_tracks[selected_track_id])}"
        )
        return self.subtitle_tracks[selected_track_id]

    def _extract_track(self, track: MKVTrack):
        subtitle_file_path = self.file_path.parent
        track.extension = get_track_extension(track)

        track.extract(subtitle_file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mkv_file", help="the .mkv to extract an .srt from")
    args = parser.parse_args()

    Extractor(args.mkv_file).extract()
