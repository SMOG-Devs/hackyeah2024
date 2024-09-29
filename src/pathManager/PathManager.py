from pathlib import Path
import os

def get_root_path() -> Path:
    return Path(__file__).parent.parent

def get_video_nr(number: int) -> Path:
    return get_root_path() / 'data' / 'Videos' / f"HY_2024_film_{number:02}.mp4"

def audio_directory(number: int) -> Path:
    return get_root_path() / 'data' / 'OutData' / f"HY_2024_film_{number:02}.wav"

def root_audio_direcory():
    return get_root_path() / 'data' / 'OutData'

def root_vad_audio_directory(filename: str) -> Path:
    return get_root_path() / 'data' / 'VadOutData' / filename

def audio_vad_directory(number: int) -> Path:
    dir_path = root_vad_audio_directory() / f"HY_2024_film_{number:02}"
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    return dir_path

def secrets_path() -> Path:
    return get_root_path() / '.env'