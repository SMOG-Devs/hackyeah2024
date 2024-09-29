import streamlit as st
import tempfile
import numpy as np
import matplotlib.pyplot as plt
from moviepy.video.io.VideoFileClip import VideoFileClip
import pandas as pd
import plotly.express as px

import requests
from typing import Dict


def send_mp4_file(file_path: str, url: str) -> Dict[str, str]:
    """
    Sends an MP4 file to a FastAPI endpoint using a POST request.

    :param file_path: Path to the MP4 file to be sent
    :param url: URL of the FastAPI file upload endpoint
    :return: Response JSON from the server
    """
    with open(file_path, 'rb') as file:
        # Prepare the file to be sent as multipart/form-data
        files = {'file': (file_path, file, 'video/mp4')}
        # Send the POST request
        response = requests.post(url, files=files)
        # Ensure the request was successful
        response.raise_for_status()
        return response.json()


def prepare_summary(summary) -> list[str]:
    return summary


def display_video(video_path: str):
    """Displays the video in the Streamlit app.

    Args:
        video_path (str): Path to the video file.
    """
    # st.video(video_path, start_time=st.session_state.get('start_time', 0))
    st.video(video_path, start_time=0)


def prepare_video_analysis(output: dict):
    # Streamlit app with sidebar
    st.sidebar.title("Analiza mowy oraz metryki")

    # Display if the topic was switched
    st.sidebar.subheader("Spójność tematu")
    st.sidebar.write(
        "Temat wypowiedzi został zmieniony w trakcie wypowiedzi."
        if not output.not_changed_topic else
        "Temat wypowiedzi jest spójny podczas wypowiedzi."
    )

    # Display summary
    st.sidebar.subheader("Podsumowanie wypowiedzi")
    summary = prepare_summary(output.summary)
    st.sidebar.write(f"{summary}")

    # Display speech structure feedback
    st.sidebar.subheader("Struktura wypowiedzi")
    st.sidebar.write(output.structure)

    # Display readability metrics
    # st.sidebar.subheader("Wskaźnik czytelności")
    # metrics = get_metrics()
    # st.sidebar.metric("Współczynnik mglistości Gunninga", metrics["gunning_fog_index"])
    # st.sidebar.metric("Indeks czytelności Flescha", metrics["flesch_reading_ease"])


def get_video_length(file_path: str) -> float:
    """
    Get the duration (length) of the video in seconds.

    :param file_path: Path to the video file
    :return: Duration of the video in seconds
    """
    with VideoFileClip(file_path) as video_clip:
        return video_clip.duration


def create_silence_segmentation_plot(output: dict, video_length: float):
    """
    Creates a spectrogram from the audio track of the video.
    """
    # create segmentation plot based on the length of the audio and the silences
    fig, ax = plt.subplots()
    ax.imshow(np.ones((1, int(video_length))), cmap='Greens')
    # silence have start and end time, so we can calculate the duration
    height = 3
    for start, end in output.silences:
        ax.add_patch(plt.Rectangle((start, 0), end - start, height, color='black'))
    ax.set_xlim(0, int(video_length))
    ax.set_ylim(0, height)

    ax.yaxis.set_visible(False)
    ax.set_xlabel('Czas nagrania [s]')
    st.subheader("Detekcja mowy w czasie")
    st.info("Czarny obszar oznacza ciszę w nagraniu, biały obszar to mowa.")
    st.pyplot(fig)
    # prepare pauzy w mowie
    start_stop_silence: list[tuple[float, float]] = []
    for start, end in output.silences:
        if start != 0 and end != video_length:
            start_stop_silence.append((start, end))
    st.write(f"Pauzy w mowie wykryte w przedziałach czasowych:")
    for idx, (start, stop) in enumerate(start_stop_silence):
        st.write(f"\t* {start:.2f} - {stop:.2f}")


def create_plot_for_pwm(pvm: tuple[list[int], list[int]]):
    """
    Creates and displays a plot for words per minute (WPM) over time.
    """

    # Extract the x and y values from the dictionary
    x_values = pvm[0]  # Time segments (seconds)
    y_values = pvm[1]  # Words per minute values

    # Create a DataFrame
    data = pd.DataFrame({'Czas nagrania [s]': x_values, 'Ilość słów na minutę': y_values})

    # Create the plot
    fig = px.line(data, x='Czas nagrania [s]', y='Ilość słów na minutę', markers=True,
                  title='Analiza tempa - ilość słów na minutę (WPM) w czasie')

    # Set the axis labels
    fig.update_layout(xaxis_title='Czas nagrania [s]', yaxis_title='Ilość słów na minutę')

    # Display the plot in the Streamlit app
    st.subheader("Analiza tempa - ilość słów na minutę (WPM) w czasie")
    st.plotly_chart(fig)

    diff_threshold = 30
    diffs = []
    pwm = zip(x_values, y_values)
    for idx, (time, pwm) in enumerate(pwm):
        if idx > 0:
            diff = abs(pwm - y_values[idx - 1])
            if diff > diff_threshold:
                diffs.append(f"\t* {time}s: {pwm} -> {y_values[idx - 1]} (różnica: {diff})")
    if diffs:
        st.write("Nagła zmiana tempa mowy (różnica 30 PWM)  wykryta w momentach:")
        for diff in diffs:
            st.write(diff)


def main():
    st.title("Go [BreakWordTraps] FinTax")

    # File uploader for video files
    video_file = st.file_uploader("Prześlij plik wideo", type=["mp4"])

    if video_file is not None:
        # Create a temporary file to save the uploaded video
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video_file:
            temp_video_file.write(video_file.read())
            output = send_mp4_file(temp_video_file.name,
                                   "https://backendd.internal.graydune-f2016363.polandcentral"
                                   ".azurecontainerapps.io/video/analyze")
            temp_video_file_path = temp_video_file.name
            temp_vid_length = get_video_length(temp_video_file_path)

            # perform OCR on the video, i need video path
            # if st.sidebar.button("Perform OCR"):
            #     ocr_on_video(temp_video_file_path)
            if st.sidebar.button("Przeprowadź analizę wideo"):
                with st.spinner('Proszę czekać, trwa analiza wideo...'):
                    # Display the uploaded video
                    display_video(temp_video_file_path)
                    prepare_video_analysis(output)
                    create_silence_segmentation_plot(output, temp_vid_length)
                    create_plot_for_pwm(output["vpm"])


if __name__ == "__main__":
    main()
