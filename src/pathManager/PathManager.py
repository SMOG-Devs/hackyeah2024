from pathlib import Path

def get_root_path() -> Path:
    return Path(__file__).parent.parent

def get_video_nr(number: int) -> Path:
    return get_root_path() / 'data/Videos' / f"HY_2024_film_{number:02}.mp4"