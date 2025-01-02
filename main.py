import cv2
import numpy as np
from screen_brightness_control import set_brightness
import tkinter as tk
from tkinter import ttk
from threading import Thread
import pyautogui
import time

# Function to detect hand landmarks using MediaPipe
def detect_hand_landmarks(image, hand_detector):
    results = hand_detector.process(image)
    return results.multi_hand_landmarks

# Function to calculate the distance between two points
def calculate_distance(point1, point2):
    return np.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

# Function to map hand positions to screen coordinates
def map_to_screen(x, y, frame_width, frame_height, screen_width, screen_height):
    screen_x = int(x * screen_width / frame_width)
    screen_y = int(y * screen_height / frame_height)
    return screen_x, screen_y

# Function to update the brightness label
def update_brightness_label(brightness_level, brightness_label):
    brightness_label.config(text=f"Brightness: {brightness_level}%")

def main():
    import mediapipe as mp

    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
    mp_drawing = mp.solutions.drawing_utils

    # Open webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    screen_width, screen_height = pyautogui.size()
    is_clicking = False
    last_click_time = 0

    # Variables for cursor smoothing
    cursor_x, cursor_y = 0, 0
    alpha = 0.2  # Smoothing factor (0 < alpha <= 1)

    def video_feed():
        nonlocal cap, hands, is_clicking, last_click_time, cursor_x, cursor_y
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame.")
                break

            # Flip the frame horizontally for a mirror effect
            frame = cv2.flip(frame, 1)

            frame_height, frame_width, _ = frame.shape

            # Convert the frame to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect hand landmarks
            hand_landmarks = detect_hand_landmarks(rgb_frame, hands)

            if hand_landmarks:
                for hand in hand_landmarks:
                    # Draw landmarks on the frame
                    mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

                    # Use landmarks for brightness control (left hand)
                    if hand.landmark[mp_hands.HandLandmark.WRIST].x < 0.5:  # Left hand assumption
                        thumb_tip = hand.landmark[mp_hands.HandLandmark.THUMB_TIP]
                        index_tip = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                        # Calculate the distance between thumb tip and index tip
                        distance = calculate_distance(thumb_tip, index_tip)

                        # Normalize distance for brightness control (adjust scaling as needed)
                        brightness_level = int(min(max(distance * 100, 0), 100))

                        # Set screen brightness
                        set_brightness(brightness_level)

                        # Update UI label
                        update_brightness_label(brightness_level, brightness_label)

                    # Use landmarks for cursor control (right hand)
                    else:  # Right hand assumption
                        index_tip = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                        thumb_tip = hand.landmark[mp_hands.HandLandmark.THUMB_TIP]

                        # Map index tip position to screen coordinates for cursor control
                        target_x, target_y = map_to_screen(index_tip.x * frame_width, index_tip.y * frame_height, frame_width, frame_height, screen_width, screen_height)

                        # Smooth cursor movement
                        cursor_x = alpha * target_x + (1 - alpha) * cursor_x
                        cursor_y = alpha * target_y + (1 - alpha) * cursor_y

                        pyautogui.moveTo(int(cursor_x), int(cursor_y))

                        # Detect click gesture (index tip close to thumb tip)
                        click_distance = calculate_distance(index_tip, thumb_tip)
                        current_time = time.time()
                        if click_distance < 0.08:  # Increased sensitivity threshold
                            if not is_clicking and (current_time - last_click_time > 0.3):  # Debounce click
                                pyautogui.click()
                                is_clicking = True
                                last_click_time = current_time
                        else:
                            is_clicking = False

            # Display the frame
            cv2.imshow("Brightness and Cursor Controller", frame)

            # Exit on pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    # Create the UI
    root = tk.Tk()
    root.title("Brightness and Cursor Controller")

    # Create a label for the brightness level
    brightness_label = ttk.Label(root, text="Brightness: 0%", font=("Helvetica", 16))
    brightness_label.pack(pady=20)

    # Run video feed in a separate thread
    video_thread = Thread(target=video_feed)
    video_thread.start()

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
