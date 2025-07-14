import time
import board
import random
import neopixel
import audiocore
import audiobusio, displayio, busio

from adafruit_display_text import label
import terminalio

from analogio import AnalogIn
from fourwire import FourWire
from digitalio import DigitalInOut, Direction, Pull

from TM1637 import TM1637
from adafruit_st7789 import ST7789
from adafruit_adxl34x import ADXL345


# ---------------- Game Setup ----------------
countdown_time = 180

# ---------------- GPIO pins ----------------
DISPLAY2_SCK_PIN = board.GP2
DISPLAY2_MOSI_PIN = board.GP3
DISPLAY2_MISO_PIN = board.GP4
DISPLAY2_CS_PIN = board.GP5
DISPLAY2_RST_PIN = board.GP6
DISPLAY2_DC_PIN = board.GP7

BIG_BUTTON_PIN = board.GP8
POTENTIOMETER_BUTTON_PIN = board.GP9

ACCELEROMETER_SDA_PIN = board.GP12
ACCELEROMETER_SCL_PIN = board.GP13

NEOPIXEL_PIN = board.GP15

AUDIO_SCK_PIN = board.GP16
AUDIO_WS_PIN = board.GP17
AUDIO_SD_PIN = board.GP18

SEQUENCER_BUTTON_PINS = [board.GP19, board.GP20, board.GP21, board.GP22]

DISPLAY1_DIO_PIN = board.GP26
DISPLAY1_CLK_PIN = board.GP27

POTENTIOMETER_PIN = board.GP28
TRANSMIT_BUTTON_PIN = board.GP10


# ---------------- Helper Classes ----------------
class Potentiometer:
    def __init__(self, pin):
        self.adc = AnalogIn(pin)
        self.choices = [3505, 3515, 3522, 3532, 3535, 3542, 3545, 3552, 3555, 3565, 3572, 3575, 3582, 3592, 3595, 3600]

    @property
    def value(self):
        return 3600 - 0.95 * self.adc.value / 65535 * 100

    @property
    def snapped_value(self):
        return min(self.choices, key=lambda x: abs(x - self.value))


# ---------------- Peripherals ----------------

# Timer display
display1 = TM1637(DISPLAY1_CLK_PIN, DISPLAY1_DIO_PIN)

# Audio output
audio_out = audiobusio.I2SOut(AUDIO_SCK_PIN, AUDIO_WS_PIN, AUDIO_SD_PIN)

# Accelerometer
accel_i2c = busio.I2C(
    ACCELEROMETER_SCL_PIN,
    ACCELEROMETER_SDA_PIN,
    frequency=400_000
)
accelerometer = ADXL345(accel_i2c)

# Potentiometer
potentiometer = Potentiometer(POTENTIOMETER_PIN)

# Buttons
big_button = DigitalInOut(BIG_BUTTON_PIN)
big_button.direction = Direction.INPUT
big_button.pull = Pull.UP

potentiometer_button = DigitalInOut(POTENTIOMETER_BUTTON_PIN)
potentiometer_button.direction = Direction.INPUT
potentiometer_button.pull = Pull.UP

sequence_button1 = DigitalInOut(SEQUENCER_BUTTON_PINS[0])
sequence_button1.direction = Direction.INPUT
sequence_button1.pull = Pull.UP

sequence_button2 = DigitalInOut(SEQUENCER_BUTTON_PINS[1])
sequence_button2.direction = Direction.INPUT
sequence_button2.pull = Pull.UP

sequence_button3 = DigitalInOut(SEQUENCER_BUTTON_PINS[2])
sequence_button3.direction = Direction.INPUT
sequence_button3.pull = Pull.UP

sequence_button4 = DigitalInOut(SEQUENCER_BUTTON_PINS[3])
sequence_button4.direction = Direction.INPUT
sequence_button4.pull = Pull.UP

# Transmit Button (Morse Code Module)
transmit_button = DigitalInOut(TRANSMIT_BUTTON_PIN)
transmit_button.direction = Direction.INPUT
transmit_button.pull = Pull.UP

# Neopixels
neopixels = neopixel.NeoPixel(NEOPIXEL_PIN, 6, brightness=2)

# TFT Display
displayio.release_displays()

spi = busio.SPI(
    clock=DISPLAY2_SCK_PIN,
    MOSI=DISPLAY2_MOSI_PIN
)

while not spi.try_lock():
    pass

spi.configure(baudrate=24_000_000)
spi.unlock()

display_bus = FourWire(spi,
    command=DISPLAY2_DC_PIN,
    chip_select=DISPLAY2_CS_PIN,
    reset=DISPLAY2_RST_PIN
)

display2 = ST7789(display_bus,
    width=240, height=320,
    rowstart=0, colstart=0,
    bgr=True, invert=False
)

screen = displayio.Group()
display2.root_group = screen


# ---------------- Other Config ----------------
Alive = True
Completed = [0, 0, 0, 0, 0]  # Tracks completion of each sequence

COLORS = {
    "RED": (255, 0, 0),
    "YELLOW": (255, 255, 0),
    "GREEN": (0, 255, 0),
    "CYAN": (0, 255, 255),
    "BLUE": (0, 0, 255),
    "PURPLE": (180, 0, 255),
    "WHITE": (255, 255, 255),
    "OFF": (0, 0, 0)
}

tick_sound = audiocore.WaveFile(open("/assets/tick.wav", "rb"))
explosion_sound = audiocore.WaveFile(open("/assets/explosion.wav", "rb"))

