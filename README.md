# MIST
A Comparison of Human and Robotic Motivational Support in a High-Stress Cognitive Task

## Prerequisites

* **Hardware:** Misty II Robot.
* **Network:** The robot and your laptop must be connected to the **same Wi-Fi network**.
* **Software:** Python 3.6 or higher.

## Installation

1.  **Clone or create this project folder.**
2.  **Install required Python libraries:**
    You need `requests` for sending commands and `websocket-client` for listening to the robot.

    ```bash
    pip install requests websocket-client
    ```

## Configuration

Before running any script, you must update the `robot_ip` variable in the Python files with your Misty's actual IP address. You can find this on the Misty App or via the Misty Studio interface.

```python
robot_ip = "192.168.1.XX" # Replace with your robot's IP
