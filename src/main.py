from video_processing import audio, frame_extractor
from pathManager.PathManager import audio_directory, get_video_nr, audio_vad_directory, secrets_path
from VAD import vad_find_silence
from whisper import Whisper
import pickle
from OpenAINodes import StructureNode, SummarizationNode, TopicChangeNode
from os import listdir
from os.path import join

def extract_offset_from_name(name: str) -> float:
    name_ = name.split(sep='.')[:-1]
    name_ = '.'.join(name_)
    offset = name_.split('__')
    return float(offset)

if __name__ == '__main__':
    vad_out_path = audio_vad_directory(1).as_posix()
    audio.extract_audio(video_path=get_video_nr(1).as_posix(),audio_path=audio_directory(1).as_posix())
    silences = vad_find_silence(audio_directory(1).as_posix(),vad_out_path)
    for silence in silences:
        print(silence)
    
    timed_transcriptions = []
    for file in listdir(vad_out_path):    
        with open(join(vad_out_path,file),'rb') as file:
            whisper = Whisper(secrets_path().as_posix())
            transcription = whisper.transcribe(file)
            transcription_timestamps = whisper.transcribe(file, timespans=True)
            timed_transcriptions.append((extract_offset_from_name(file), transcription_timestamps))
        
    with open('video2_text.pickle','wb') as port:
        pickle.dump(transcription,port)

    with open('video2_transcription.pickle','wb') as port:
        pickle.dump(transcription_timestamps,port)
    
    with open('video2_text.pickle','rb') as port:
        trancription = pickle.load(port)

    with open('video2_transcription.pickle','rb') as port:
        transcription_timestamps = pickle.load(port)
        
    # structure = StructureNode(secrets_path())
    # grade = structure.mark_structure(trancription)
    # print(grade)
    
    # structure = SummarizationNode(secrets_path())
    # grade = structure.summarize(trancription)
    # print(grade)
    
    # structure = TopicChangeNode(secrets_path())
    # grade = structure.detect_change(trancription)
    # print(grade)
