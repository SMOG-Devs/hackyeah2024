from video_processing import audio
from pathManager.PathManager import secrets_path, root_audio_direcory, root_vad_audio_directory
from VAD import vad_find_silence
from whisper import Whisper
from OpenAINodes import StructureNode, SummarizationNode, TopicChangeNode
from os import listdir
from os.path import join
from fastapi import FastAPI, UploadFile
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import List, Tuple
from io import BytesIO
from uuid import uuid4
from metrics import words_per_minute, gunning_fog_index, flesch_reading_ease

objects = dict()


class Output(BaseModel):
    summary: str
    not_changed_topic: bool
    structure: str
    vpm: Tuple[List[int], List[int]]
    silences: List[Tuple[float, float]]
    ganning: float
    flesh: float


@asynccontextmanager
async def lifespan(app: FastAPI):
    objects['whisper'] = Whisper(secrets_path().as_posix())
    objects['structure'] = StructureNode(secrets_path())
    objects['summarize'] = SummarizationNode(secrets_path())
    objects['topic_change'] = TopicChangeNode(secrets_path())
    objects['cunter'] = 0
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/video/analyze")
def extract_offset_from_name(name: str) -> float:
    name_ = name.split(sep='.')[:-1]
    name_ = '.'.join(name_)
    offset = name_.split('__')
    return float(offset)


@app.post("/video/analyze")
async def analyze(file: UploadFile):
    bytes_ = await file.read()
    original_filename = file.filename
    plain_filename = original_filename.split('.')[:-1]
    plain_filename = '.'.join(plain_filename)
    filename = plain_filename + str(uuid4())
    filename_ext = filename + '.wav'
    vad_out_path = root_vad_audio_directory(filename)
    audio_directory = root_audio_direcory() / filename_ext
    audio.extract_audio_from_bytes(BytesIO(bytes_), audio_directory.as_posix())
    silences = vad_find_silence(audio_directory.as_posix(), vad_out_path.as_posix())

    audio_length = silences[-1].end
    timed_transcriptions = []
    for file in listdir(vad_out_path):
        with open(join(vad_out_path, file), 'rb') as file:
            whisper: Whisper = objects['whisper']
            trancription = whisper.transcribe(file)
            transcription_timestamps = whisper.transcribe(file, timespans=True)
            timed_transcriptions.append((extract_offset_from_name(file), transcription_timestamps))

    structure: StructureNode = objects['structure']
    structure_ = structure.mark_structure(trancription)

    summarization: SummarizationNode = objects['summarize']
    summarization_ = summarization.summarize(trancription)

    change: TopicChangeNode = objects['topic_change']
    change_ = change.detect_change(trancription)

    vpm_, timeline = words_per_minute(trancription, audio_length=audio_length)
    ganning = gunning_fog_index(trancription)
    flesh = flesch_reading_ease(trancription)

    return Output(
        summary=summarization_,
        not_changed_topic=change_,
        vpm=(vpm_, timeline),
        silences=[(silence.start, silence.end) for silence in silences],
        ganning=ganning,
        flesh=flesh,
        structure=structure_
    )

# if __name__ == '__main__':
#     vad_out_path = audio_vad_directory(1).as_posix()
#     audio.extract_audio_from_bytes(video_path=get_video_nr(1).as_posix(),audio_path=audio_directory(1).as_posix())
#     silences = vad_find_silence(audio_directory(1).as_posix(),vad_out_path)

#     end_timestamp = silences[-1].end
#     timed_transcriptions = []
#     for file in listdir(vad_out_path):    
#         with open(join(vad_out_path,file),'rb') as file:
#             whisper = Whisper(secrets_path().as_posix())
#             transcription = whisper.transcribe(file)
#             transcription_timestamps = whisper.transcribe(file, timespans=True)
#             timed_transcriptions.append((extract_offset_from_name(file), transcription_timestamps))

#     with open('video2_text.pickle','wb') as port:
#         pickle.dump(transcription,port)

#     with open('video2_transcription.pickle','wb') as port:
#         pickle.dump(transcription_timestamps,port)

#     with open('video2_text.pickle','rb') as port:
#         trancription = pickle.load(port)

#     with open('video2_transcription.pickle','rb') as port:
#         transcription_timestamps = pickle.load(port)

#     # structure = StructureNode(secrets_path())
#     # grade = structure.mark_structure(trancription)
#     # print(grade)

#     # structure = SummarizationNode(secrets_path())
#     # grade = structure.summarize(trancription)
#     # print(grade)

#     # structure = TopicChangeNode(secrets_path())
#     # grade = structure.detect_change(trancription)
#     # print(grade)
