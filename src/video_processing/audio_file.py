from pydub import AudioSegment
from src.VAD.vad import vad_find_silence


class AudioFile:
    def __init__(self, path: str):
        self.path = path
        self.audio = AudioSegment.from_file(path)

    def detect_silence(self) -> list:
        """
        Detect silence in the audio file.

        Returns:
            list: A list of Silence objects.
        """
        return vad_find_silence(self.path)
