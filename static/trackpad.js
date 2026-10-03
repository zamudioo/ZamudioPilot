/**
 * trackpad.js — Shared trackpad + left-click logic
 * Used by both index.html and mouse.html
 * Requires: socket (SocketIO instance) already defined in parent page
 */

function initTrackpad(trackpadId, leftBtnId) {
  const trackpad = document.getElementById(trackpadId);
  const leftBtn  = document.getElementById(leftBtnId);

  const MOVE_THRESHOLD = 5;
  const TAP_TIME       = 200;

  let pointers         = new Map();
  let initialTouch     = null;
  let didMove          = false;
  let leftButtonDown   = false;
  let twoFingerTap     = false;
  let gestureStart     = 0;
  let initialPositions = new Map();
  let lastScrollY      = 0;

  // ── Left button hold (drag) ──────────────────────────────────────────────
  leftBtn.addEventListener('pointerdown', () => {
    leftButtonDown = true;
    socket.emit('mouse_down', { button: 'left' });
  });
  leftBtn.addEventListener('pointerup', () => {
    leftButtonDown = false;
    socket.emit('mouse_up', { button: 'left' });
  });

  // ── Trackpad pointer events ──────────────────────────────────────────────
  trackpad.addEventListener('pointerdown', e => {
    pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
    trackpad.setPointerCapture(e.pointerId);

    if (pointers.size === 1) {
      initialTouch = { x: e.clientX, y: e.clientY };
      didMove = false;
    } else if (pointers.size === 2) {
      twoFingerTap     = true;
      gestureStart     = Date.now();
      initialPositions = new Map(pointers);
      const ys         = Array.from(pointers.values()).map(p => p.y);
      lastScrollY      = (ys[0] + ys[1]) / 2;
    }
  });

  trackpad.addEventListener('pointermove', e => {
    if (!pointers.has(e.pointerId)) return;
    pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });

    if (pointers.size === 2) {
      // Two-finger scroll
      if (twoFingerTap) {
        const init = initialPositions.get(e.pointerId);
        if (init && Math.hypot(e.clientX - init.x, e.clientY - init.y) > MOVE_THRESHOLD) {
          twoFingerTap = false;
        }
      }
      const ys    = Array.from(pointers.values()).map(p => p.y);
      const avgY  = (ys[0] + ys[1]) / 2;
      const dy    = avgY - lastScrollY;
      lastScrollY = avgY;
      socket.emit('mouse_scroll', { dy: -dy });

    } else {
      // One-finger move
      if (initialTouch) {
        const dx = e.clientX - initialTouch.x;
        const dy = e.clientY - initialTouch.y;
        if (Math.hypot(dx, dy) > MOVE_THRESHOLD) didMove = true;
      }
      socket.emit('mouse_move', { dx: e.movementX, dy: e.movementY });
    }
  });

  trackpad.addEventListener('pointerup', e => {
    pointers.delete(e.pointerId);
    trackpad.releasePointerCapture(e.pointerId);

    if (pointers.size === 0) {
      if (!leftButtonDown && !didMove) {
        socket.emit('mouse_click', { button: 'left' });
      }
      if (twoFingerTap && (Date.now() - gestureStart) < TAP_TIME) {
        socket.emit('mouse_click', { button: 'right' });
      }
      initialTouch = null;
      didMove      = false;
      twoFingerTap = false;
    }
  });

  trackpad.addEventListener('pointercancel', e => {
    pointers.clear();
    trackpad.releasePointerCapture(e.pointerId);
    initialTouch = null;
    didMove      = false;
    twoFingerTap = false;
  });
}
