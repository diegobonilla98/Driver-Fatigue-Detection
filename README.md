# Driver-Fatigue-Detection
Lightweight Driver Fatigue detection

This project uses the Mediapipe library to detect driver fatigue by monitoring eye blinking and yawns in real-time. It can be used on portable PCs like Raspberry Pi due to its lightness, and only requires a webcam pointing at the driver to function.

## Requirements
To use this program, you'll need:

- Python 3.x
- Mediapipe library (version 0.8.7 or later)
- OpenCV library (version 4.5.2 or later)
- NumPy library (version 1.21.2 or later)

## Usage
The program will automatically detect the default camera and start monitoring the driver for signs of fatigue. If the driver yawns or blinks their eyes for an extended period of time, the program will issue an alert to warn the driver to take a break.

## Customization
You can customize the program by adjusting the threshold values for eye blinking and yawn detection in the driver_fatigue_detection.py script. You can also customize the alert message and the duration of the alert.

## Contributions
Contributions to this project are welcome! If you have any suggestions, bug reports, or feature requests, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License.

## README.md Generation
Thanks, ChatGPT
