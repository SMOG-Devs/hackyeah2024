#syntax=docker/dockerfile:1.5

FROM python:3.12.6-slim

WORKDIR /frontend

COPY ./requirements.txt .

RUN pip install --upgrade pip 

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

COPY ./src/frontend.py .

EXPOSE 8501

CMD ["streamlit", "run", "./frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]