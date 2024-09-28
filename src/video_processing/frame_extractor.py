import cv2
import os
from typing import Optional


class VideoFrameExtractor:
    """
    A class to extract frames from a video file and save them as images in the specified output directory.
    """

    def __init__(self, video_path: str, output_dir: str):
        """
        Initialize the VideoFrameExtractor.

        :param video_path: Path to the video file.
        :param output_dir: Directory where extracted frames will be saved.
        """
        self.video_path = video_path
        self.output_dir = output_dir
        # makedirs
        os.makedirs(output_dir, exist_ok=True)

    def extract_frames(self, frame_rate: Optional[int] = 1) -> None:
        """
        Extract and save frames from the video at the specified frame rate.

        :param frame_rate: Number of frames to skip between saves. Default is 1, meaning save every frame.
        """
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise ValueError(f"Error opening video file: {self.video_path}")

        frame_count = 0
        saved_frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % frame_rate == 0:
                frame_filename = os.path.join(self.output_dir, f"frame_{saved_frame_count:06d}.jpg")
                cv2.imwrite(frame_filename, frame)
                print(f"Saved frame {saved_frame_count} at {frame_filename}")
                saved_frame_count += 1

            frame_count += 1

        cap.release()
        print(f"Extraction complete. {saved_frame_count} frames saved.")


if __name__ == "__main__":
    # Path to the input video file
    video_path = r"C:\coding\hackyeah2024\videos\HY_2024_film_01.mp4"
    file_name = video_path.split("\\")[-1].split(".")[0]
    # Directory where extracted frames will be saved
    output_dir = rf"../../data/frames/{file_name}"

    # Initialize the VideoFrameExtractor
    extractor = VideoFrameExtractor(video_path, output_dir)

    # Extract frames from the video at a frame rate of 10 (i.e., save every 10th frame)
    extractor.extract_frames(frame_rate=5)
