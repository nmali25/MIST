import requests
import time
import random
import base64
import os
from gtts import gTTS
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

robot_ip = "192.168.0.73"

base_url = f"http://{robot_ip}/api"
upload_url = f"{base_url}/audio"
play_url = f"{base_url}/audio/play"
image_url = f"{base_url}/images/display"
arm_url = f"{base_url}/arms/set"
head_url = f"{base_url}/head"
led_url = f"{base_url}/led"
led_transition_url = f"{base_url}/led/transition"

QUESTION_HINTS = {
    "1": "Remember, the powerhouse of the cell starts with M.",
    "2": "Think about the order of operations. Multiply before you add.",
    "3": "This event happened right after World War 2.",
    "default": "Take a deep breath. Read the question again slowly. You know this."
}


def generate_and_upload_audio(text, filename, slow_mode=False):
    tts = gTTS(text=text, lang='en', slow=slow_mode, tld='com')
    tts.save(filename)

    with open(filename, "rb") as audio_file:
        encoded_string = base64.b64encode(audio_file.read()).decode('utf-8')

    payload = {
        "FileName": filename,
        "Data": encoded_string,
        "ImmediatelyApply": False,
        "OverwriteExisting": True
    }
    requests.post(upload_url, json=payload)
    if os.path.exists(filename):
        os.remove(filename)


def reset_robot():
    requests.post(led_url, json={"Red": 0, "Green": 0, "Blue": 0})
    requests.post(image_url, json={"FileName": "e_DefaultContent.jpg"})
    requests.post(head_url, json={"Pitch": 0,
                  "Roll": 0, "Yaw": 0, "Velocity": 60})
    requests.post(arm_url, json={
                  "RightArmPosition": 80, "LeftArmPosition": 80, "RightArmVelocity": 60, "LeftArmVelocity": 60})


def thoughtful_pose():
    requests.post(led_transition_url, json={"Red": 0, "Green": 0, "Blue": 255, "Red2": 0,
                  "Green2": 0, "Blue2": 100, "TransitionType": "Breathe", "TimeMs": 1000})
    requests.post(image_url, json={"FileName": "e_Contempt.jpg"})
    requests.post(head_url, json={"Pitch": -10,
                  "Roll": 20, "Yaw": 0, "Velocity": 40})
    requests.post(arm_url, json={
                  "RightArmPosition": -20, "LeftArmPosition": 80, "RightArmVelocity": 40, "LeftArmVelocity": 40})


@app.route('/correct', methods=['POST'])
def handle_correct():
    print("Received Correct Answer Trigger")
    requests.post(led_transition_url, json={"Red": 0, "Green": 255, "Blue": 0,
                  "Red2": 0, "Green2": 0, "Blue2": 0, "TransitionType": "Blink", "TimeMs": 200})
    requests.post(image_url, json={"FileName": "e_Ecstasy.jpg"})
    requests.post(arm_url, json={"RightArmPosition": -90, "LeftArmPosition": -
                  90, "RightArmVelocity": 100, "LeftArmVelocity": 100})
    requests.post(head_url, json={"Pitch": -20,
                  "Roll": 0, "Yaw": 0, "Velocity": 100})

    phrases = ["Woohoo! That is correct!", "Well done! Way to go!"]
    phrase = random.choice(phrases)

    generate_and_upload_audio(phrase, "temp_response.mp3", slow_mode=False)
    requests.post(play_url, json={"FileName": "temp_response.mp3"})

    time.sleep(4)
    reset_robot()
    return jsonify({"status": "success"})


@app.route('/incorrect', methods=['POST'])
def handle_incorrect():
    print("Received Incorrect Answer Trigger")
    requests.post(led_transition_url, json={"Red": 255, "Green": 0, "Blue": 0,
                  "Red2": 0, "Green2": 0, "Blue2": 0, "TransitionType": "Blink", "TimeMs": 500})
    requests.post(image_url, json={"FileName": "e_Sadness.jpg"})
    requests.post(head_url, json={"Pitch": 20,
                  "Roll": 0, "Yaw": 0, "Velocity": 60})
    requests.post(arm_url, json={
                  "RightArmPosition": -40, "LeftArmPosition": 80, "RightArmVelocity": 50, "LeftArmVelocity": 50})

    phrases = ["That's okay, we can do this!",
               "That’s alright. You got the next one!"]
    phrase = random.choice(phrases)

    generate_and_upload_audio(phrase, "temp_response.mp3", slow_mode=True)
    requests.post(play_url, json={"FileName": "temp_response.mp3"})

    time.sleep(5)
    reset_robot()
    return jsonify({"status": "success"})


@app.route('/hint', methods=['POST'])
def handle_hint():
    data = request.json
    q_id = str(data.get("questionId", "default"))
    print(f"Received Hint Request for Question {q_id}")

    hint_text = QUESTION_HINTS.get(q_id, QUESTION_HINTS["default"])

    thoughtful_pose()
    generate_and_upload_audio(hint_text, "hint.mp3", slow_mode=True)
    requests.post(play_url, json={"FileName": "hint.mp3"})

    time.sleep(6)
    reset_robot()
    return jsonify({"status": "success"})


if __name__ == "__main__":
    reset_robot()
    app.run(port=5000)
