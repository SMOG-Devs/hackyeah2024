#syntax=docker/dockerfile:1.5

FROM python:3.12.6-slim

WORKDIR /frontend

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

COPY ./src/frontend.py .

EXPOSE 8501

CMD ["streamlit", "run", "./frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]