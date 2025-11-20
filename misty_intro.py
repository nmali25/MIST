import requests
import time
import base64
import os
from gtts import gTTS

robot_ip = "192.168.0.73"

base_url = f"http://{robot_ip}/api"
upload_url = f"{base_url}/audio"
play_url = f"{base_url}/audio/play"
image_url = f"{base_url}/images/display"
arm_url = f"{base_url}/arms/set"
head_url = f"{base_url}/head"


def generate_and_upload_audio(text, filename, slow_mode=False):
    tts = gTTS(text=text, lang='en', slow=slow_mode)
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


def perform_intro():
    print("Generating audio...")
    generate_and_upload_audio(
        "Hi! I am Misty! I will be your helper for the test today!", "intro1.mp3", slow_mode=False)
    generate_and_upload_audio(
        "Don't be nervous. I am here to help and motivate you throughout.", "intro2.mp3", slow_mode=True)
    generate_and_upload_audio("Best of luck!", "intro3.mp3", slow_mode=False)

    print("Starting Intro...")
    requests.post(image_url, json={"FileName": "e_Joy.jpg"})
    requests.post(head_url, json={"Pitch": -20,
                  "Roll": 0, "Yaw": 0, "Velocity": 80})
    requests.post(arm_url, json={
                  "RightArmPosition": -90, "LeftArmPosition": 80, "RightArmVelocity": 60, "LeftArmVelocity": 60})

    requests.post(play_url, json={"FileName": "intro1.mp3"})
    time.sleep(5)

    requests.post(head_url, json={"Pitch": 10,
                  "Roll": 0, "Yaw": 0, "Velocity": 80})
    requests.post(arm_url, json={
                  "RightArmPosition": 80, "LeftArmPosition": 80, "RightArmVelocity": 30, "LeftArmVelocity": 30})

    requests.post(play_url, json={"FileName": "intro2.mp3"})
    time.sleep(5)

    requests.post(image_url, json={"FileName": "e_Ecstasy.jpg"})
    requests.post(head_url, json={"Pitch": -15,
                  "Roll": 0, "Yaw": 0, "Velocity": 20})

    requests.post(play_url, json={"FileName": "intro3.mp3"})
    time.sleep(3)

    requests.post(head_url, json={"Pitch": 15,
                  "Roll": 0, "Yaw": 0, "Velocity": 15})
    requests.post(arm_url, json={
                  "RightArmPosition": 80, "LeftArmPosition": 80, "RightArmVelocity": 40, "LeftArmVelocity": 40})
    requests.post(image_url, json={"FileName": "e_DefaultContent.jpg"})


if __name__ == "__main__":
    try:
        perform_intro()
    except Exception as e:
        print(f"Error: {e}")
