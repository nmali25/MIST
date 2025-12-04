import requests
import time
import base64
import os
from gtts import gTTS

robot_ip = "192.168.0.245"

base_url = f"http://{robot_ip}/api"
upload_url = f"{base_url}/audio"
play_url = f"{base_url}/audio/play"
image_url = f"{base_url}/images/display"
arm_url = f"{base_url}/arms/set"
head_url = f"{base_url}/head"
led_url = f"{base_url}/led"
led_transition_url = f"{base_url}/led/transition"


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


def perform_intro():
    print("Generating and uploading audio...")
    generate_and_upload_audio(
        "Hi! I am Misty! I will be your helper for the test today!",
        "intro1.mp3",
        slow_mode=False
    )
    generate_and_upload_audio(
        "Don't be nervous. I am here to help and motivate you throughout. If you get stuck, click on the ’Hint’ button on the screen and I will give you a hint.",
        "intro2.mp3",
        slow_mode=True
    )
    generate_and_upload_audio(
        "Best of luck!",
        "intro3.mp3",
        slow_mode=False
    )

    print("Starting Intro...")

    requests.post(led_transition_url, json={
        "Red": 148, "Green": 0, "Blue": 211,
        "Red2": 75, "Green2": 0, "Blue2": 130,
        "TransitionType": "Breathe",
        "TimeMs": 1000
    })
    requests.post(image_url, json={"FileName": "e_Admiration.jpg"})
    # requests.post(image_url, json={"FileName": "e_Joy2.jpg"})

    requests.post(head_url, json={"Pitch": 0,
                  "Roll": 0, "Yaw": 0, "Velocity": 70})
    requests.post(arm_url, json={
                  "RightArmPosition": -90, "LeftArmPosition": 80, "RightArmVelocity": 60, "LeftArmVelocity": 60})

    print("Playing Part 1...")
    requests.post(play_url, json={"FileName": "intro1.mp3"})
    time.sleep(5)

    print("Playing Part 2...")
    requests.post(led_transition_url, json={
        "Red": 0, "Green": 191, "Blue": 255,
        "Red2": 0, "Green2": 0, "Blue2": 100,
        "TransitionType": "Breathe",
        "TimeMs": 2000
    })
    requests.post(image_url, json={"FileName": "e_Joy.jpg"})
    requests.post(head_url, json={"Pitch": 10,
                  "Roll": 0, "Yaw": 0, "Velocity": 30})
    requests.post(arm_url, json={
                  "RightArmPosition": 80, "LeftArmPosition": 80, "RightArmVelocity": 30, "LeftArmVelocity": 30})
    requests.post(play_url, json={"FileName": "intro2.mp3"})

    time.sleep(12)

    print("Playing Part 3...")
    requests.post(led_transition_url, json={
        "Red": 0, "Green": 255, "Blue": 0,
        "Red2": 255, "Green2": 255, "Blue2": 0,
        "TransitionType": "Blink",
        "TimeMs": 200
    })
    requests.post(image_url, json={"FileName": "e_Ecstasy.jpg"})
    requests.post(head_url, json={"Pitch": -15,
                  "Roll": 0, "Yaw": 0, "Velocity": 30})

    requests.post(play_url, json={"FileName": "intro3.mp3"})
    time.sleep(3)

    requests.post(led_url, json={"Red": 0, "Green": 0, "Blue": 0})
    requests.post(head_url, json={"Pitch": 0,
                  "Roll": 0, "Yaw": 0, "Velocity": 15})
    requests.post(arm_url, json={
                  "RightArmPosition": 80, "LeftArmPosition": 80, "RightArmVelocity": 40, "LeftArmVelocity": 40})
    requests.post(image_url, json={"FileName": "e_DefaultContent.jpg"})


if __name__ == "__main__":
    try:
        perform_intro()
    except Exception as e:
        print(f"Error: {e}")
