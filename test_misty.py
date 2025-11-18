import requests
import json
import time

robot_ip = "192.168.0.73"

speak_url = f"http://{robot_ip}/api/tts/speak"
image_url = f"http://{robot_ip}/api/images/display"
arm_url = f"http://{robot_ip}/api/arms/set"
head_url = f"http://{robot_ip}/api/head"

speak_payload = {
    "Text": "Hi! I am Misty!! I will be your examination helper today! How are you?"
}

image_happy_payload = {
    "FileName": "e_Joy.jpg"
}

image_default_payload = {
    "FileName": "e_DefaultContent.jpg"
}

arm_raise_payload = {
    "RightArmPosition": -45,
    "LeftArmPosition": 80,
    "RightArmVelocity": 75,
    "LeftArmVelocity": 75
}

head_raise_payload = {
    "Pitch": -10,
    "Roll": 0,
    "Yaw": 0,
    "Velocity": 90
}

arm_lower_payload = {
    "RightArmPosition": 80,
    "LeftArmPosition": 80,
    "RightArmVelocity": 75,
    "LeftArmVelocity": 75
}

head_reset_payload = {
    "Pitch": 0,
    "Roll": 0,
    "Yaw": 0,
    "Velocity": 90
}

try:
    print("Changing eyes to happy...")
    requests.post(image_url, json=image_happy_payload)

    print("2. Raising right arm...")
    requests.post(arm_url, json=arm_raise_payload)

    print("3. Tilting head up...")
    requests.post(head_url, json=head_raise_payload)

    print("Sending speech command...")
    response = requests.post(speak_url, json=speak_payload)

    print(f"Response: {response.json()}")

    print("Waiting for speech to finish (approx. 7 seconds)...")
    time.sleep(5)

    print("5. Lowering arm...")
    requests.post(arm_url, json=arm_lower_payload)

    print("7. Resetting head...")
    requests.post(head_url, json=head_reset_payload)

    print("Resetting eyes to default...")
    requests.post(image_url, json=image_default_payload)

    print("Sequence complete.")

except requests.exceptions.ConnectionError as e:
    print(f"\n--- CONNECTION ERROR ---")
    print("Could not connect to Misty.")
    print("Please check your IP address and that you are on the same Wi-Fi network.")
except Exception as e:
    print(f"\nAn error occurred: {e}")
