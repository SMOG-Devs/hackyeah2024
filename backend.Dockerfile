#syntax=docker/dockerfile:1.5

FROM python:3.12.6-slim

WORKDIR /backend

RUN apt-get update --fix-missing && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install wget build-essential cmake libfreetype6-dev pkg-config libfontconfig-dev libjpeg-dev libopenjp2-7-dev -y

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