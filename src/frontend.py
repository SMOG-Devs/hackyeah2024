import streamlit as st
import os
import tempfile
import numpy as np
import matplotlib.pyplot as plt
from moviepy.video.io.VideoFileClip import VideoFileClip

from VAD.vad import vad_find_silence
from video_processing.audio import extract_audio


def is_topic_switched():
    not_topic_switch: bool = True  # czy jest spojny
    return not_topic_switch


def prepare_summary():
    summary: list[str] = ["dupa1", "udpa2"]  # bulletpointy
    return summary


def is_speech_structure_preserved():
    # czy jest zachowaana struktura wypowiedzi
    speech_structure: str = "Structure is not good, not terrible. The ending is missing and shit, ya'know brother."
    return speech_structure


def get_words_per_minute():
    # sliding window seconds center -> PWM of the window
    words_per_minute: dict[int, int] = {
        10: 140,
        15: 90,
        20: 145,
        25: 123,
        30: 132,
    }
    return words_per_minute


def get_metrics():
    """
    Returns gunning_fog_index, flesch_reading_ease.
    """
    gunning_fog_index = 20
    flesch_reading_ease = 123.23
    return {
        "gunning_fog_index": gunning_fog_index,
        "flesch_reading_ease": flesch_reading_ease
    }


def display_video(video_path: str):
    """Displays the video in the Streamlit app.

    Args:
        video_path (str): Path to the video file.
    """
    # st.video(video_path, start_time=st.session_state.get('start_time', 0))
    st.video(video_path, start_time=0)


def prepare_video_analysis():
    # Streamlit app with sidebar
    st.sidebar.title("Analiza mowy oraz metryki")

    # Display if the topic was switched
    st.sidebar.subheader("Spójność tematu")
    st.sidebar.write(
        "Temat wypowiedzi został zmieniony w trakcie wypowiedzi."
        if is_topic_switched() else
        "Temat wypowiedzi jest spójny podczas wypowiedzi."
    )

    # Display summary
    st.sidebar.subheader("Podsumowanie wypowiedzi")
    summary = prepare_summary()
    for bullet in summary:
        st.sidebar.write(f"- {bullet}")

    # Display speech structure feedback
    st.sidebar.subheader("Struktura wypowiedzi")
    st.sidebar.write(is_speech_structure_preserved())

    # Display readability metrics
    st.sidebar.subheader("Wskaźnik czytelności")
    metrics = get_metrics()
    st.sidebar.metric("Współczynnik mglistości Gunninga", metrics["gunning_fog_index"])
    st.sidebar.metric("Indeks czytelności Flescha", metrics["flesch_reading_ease"])


def get_video_length(file_path: str) -> float:
    """
    Get the duration (length) of the video in seconds.

    :param file_path: Path to the video file
    :return: Duration of the video in seconds
    """
    with VideoFileClip(file_path) as video_clip:
        return video_clip.duration


def create_silence_segmentation_plot(audio_path: str, video_length: float):
    """
    Creates a spectrogram from the audio track of the video.
    """
    silences = vad_find_silence(audio_path, os.path.dirname(audio_path))

    # create segmentation plot based on the length of the audio and the silences
    fig, ax = plt.subplots()
    ax.imshow(np.ones((1, int(video_length))), cmap='Greens')
    # silence have start and end time, so we can calculate the duration
    height = 3
    for silence in silences:
        ax.add_patch(plt.Rectangle((silence.start, 0), silence.end - silence.start, height, color='black'))
    ax.set_xlim(0, int(video_length))
    ax.set_ylim(0, height)

    ax.yaxis.set_visible(False)
    ax.set_xlabel('Czas nagrania [s]')
    st.subheader("Detekcja mowy w czasie")
    st.info("Czarny obszar oznacza ciszę w nagraniu, biały obszar to mowa.")
    st.pyplot(fig)
    # prepare pauzy w mowie
    start_stop_silence: list[tuple[float, float]] = []
    for silence in silences:
        if silence.start != 0 and silence.end != video_length:
            start_stop_silence.append((silence.start, silence.end))
    st.write(f"Pauzy w mowie wykryte w przedziałach czasowych:")
    for idx, (start, stop) in enumerate(start_stop_silence):
        st.write(f"\t* {start:.2f} - {stop:.2f}")


def create_plot_for_pwm():
    """
    Creates and displays a plot for words per minute (WPM) over time.
    """
    pwm = get_words_per_minute()

    # Extract the x and y values from the dictionary
    x_values = list(pwm.keys())  # Time segments (seconds)
    y_values = list(pwm.values())  # Words per minute values

    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(x_values, y_values, marker='o', linestyle='-', color='b')
    # Set labels and title
    ax.set_xlabel('Czas nagrania [s]')
    ax.set_ylabel('Ilość słów na minutę')

    # Display the plot in the Streamlit app
    st.subheader("Analiza tempa - ilość słów na minutę (WPM) w czasie")
    st.pyplot(fig)

    diff_threshold = 30
    diffs = []
    for idx, (time, pwm) in enumerate(pwm.items()):
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
            temp_video_file_path = temp_video_file.name
            temp_vid_length = get_video_length(temp_video_file_path)
            audio_path = "data/audio/audio.wav"
            extract_audio(temp_video_file_path, audio_path)

            # perform OCR on the video, i need video path
            # if st.sidebar.button("Perform OCR"):
            #     ocr_on_video(temp_video_file_path)
            if st.sidebar.button("Przeprowadź analizę wideo"):
                with st.spinner('Proszę czekać, trwa analiza wideo...'):
                    # Display the uploaded video
                    display_video(temp_video_file_path)
                    prepare_video_analysis()
                    create_silence_segmentation_plot(audio_path, temp_vid_length)
                    create_plot_for_pwm()


if __name__ == "__main__":
    main()
