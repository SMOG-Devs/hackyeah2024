from video_processing import audio, frame_extractor
from pathManager.PathManager import audio_directory, get_video_nr

if __name__ == '__main__':
    audio.extract_audio(video_path=get_video_nr(1).as_posix(),audio_path=audio_directory(1).as_posix())