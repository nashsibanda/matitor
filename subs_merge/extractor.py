"""Extract subtitles from a Matroska file."""

from pathlib import Path

from pymkv import MKVFile, MKVTrack

from pymkv.TypeTrack import get_track_extension as pymkv_get_track_extension

TrackId = int

ADDITIONAL_EXTENSIONS = {
    "SubStationAlpha": "ass",
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

    def __init__(self, mkv_file_path: str) -> None:
        self.file_path = Path(mkv_file_path)
        self.mkv_file = MKVFile(mkv_file_path)
        self.subtitle_tracks = {
            track.track_id: track
            for track in self.mkv_file.tracks
            if track.track_type == "subtitles"
        }

    def _get_track_info_string(self, track: MKVTrack) -> str:
        return f"ID: {track.track_id} - Lang: {track.language} - Track Name: {track.track_name} - Codec: {track.track_codec}"

    def extract(self, file_path: Path | str | None = None) -> str:
        selected_track = self._ask_for_choice()
        return self._extract_track(selected_track, file_path)

    def _ask_for_choice(self) -> MKVTrack:
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

    def _extract_track(
        self, track: MKVTrack, file_path: Path | str | None = None
    ) -> str:
        track.extension = get_track_extension(track)
        if file_path is None:
            file_path = self.file_path.parent
        return track.extract(file_path)
