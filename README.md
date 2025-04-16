# ZamudioPilot

ZamudioPilot is a tool that allows you to control your computer (volume, media playback, keyboard, mouse, etc.) from a locally hosted web page accessible from a mobile device.

## Features

- Volume control (up, down, mute)
- Media playback control (play/pause, next, previous)
- Keyboard input
- Mouse control (move, click and scroll)

## Installation

### Requirements

- Python 3.x
- pip (Python package manager)

### Steps

1. Clone this repository:

```bash
git clone https://github.com/zamudioo/zamudiopilot.git
cd zamudiopilot
```

2. Install the dependencies:
```bash
pip install flask flask-socketio pyautogui
```
Run the server:
```bash
python zamudiopilot.py
```

Access to the url given on the console
## Usage
###Server
The zamudiopilot.py file is the main server that handles control requests and executes them on the computer.

## Client
The web interface is located in templates/index.html and allows you to send commands to the server.

## Available Commands
### Volume
up: Increase volume
down: Decrease volume
mute: Mute volume
### Media Playback
play_pause: Play/Pause
next: Next track
prev: Previous track
### Keyboard
Type any text in the input field and press "Send".
### Mouse
move around your screen with a trackpad.
(works like a regular trackpad, with functions like scroll, drag, etc.)
