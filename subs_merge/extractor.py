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

    def __init__(self, mkv_file_path: Path | str) -> None:
        if isinstance(mkv_file_path, Path):
            self.file_path = mkv_file_path
        else:
            self.file_path = Path(mkv_file_path)
        self.mkv_file = MKVFile(mkv_file_path)
        self.subtitle_tracks = {
            track.track_id: track
            for track in self.mkv_file.tracks
            if track.track_type == "subtitles"
        }

    def _get_track_info_string(self, track: MKVTrack) -> str:
        return f"ID: {track.track_id} - Lang: {track.language} - Track Name: {track.track_name} - Codec: {track.track_codec}"

    def get_most_likely_track_id(
        self, language: str, track_name: str | None = None
    ) -> int:
        all_tracks = list(self.subtitle_tracks.values())
        same_language_tracks = [
            track for track in all_tracks if track.language == language
        ]
        if len(same_language_tracks) == 0:
            raise ValueError(
                f"No tracks found for language: {language} in {self.file_path.name}"
            )
        if len(same_language_tracks) == 1:
            return same_language_tracks[0].track_id
        if track_name is not None:
            same_track_name_tracks = [
                track
                for track in same_language_tracks
                if track.track_name == track_name
            ]
            if len(same_track_name_tracks) > 0:
                return same_track_name_tracks[0].track_id
        if len(same_language_tracks) > 1:
            full_language_tracks = [
                track
                for track in same_language_tracks
                if any(
                    x in track.track_name.lower()
                    if track.track_name is not None
                    else ""
                    for x in ["full", "complete"]
                )
            ]
            if len(full_language_tracks) > 0:
                return full_language_tracks[0].track_id
        return same_language_tracks[0].track_id

    def extract(
        self, file_path: Path | str | None = None, track_id: int | None = None
    ) -> str:
        print(f"🚨🚨🚨 ==>> track_id: {track_id}")
        if track_id is None:
            selected_track = self._ask_for_choice()
        else:
            try:
                selected_track = self.subtitle_tracks[track_id]
            except KeyError:
                print(f"Track ID {track_id} not found.")
                raise ValueError(f"Track ID {track_id} not found.")
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
