import requests
import json
import time
import websocket

robot_ip = "192.168.0.73"
robot_ws = f"ws://{robot_ip}/pubsub"
arm_url = f"http://{robot_ip}/api/arms/set"

arm_raise_payload = {
    "RightArmPosition": -45,
    "LeftArmPosition": 80,
    "RightArmVelocity": 75,
    "LeftArmVelocity": 75
}

# --- This is the function we call when the event is heard ---


def speak(text):
    print(f"\n*** KEY PHRASE DETECTED! Sending speak command: {text} ***\n")
    try:
        url = f"http://{robot_ip}/api/tts/speak"
        payload = {"Text": text}
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error when trying to speak: {e}")

# --- This tells Misty to turn on her key phrase listener ---


def start_key_phrase_recognition():
    print("Telling Misty to start her key phrase recognition engine...")
    url = f"http://{robot_ip}/api/audio/keyphrase/start"
    try:
        requests.post(url, json={})
    except Exception as e:
        print(f"Error starting recognition: {e}")

# --- This is our subscription message ---


def get_subscription_message():
    return {
        "Operation": "subscribe",
        "Type": "KeyPhraseRecognized",
        "EventName": "KeyPhraseEvent",
        "DebounceMs": 100
    }

# --- These functions handle WebSocket events ---


def on_message(ws, message):
    data = json.loads(message)

    # --- THIS IS THE NEW LOGIC ---
    # Check 1: Does the eventName match?
    # Check 2: Is the "message" field a dictionary (not a string)?
    if (data.get("eventName") == "KeyPhraseEvent" and
            isinstance(data.get("message"), dict)):

        # We can also check the confidence level
        confidence = data["message"].get("confidence")
        if confidence and confidence > 50:
            speak("Hi Niyati")
            requests.post(arm_url, json=arm_raise_payload)


def on_error(ws, error):
    print(f"--- WebSocket Error: {error} ---")


def on_close(ws, close_status_code, close_msg):
    print("--- WebSocket Closed ---")


def on_open(ws):
    print("--- WebSocket Connection Opened ---")
    start_key_phrase_recognition()
    print("Subscribing to Key Phrase events...")
    ws.send(json.dumps(get_subscription_message()))


# --- Main program ---
if __name__ == "__main__":
    try:
        print("Starting WebSocket listener...")

        ws_app = websocket.WebSocketApp(robot_ws,
                                        on_open=on_open,
                                        on_message=on_message,
                                        on_error=on_error,
                                        on_close=on_close)

        print(f"Script is now listening indefinitely for 'Hey Misty'...")
        print("Press Ctrl+C to stop the script.")
        ws_app.run_forever()

    except KeyboardInterrupt:
        print("\nScript stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
