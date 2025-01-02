Brightness and Cursor Controller Using Hand Gestures
This project allows users to control screen brightness and move/click the cursor using hand gestures. It utilizes computer vision techniques with MediaPipe for hand tracking, integrates a GUI with Tkinter, and provides real-time functionality.

Features
Brightness Control: Adjust the screen brightness using the distance between thumb and index finger on the left hand.
Cursor Control: Move the cursor using the index finger of the right hand.
Click Functionality: Perform mouse clicks by bringing the thumb and index finger of the right hand together.
Installation
Follow these steps to set up the project:

Prerequisites
Ensure you have the following installed:

Python 3.7 or higher
A webcam (for hand gesture detection)
Step-by-Step Guide
Clone the Repository

bash
Copy code
git clone https://github.com/yourusername/brightness-cursor-controller.git
cd brightness-cursor-controller
Create a Virtual Environment (Optional but Recommended)

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\\Scripts\\activate`
Install Dependencies Install the required Python libraries:

bash
Copy code
pip install -r requirements.txt
Alternatively, install manually:

bash
Copy code
pip install opencv-python numpy mediapipe pyautogui screen-brightness-control
Run the Application Execute the script:

bash
Copy code
python brightness_cursor_controller.py
Exit the Application Press the q key while the video feed window is active to quit the application.

Usage
Brightness Adjustment:

Use your left hand.
Move the thumb and index finger closer or farther apart to decrease or increase brightness.
Cursor Movement:

Use your right hand.
Point with the index finger to move the cursor.
Clicking:

Bring the thumb and index finger of the right hand together to perform a click.
