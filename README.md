# 🎬 Project DUDE 🤙

**One Pose. Zero Clicks. Full Mass! 🔥**

Project DUDE is a movie-inspired, hand-gesture-controlled music player that turns an iconic PR pose into a real-time interaction. Using computer vision, it detects the gesture through a webcam and plays **“Oorum Blood”** automatically.

## ✨ Features

- 🖐️ **Hand Gesture Recognition** — Detects the PR pose using MediaPipe.
- 📷 **Real-Time Camera Tracking** — Uses OpenCV to process webcam frames.
- 🎵 **Automatic Music Playback** — Plays music when the target gesture is detected.
- 🌐 **Flask Integration** — Connects the Python backend with a web interface.
- 🎬 **Cinematic Interface** — HTML, CSS, and JavaScript create the interactive experience.

## 🛠️ Tech Stack

- Python
- OpenCV
- MediaPipe
- Pygame
- Flask
- HTML, CSS, JavaScript

## ⚙️ How It Works

1. Start the application and activate the camera.
2. Show the PR hand gesture in front of the webcam.
3. MediaPipe tracks the hand landmarks.
4. Python checks whether the gesture matches the target pose.
5. When detected, Pygame plays the music.

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/mohamedfahim18/Project-Dude.git
cd Project-DUDE
```

### 2. Install dependencies

```bash
pip install opencv-python mediapipe pygame flask
```

### 3. Add your assets

Place the required MediaPipe model file and your music file in the appropriate project locations. Update the file paths in the code if necessary.

### 4. Run the application

Run your Flask application's Python entry-point file, then open the local URL displayed in the terminal.

## 🎯 Project Goal

To combine computer vision, gesture recognition, and web development into a fun, interactive, cinema-inspired experience.

## 👨‍💻 Author

Developed as a creative experiment in Python, computer vision, and gesture-based interaction.

**In *Project DUDE*, my hand doesn't act on its own; it makes my code act! 🤙🔥**
