from video_processing import audio, frame_extractor
from pathManager.PathManager import audio_directory, get_video_nr, audio_vad_directory, secrets_path
from VAD import vad_find_silence
from whisper import Whisper
import pickle
from OpenAINodes import StructureNode, SummarizationNode, TopicChangeNode

if __name__ == '__main__':
    # audio.extract_audio(video_path=get_video_nr(1).as_posix(),audio_path=audio_directory(1).as_posix())
    # silences = vad_find_silence(audio_directory(1).as_posix(),audio_vad_directory(1).as_posix())
    # for silence in silences:
    #     print(silence)
    # with open(r'src/data/VadOutData/HY_2024_film_01/chunk-04.wav','rb') as file:
    #     whisper = Whisper(secrets_path().as_posix())
    #     transcription = whisper.transcribe(file)
        
    # with open('video2_text.pickle','wb') as port:
    #     pickle.dump(transcription,port)
    
    with open('video2_text.pickle','rb') as port:
        trancription = pickle.load(port)
        
    # structure = StructureNode(secrets_path())
    # grade = structure.mark_structure(trancription)
    # print(grade)
    
    # structure = SummarizationNode(secrets_path())
    # grade = structure.summarize(trancription)
    # print(grade)
    
    structure = TopicChangeNode(secrets_path())
    grade = structure.detect_change(trancription)
    print(grade)
