#syntax=docker/dockerfile:1.5

FROM python:3.11-slim

WORKDIR /backend

COPY ./requirements.txt .

RUN pip install --upgrade pip 

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

RUN mkdir ./data
RUN mkdir ./data/OutData
RUN mkdir ./data/VadOutData
RUN mkdir ./data/Videos


COPY ./src/metrics ./metrics
COPY ./src/ocr ./ocr
COPY ./src/OpenAINodes ./OpenAINodes
COPY ./src/pathManager ./pathManager
COPY ./src/transcription ./transcription
COPY ./src/VAD ./VAD
COPY ./src/video_processing ./video_processing
COPY ./src/whisper ./whisper
COPY ./src/__init__.py .
COPY ./src/main.py . 
COPY ./src/setup.py .

RUN pip install -e .

EXPOSE 8000

CMD ["fastapi", "run", "./main.py"]