import cv2
import mediapipe as mp
import pygame
import threading
from flask import Flask, render_template, Response, jsonify
import math

def calculate_angle(a, b, c):
    angle = math.degrees(
        math.atan2(c.y - b.y, c.x - b.x)
        - math.atan2(a.y - b.y, a.x - b.x)
    )

    angle = abs(angle)

    if angle > 180:
        angle = 360 - angle

    return angle

app = Flask(__name__)

cap = None
camera_running = False
camera_lock = threading.Lock()

BaseOptions = mp.tasks.BaseOptions

pygame.mixer.init()
pygame.mixer.music.load("oorum blood.mp3")

HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode


options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path="hand_landmarker.task"
    ),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1
)


def start_camera():

    global cap
    global camera_running

    with camera_lock:

        if camera_running and cap is not None:
            return True
    
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        cap.set(cv2.CAP_PROP_FPS, 30)

        if not cap.isOpened():

            cap.release()
            cap = None

            return False

        camera_running = True

    return True

def stop_camera():

    global cap
    global camera_running

    with camera_lock:

        camera_running = False

        # Stop music
        pygame.mixer.music.stop()

        # Release camera
        if cap is not None:

            cap.release()
            cap = None


def generate_frames():

    global cap
    global camera_running

    with HandLandmarker.create_from_options(options) as landmarker:

        while True:

            with camera_lock:

                if not camera_running or cap is None:
                    break

                current_cap = cap


            success, frame = current_cap.read()

            if not success:
                break



            frame = cv2.flip(frame, 1)

            rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=rgb
            )

            results = landmarker.detect_for_video(
                mp_image,
                int(current_cap.get(cv2.CAP_PROP_POS_MSEC))
            )

            gesture = "No Hand"


            if results.hand_landmarks:

                hand = results.hand_landmarks[0]

                index_tip = hand[8]
                index_pip = hand[6]

                middle_tip = hand[12]
                middle_pip = hand[10]

                ring_tip = hand[16]
                ring_pip = hand[14]

                pinky_tip = hand[20]
                pinky_pip = hand[18]

                index_mcp = hand[5]
                middle_mcp = hand[9]
                ring_mcp = hand[13]
                pinky_mcp = hand[17]

                index_angle = calculate_angle(
                    index_mcp,
                    index_pip,
                    index_tip
                )

                middle_angle = calculate_angle(
                    middle_mcp,
                    middle_pip,
                    middle_tip
                )

                ring_angle = calculate_angle(
                    ring_mcp,
                    ring_pip,
                    ring_tip
                )

                pinky_angle = calculate_angle(
                    pinky_mcp,
                    pinky_pip,
                    pinky_tip
                )

                index_extended = index_angle > 155

                middle_folded = middle_angle < 145
                ring_folded = ring_angle < 145
                pinky_folded = pinky_angle < 145

                if (
                    index_extended
                    and middle_folded
                    and ring_folded
                    and pinky_folded
                ):

                    gesture = "👉 PR POSE DETECTED!"

                    if not pygame.mixer.music.get_busy():

                        pygame.mixer.music.play()

                else:

                    gesture = "Hand detected"


            cv2.putText(
                frame,
                gesture,
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            ret, buffer = cv2.imencode(
                ".jpg",
                frame
            )

            if not ret:
                continue

            frame_bytes = buffer.tobytes()


            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + frame_bytes
                + b"\r\n"
            )


@app.route("/")
def index():

    return render_template("index.html")

@app.route("/start")
def start():

    if start_camera():

        return jsonify({
            "status": "started"
        })

    return jsonify({
        "status": "error",
        "message": "Could not open camera"
    }), 500


@app.route("/stop")
def stop():

    stop_camera()

    return jsonify({
        "status": "stopped"
    })

@app.route("/video_feed")
def video_feed():

    return Response(
        generate_frames(),
        mimetype=(
            "multipart/x-mixed-replace; "
            "boundary=frame"
        )
    )


if __name__ == "__main__":

    app.run(
        debug=False,
        threaded=True
    )