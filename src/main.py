from video_processing import audio, frame_extractor
from pathManager.PathManager import audio_directory, get_video_nr, audio_vad_directory
from VAD import vad_find_silence

if __name__ == '__main__':
    audio.extract_audio(video_path=get_video_nr(2).as_posix(),audio_path=audio_directory(2).as_posix())
    silences = vad_find_silence(audio_directory(2).as_posix(),audio_vad_directory(2).as_posix())
    for silence in silences:
        print(silence)