from flask import Flask, render_template
from flask_socketio import SocketIO
import pyautogui
import socket
import os
import win32api
import threading
import pystray
from PIL import Image, ImageDraw
from plyer import notification

# ── Config ──────────────────────────────────────────────────────────────────
SCROLL_FACTOR  = 5
pyautogui.FAILSAFE = False   # Evita que el server explote si el mouse llega a una esquina

app      = Flask(__name__)
socketio = SocketIO(app)

# Teclas que se mandan directo a pyautogui.press()
SPECIAL_KEYS = {
    "esc", "tab", "capslock", "shift", "ctrl", "alt", "win", "menu",
    "enter", "backspace", "space",
    "f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12",
}

# Teclas del handler 'special' que solo necesitan press()
PRESSABLE_SPECIAL = {
    'space', 'esc', 'win', 'up', 'down', 'right', 'left', 'prtsc',
    'f1','f2','f3','f4','f5','f6','f7','f8','f9','f10','f11','f12',
}

# ── Rutas ────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mouse')
def mouse():
    return render_template('mouse.html')

# ── Handlers de socket ────────────────────────────────────────────────────────
@socketio.on('volume')
def handle_volume(data):
    actions = {'up': 'volumeup', 'down': 'volumedown', 'mute': 'volumemute'}
    if data in actions:
        pyautogui.press(actions[data])

@socketio.on('media')
def handle_media(data):
    actions = {'play_pause': 'playpause', 'next': 'nexttrack', 'prev': 'prevtrack'}
    if data in actions:
        pyautogui.press(actions[data])

@socketio.on('keyboard')
def handle_keyboard(data):
    key = data.strip()
    if key.lower() in SPECIAL_KEYS:
        pyautogui.press(key.lower())
    else:
        pyautogui.write(key)

@socketio.on('special')
def handle_special(data):
    if data in PRESSABLE_SPECIAL:
        pyautogui.press(data)
    elif data == 'copy':
        pyautogui.hotkey('ctrl', 'c')
    elif data == 'paste':
        pyautogui.hotkey('ctrl', 'v')
    elif data == 'cap':
        pyautogui.hotkey('alt', 'f1')
    elif data == 'vid':
        pyautogui.press('f23')
    elif data == 'suspend':
        win32api.SetSystemPowerState(False, True)   # False = sleep, True = hibernate
    elif data == 'off':
        os.system('shutdown -s')

@socketio.on('mouse_move')
def handle_mouse_move(data):
    pyautogui.moveRel(data.get('dx', 0), data.get('dy', 0))

@socketio.on('mouse_click')
def handle_mouse_click(data):
    pyautogui.click(button=data.get('button', 'left'))

@socketio.on('mouse_down')
def handle_mouse_down(data):
    pyautogui.mouseDown(button=data.get('button', 'left'))

@socketio.on('mouse_up')
def handle_mouse_up(data):
    pyautogui.mouseUp(button=data.get('button', 'left'))

@socketio.on('mouse_scroll')
def handle_mouse_scroll(data):
    try:
        dy = int(data.get('dy', 0)) * SCROLL_FACTOR
    except (TypeError, ValueError):
        dy = 0
    if dy != 0:
        pyautogui.scroll(dy)

# ── Utilidades ────────────────────────────────────────────────────────────────
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

def create_tray_icon(ip_address):
    image = Image.new('RGB', (64, 64), color=(0, 0, 0))
    dc    = ImageDraw.Draw(image)
    dc.text((8, 24), 'IP', fill=(255, 255, 255))
    icon  = pystray.Icon('server_ip', image, title=f'Servidor IP: {ip_address}')
    threading.Thread(target=icon.run, daemon=True).start()

def notify_ip(ip):
    notification.notify(
        title='Servidor iniciado',
        message=f'La IP local es: {ip}',
        timeout=10
    )

# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == '__main__':
    ip   = get_local_ip()
    port = 5000
    print(f'Servidor corriendo en http://{ip}:{port}')
    create_tray_icon(ip)
    notify_ip(ip)
    socketio.run(app, host='0.0.0.0', port=port)