color_sequences = [
    ["RED", "BLUE", "GREEN", "YELLOW"],
    ["YELLOW", "RED", "BLUE", "GREEN"],
    ["BLUE", "GREEN", "YELLOW", "RED"],
    ["GREEN", "YELLOW", "RED", "BLUE"],
    ["RED", "RED", "BLUE", "YELLOW"]
]

last_second_tick = 0.0
last_accel_update = 0.0
last_acceleration = None
STRIKE_THRESHOLD = 15.0 # m/s^2, gravity is ~9.8. Adjust for sensitivity.

MORSE_CODE = { 'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.',
               'F':'..-.', 'G':'--.', 'H':'....', 'I':'..', 'J':'.---',
               'K':'-.-', 'L':'.-..', 'M':'--', 'N':'-.', 'O':'---',
               'P':'.--.', 'Q':'--.-', 'R':'.-.', 'S':'...', 'T':'-',
               'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-', 'Y':'-.--',
               'Z':'--..'}
MORSE_WORDS = ["SHELL", "HALLS", "SLICK", "TRICK", "BOXES", "LEAKS", "STROBE",
               "BISTRO", "FLICK", "BOMBS", "BREAK", "BRICK", "STEAK", "STING",
               "VECTOR", "BEATS"]

# Morse Code Module State
morse_state = "IDLE"
morse_word_to_send = ""
morse_char_index = 0
morse_signal_index = 0
morse_last_time = 0.0
morse_time_unit = 0.25 # seconds for one dot

# ---------------- Main Loop ----------------
while Alive:
    now = time.monotonic()

    # --- MODULE: Morse Code ---
    # The potentiometer is not used in this implementation but its value can be read via:
    # potentiometer.snapped_value or potentiometer.value

    # Pressing the transmit button starts or restarts the sequence for a new word
    if not transmit_button.value:
        # Only trigger on a new press
        if morse_state == "IDLE":
            # Select a random word from the list.
            if MORSE_WORDS:
                morse_word_to_send = random.choice(MORSE_WORDS)
                print(f"Morse word to transmit: {morse_word_to_send}")

                # Clear previous text and display the new word
                while len(screen) > 0:
                    screen.pop()
                text_area = label.Label(
                    terminalio.FONT,
                    text=morse_word_to_send,
                    color=0xFFFFFF,
                    scale=3
                )
                text_area.x = display2.width // 2 - text_area.bounding_box[2] // 2
                text_area.y = display2.height // 2
                screen.append(text_area)

                morse_state = "START_SEQUENCE"
                morse_char_index = 0
                morse_signal_index = 0
                morse_last_time = now

    if morse_state != "IDLE":
        # If button is released, allow re-triggering
        if transmit_button.value and morse_state == "START_SEQUENCE" and (now - morse_last_time) < 0.1:
            pass  # Debounce/wait for release

        if morse_state == "START_SEQUENCE":
            neopixels[0] = COLORS["BLUE"]
            if (now - morse_last_time) >= 1.0:  # Blue light for 1 second
                neopixels[0] = COLORS["OFF"]
                morse_state = "LETTER_GAP"  # Start with a gap before the first letter
                morse_last_time = now

        elif morse_state == "LETTER_GAP":
            if (now - morse_last_time) >= (3 * morse_time_unit):
                if morse_char_index >= len(morse_word_to_send):
                    morse_state = "IDLE"  # Word finished
                    # Clear the text from the screen
                    while len(screen) > 0:
                        screen.pop()
                else:
                    morse_state = "SIGNAL"
                    morse_signal_index = 0
                morse_last_time = now

        elif morse_state == "SIGNAL_GAP":
            if (now - morse_last_time) >= morse_time_unit:
                morse_signal_index += 1
                morse_state = "SIGNAL"
                morse_last_time = now

        elif morse_state == "SIGNAL":
            char = morse_word_to_send[morse_char_index]
            if char not in MORSE_CODE:  # Skip unknown characters
                morse_char_index += 1
                morse_state = "LETTER_GAP"
            else:
                morse_pattern = MORSE_CODE[char]
                if morse_signal_index >= len(morse_pattern):
                    morse_char_index += 1
                    morse_state = "LETTER_GAP"
                else:
                    signal = morse_pattern[morse_signal_index]
                    if signal == '.':
                        morse_state = "DOT"
                    else:  # signal == '-'
                        morse_state = "DASH"
            morse_last_time = now

        elif morse_state == "DOT":
            neopixels[0] = COLORS["WHITE"]
            if (now - morse_last_time) >= morse_time_unit:
                neopixels[0] = COLORS["OFF"]
                morse_state = "SIGNAL_GAP"
                morse_last_time = now

        elif morse_state == "DASH":
            neopixels[0] = COLORS["WHITE"]
            if (now - morse_last_time) >= (3 * morse_time_unit):
                neopixels[0] = COLORS["OFF"]
                morse_state = "SIGNAL_GAP"
                morse_last_time = now

    # Other logic here - accelerometer updates, button presses, etc.

    # Update timer display every second and play tick sound
    if countdown_time > 0 and (now - last_second_tick) >= 1.0:
        minutes, seconds = divmod(countdown_time, 60)
        display1.numbers(minutes, seconds, countdown_time % 2 == 0)

        audio_out.play(tick_sound)

        # Wait for the sound to finish
        while audio_out.playing:
            pass

        countdown_time -= 1
        last_second_tick = now

    elif countdown_time == 0 and (now - last_second_tick) >= 1.0:
        Alive = False


display1.numbers(00000, False)
audio_out.play(explosion_sound)

while audio_out.playing:
    pass
