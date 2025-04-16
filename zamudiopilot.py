# zamudiopilot.py

from flask import Flask, render_template
from flask_socketio import SocketIO
import pyautogui
import socket

SCROLL_FACTOR = 5  # puedes cambiar valores hasta q se acomode el scroll

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

@socketio.on('mouse_move')
def handle_mouse_move(data):
    dx = data.get('dx', 0)
    dy = data.get('dy', 0)
    pyautogui.moveRel(dx, dy)

@socketio.on('mouse_click')
def handle_mouse_click(data):
    button = data.get('button', 'left')
    pyautogui.click(button=button)

@socketio.on('mouse_down')
def handle_mouse_down(data):
    button = data.get('button', 'left')
    pyautogui.mouseDown(button=button)

@socketio.on('mouse_up')
def handle_mouse_up(data):
    button = data.get('button', 'left')
    pyautogui.mouseUp(button=button)

@socketio.on('mouse_scroll')
def handle_mouse_scroll(data):
    # Convertimos y aplicamos el factor de velocidad
    raw_dy = data.get('dy', 0)
    try:
        dy = int(raw_dy) * SCROLL_FACTOR
    except (TypeError, ValueError):
        dy = 0
    if dy != 0:
        pyautogui.scroll(dy)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

if __name__ == '__main__':
    ip = get_local_ip()
    port = 5000
    print(f'Servidor corriendo en http://{ip}:{port}')
    socketio.run(app, host='0.0.0.0', port=port)
