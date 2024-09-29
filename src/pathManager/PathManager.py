from pathlib import Path
import os

def get_root_path() -> Path:
    return Path(__file__).parent.parent

def get_video_nr(number: int) -> Path:
    return get_root_path() / 'data' / 'Videos' / f"HY_2024_film_{number:02}.mp4"

def audio_directory(number: int) -> Path:
    return get_root_path() / 'data' / 'OutData' / f"HY_2024_film_{number:02}.wav"

def audio_vad_directory(number: int) -> Path:
    dir_path = get_root_path() / 'data' / 'VadOutData' / f"HY_2024_film_{number:02}"
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    return dir_path

def secrets_path() -> Path:
    return get_root_path() / '.env'