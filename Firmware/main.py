import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.modules.macros import Press, Release, Tap, Macros
from kmk.keys import KC
from kmk.modules.encoder import Encoder
from kmk.modules.pwm_led import PWMLED

# --------------------------
keyboard = KMKKeyboard()

# --------------------------
# Macro module
macros = Macros()
keyboard.modules.append(macros)

# --------------------------
# Normal buttons
BUTTON_PINS = [board.D8, board.D9, board.D10, board.D11]
keyboard.matrix = KeysScanner(
    pins=BUTTON_PINS,
    value_when_pressed=False,
)

# --------------------------
# Rotary Encoder (Volume Control)
encoder = Encoder()
encoder.pins = (board.D1, board.D2)  # A, B
encoder.map = (KC.VOLU, KC.VOLD)      # CW = Volume Up, CCW = Volume Down
keyboard.modules.append(encoder)

# --------------------------
# LEDs
leds = PWMLED(pins=[board.D3, board.D4])
keyboard.modules.append(leds)

# --------------------------
# Variable to store mic state
mic_on = False

# --------------------------
# Function to toggle mic + LEDs
def toggle_mic(pressed):
    global mic_on
    if pressed:
        mic_on = not mic_on  # toggle state
        if mic_on:
            leds.set_all(255)  # turn on LEDs
        else:
            leds.set_all(0)    # turn off LEDs
        return KC.MUTE       # return MUTE keycode

# --------------------------
# Keymap for Live Streaming
keyboard.keymap = [
    [
        Tap(toggle_mic),  # D8 → Mute/Unmute + LED
        KC.MACRO(Press(KC.LCTRL, KC.LSHIFT, KC.S), Release(KC.LCTRL, KC.LSHIFT, KC.S)),  # D9 → Start/Stop stream
        KC.MACRO(Press(KC.LCTRL, KC.LSHIFT, KC.ONE), Release(KC.LCTRL, KC.LSHIFT, KC.ONE)),  # D10 → Scene 1
        KC.MACRO(Press(KC.LCTRL, KC.LSHIFT, KC.TWO), Release(KC.LCTRL, KC.LSHIFT, KC.TWO)),  # D11 → Scene 2
    ]
]

# --------------------------
if __name__ == '__main__':
    keyboard.go()
