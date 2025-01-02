# Brightness and Cursor Controller

This project uses a webcam to control screen brightness and cursor movement based on hand gestures. It leverages MediaPipe for hand landmark detection, OpenCV for video processing, and Tkinter for the user interface.

## Features

- Adjust screen brightness using the left hand.
- Control cursor movement using the right hand.
- Click gesture detection for mouse clicks.

## Requirements

- Python 3.x
- OpenCV
- NumPy
- Screen Brightness Control
- Tkinter
- PyAutoGUI
- MediaPipe

## Installation

1. Clone the repository:
    ```sh
    
    cd brightness-controller
    ```

2. Install the required packages:
    ```sh
    pip install opencv-python numpy screen-brightness-control tkinter pyautogui mediapipe
    ```

## Usage

Run the main script to start the application:
```sh
python main.py
