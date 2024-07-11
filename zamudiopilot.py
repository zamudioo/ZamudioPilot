# zamudiopilot.py
from flask import Flask, render_template
from flask_socketio import SocketIO
import pyautogui
import socket

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('volume')
def handle_volume(data):
    if data == 'up':
        pyautogui.press('volumeup')
    elif data == 'down':
        pyautogui.press('volumedown')
    elif data == 'mute':
        pyautogui.press('volumemute')

@socketio.on('media')
def handle_media(data):
    if data == 'play_pause':
        pyautogui.press('playpause')
    elif data == 'next':
        pyautogui.press('nexttrack')
    elif data == 'prev':
        pyautogui.press('prevtrack')

@socketio.on('keyboard')
def handle_keyboard(data):
    pyautogui.write(data)

@socketio.on('mouse')
def handle_mouse(data):
    direction = data['direction']
    distance = 10  # Movimiento en píxeles
    if direction == 'up':
        pyautogui.move(0, -distance)
    elif direction == 'down':
        pyautogui.move(0, distance)
    elif direction == 'left':
        pyautogui.move(-distance, 0)
    elif direction == 'right':
        pyautogui.move(distance, 0)
    elif direction == 'click':
        pyautogui.click()

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

if __name__ == '__main__':
    ip = get_local_ip()
    port = 5000
    print(f'Server running at http://{ip}:{port}')
    socketio.run(app, host='0.0.0.0', port=port)
