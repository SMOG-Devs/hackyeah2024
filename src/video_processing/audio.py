from moviepy.editor import VideoFileClip
from pathlib import Path
from pydub import AudioSegment


def extract_audio(video_path: str, audio_path: str) -> None:
    """
    Extracts audio from a video file and saves it to the specified audio file.

    Args:
        video_path (str): The path to the input video file.
        audio_path (str): The path to save the extracted audio file.

    Returns:
        None
    """
    # Load the video file
    audio = AudioSegment.from_file(video_path, format="mp4")
    audio.export(audio_path, format="wav")


if __name__ == "__main__":
    video_path = Path(r"C:\coding\hackyeah2024\data\videos\HY_2024_film_01.mp4")
    output_audio_path = video_path.parent.parent / "audio" / f"{video_path.stem}.mp3"
    extract_audio(video_path.as_posix(), str(output_audio_path))