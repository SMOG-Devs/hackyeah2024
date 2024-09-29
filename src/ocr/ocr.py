from typing import Any
from typing import Tuple, Optional

import cv2
import easyocr
import matplotlib.pyplot as plt
import numpy as np


def crop_image_and_remove(image_path: str, crop_area: Tuple[int, int, int, int]) -> np.array:
    """
    Crop the image from the specified area and remove that portion from the original image.

    :param image_path: Path to the input image file.
    :param crop_area: Tuple defining the crop area as (x1, y1, x2, y2).
    :raises FileNotFoundError: If the image file is not found at the specified path.
    :raises ValueError: If the crop area is invalid.
    :return: Tuple containing the remaining image and the cropped portion of the image.
    """
    # Load the image using OpenCV
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")

    # Extract crop coordinates
    x1, y1, x2, y2 = crop_area

    # Validate crop area
    if x1 >= x2 or y1 >= y2 or x1 < 0 or y1 < 0 or x2 > image.shape[1] or y2 > image.shape[0]:
        raise ValueError("Invalid crop area provided. Ensure the coordinates are within the image bounds.")

    # Crop the image
    cropped_image = image[y1:y2, x1:x2]

    return cropped_image


def show_image_from_array(image: Any) -> None:
    """
    Display an image (in BGR format) using matplotlib.

    :param image: The image array in BGR format.
    :param title: The title of the image for display.
    :return: None (displays the image using matplotlib).
    """
    # Convert the image from BGR (OpenCV) to RGB (matplotlib format)
    print("Shape:", image.shape)
    # Display the image using matplotlib
    plt.imshow(image, cmap='gray')
    plt.axis('off')  # Turn off axis labels for clean display
    plt.show()


def perform_ocr(image: np.ndarray, crop_area: Optional[Tuple[int, int, int, int]] = None) -> str:
    """
    Perform OCR on the given image, with an option to crop the image before extracting text.

    :param image: The input image as a NumPy array.
    :param crop_area: Optional tuple defining the crop region as (x1, y1, x2, y2). If None, the full image is used.
    :return: Extracted text from the image.
    :raises ValueError: If the image cannot be processed or the crop area is invalid.
    """
    # Check if the image is None or empty
    if image is None or image.size == 0:
        raise ValueError("Provided image is empty or invalid.")

    # If a crop area is provided, validate and apply the crop
    if crop_area:
        x1, y1, x2, y2 = crop_area
        if x1 >= x2 or y1 >= y2:
            raise ValueError("Invalid crop area provided.")

        # Crop the image using the specified coordinates
        image = image[y1:y2, x1:x2]

    # Initialize the EasyOCR reader with Polish as the default language
    reader = easyocr.Reader(['pl'], gpu=True)  # Specify Polish language

    # Perform OCR using EasyOCR
    results = reader.readtext(image)

    # Extract text from results
    extracted_text = ' '.join([result[1] for result in results])

    return extracted_text


def ocr_on_video(video_path: str, crop_area: Optional[Tuple[int, int, int, int]] = (400, 880, 1520, 1080)) -> list[str]:
    """
    Perform OCR on a video file by extracting frames and processing them.

    :param crop_area:
    :param video_path: Path to the input video file.
    :return: Extracted text from the video.
    """
    # Initialize the EasyOCR reader with Polish as the default language
    reader = easyocr.Reader(['pl'], gpu=True)  # Specify Polish language

    # Initialize an empty string to store the extracted text
    extracted_text = []

    # Initialize the video capture object
    cap = cv2.VideoCapture(video_path)

    # Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        ret, image = cap.read()

        # Break the loop if the frame is not read properly
        if not ret:
            break

        # If a crop area is provided, validate and apply the crop
        if crop_area:
            x1, y1, x2, y2 = crop_area
            if x1 >= x2 or y1 >= y2:
                raise ValueError("Invalid crop area provided.")

            # Crop the image using the specified coordinates
            image = image[y1:y2, x1:x2]

        # Perform OCR on the frame
        results = reader.readtext(image)

        # Extract text from results
        frame_text = ' '.join([result[1] for result in results])
        extracted_text.append(frame_text)

    # Release the video capture object
    cap.release()

    return extracted_text


if __name__ == "__main__":
    # Path to the input image
    image_path = r"C:\coding\hackyeah2024\frames\HY_2024_film_01\frame_000061.jpg"

    crop_area: Tuple[int, int, int, int] = (400, 880, 1520, 1080)

    # Crop the image and get the cropped portion
    cropped_image = crop_image_and_remove(image_path, crop_area=crop_area)
    # convert to grayscale
    gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    gray_image = (gray_image == gray_image.max()) * 255

    # Display the cropped image
    show_image_from_array(cropped_image)
    show_image_from_array(gray_image)

    # Perform OCR on the cropped image
    extracted_text = perform_ocr(cropped_image)
    print(f"Extracted Text:\n{extracted_text}")
