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
strikes = 0

# ---------------- GPIO pins ----------------
DISPLAY2_SCK_PIN = board.GP2
DISPLAY2_MOSI_PIN = board.GP3
DISPLAY2_MISO_PIN = board.GP4
DISPLAY2_CS_PIN = board.GP5
DISPLAY2_RST_PIN = board.GP6
DISPLAY2_DC_PIN = board.GP7

BIG_BUTTON_PIN = board.GP8

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
last_pot_value = 0 # Last potentiometer value

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


# Helper functions for serial number checks
def serial_has_vowel():
    return any(char in "AEIOU" for char in serial_number)


def serial_last_digit_is_even():
    # Find the last digit in the serial number
    last_digit = -1
    for char in serial_number:
        if char.isdigit():
            last_digit = int(char)

    if last_digit == -1:  # No digits in serial
        return False
    return last_digit % 2 == 0

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
neopixels = neopixel.NeoPixel(NEOPIXEL_PIN, 6, brightness=0.5)

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

# screen = displayio.Group()
screen = displayio.CIRCUITPYTHON_TERMINAL # For Debugging
display2.root_group = screen


# ---------------- Other Config ----------------
Alive = True
Completed = [0, 0, 0, 0, 0]  # Tracks completion of each sequence
Debug = False

# Serial Number Generation
possible_serial_numbers = ["SN48K2", "FRQ1A3"]
serial_number = random.choice(possible_serial_numbers)
chosen_serial_index = possible_serial_numbers.index(serial_number)
print(f"Serial Number: {serial_number}")

# Display and logging settings
pot_check_interval = 0.2  # seconds
last_pot_check_time = 0.0
pot_text_label = None

if Debug:
    # In debug mode, the screen shows all print() statements
    screen = displayio.CIRCUITPYTHON_TERMINAL
else:
    # In normal mode, show serial and pot frequency
    screen = displayio.Group()

    # Serial Number Label
    serial_display_text = f"Serial {chosen_serial_index + 1}"
    serial_label = label.Label(
        terminalio.FONT,
        text=serial_display_text,
        color=0xFFFFFF,
        scale=3,
        anchor_point=(0.5, 0.0),
        anchored_position=(display2.width // 2, 10)
    )
    screen.append(serial_label)

    # Potentiometer Frequency Label
    pot_text_label = label.Label(
        terminalio.FONT,
        text="",
        color=0xFFFF00,
        scale=3,
        anchor_point=(0.5, 1.0),
        anchored_position=(display2.width // 2, display2.height - 10)
    )
    screen.append(pot_text_label)

display2.root_group = screen

# Sounds
tick_sound = audiocore.WaveFile(open("/assets/tick.wav", "rb"))
explosion_sound = audiocore.WaveFile(open("/assets/explosion.wav", "rb"))

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

color_sequences = [
    ["RED", "BLUE", "GREEN", "YELLOW"],
    ["YELLOW", "RED", "BLUE", "GREEN"],
    ["BLUE", "GREEN", "YELLOW", "RED"],
    ["GREEN", "YELLOW", "RED", "BLUE"],
    ["RED", "RED", "BLUE", "YELLOW"]
]

# Time and Gyro
last_second_tick = 0.0
last_accel_update = 0.0
last_acceleration = None
STRIKE_THRESHOLD = 15.0 # m/s^2, gravity is ~9.8. Adjust for sensitivity.

# Morse Code Module Config
MORSE_CODE = { 'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.',
               'F':'..-.', 'G':'--.', 'H':'....', 'I':'..', 'J':'.---',
               'K':'-.-', 'L':'.-..', 'M':'--', 'N':'-.', 'O':'---',
               'P':'.--.', 'Q':'--.-', 'R':'.-.', 'S':'...', 'T':'-',
               'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-', 'Y':'-.--',
               'Z':'--..'}
MORSE_WORDS = ["SHELL", "HALLS", "SLICK", "TRICK", "BOXES", "LEAKS", "STROBE",
               "BISTRO", "FLICK", "BOMBS", "BREAK", "BRICK", "STEAK", "STING",
               "VECTOR", "BEATS"]
MORSE_FREQUENCIES = {
    "SHELL": 3505, "HALLS": 3515, "SLICK": 3522, "TRICK": 3532,
    "BOXES": 3535, "LEAKS": 3542, "STROBE": 3545, "BISTRO": 3552,
    "FLICK": 3555, "BOMBS": 3565, "BREAK": 3572, "BRICK": 3575,
    "STEAK": 3582, "STING": 3592, "VECTOR": 3595, "BEATS": 3600
}

morse_correct_frequency = 0

# Morse Code Module State
morse_state = "IDLE"
morse_word_to_send = ""
morse_char_index = 0
morse_signal_index = 0
morse_last_time = 0.0
morse_time_unit = 0.25 # seconds for one dot

# Power Sequencer Module State
sequencer_state = "STARTING"  # STARTING, SHOW_SEQUENCE, AWAIT_INPUT, SOLVED
sequencer_sequence = []
sequencer_correct_presses = []
sequencer_user_presses = []
sequencer_color_index = 0
sequencer_last_flash_time = 0.0
sequencer_flash_interval = 0.75 # seconds

# Reset Neopixels
neopixels[0] = COLORS["OFF"]

# ---------------- Main Loop ----------------
while Alive:
    now = time.monotonic()

    # --- MODULE: Morse Code ---
    # Pressing the transmit button starts the sequence.
    # Once started, the morse code will loop.
    # The user must set the potentiometer to the correct frequency and press the button again to solve.

    # State transition: IDLE -> TRANSMITTING
    if not transmit_button.value and morse_state == "IDLE":
        if MORSE_WORDS:
            morse_word_to_send = random.choice(MORSE_WORDS)
            morse_correct_frequency = MORSE_FREQUENCIES[morse_word_to_send]
            print(f"Word: {morse_word_to_send}\nFreq: {morse_correct_frequency / 1000.0} MHz")

            morse_state = "START_SEQUENCE"
            morse_char_index = 0
            morse_signal_index = 0
            morse_last_time = now
            time.sleep(0.2)  # Debounce

    # State transition: TRANSMITTING -> check answer
    elif not transmit_button.value and morse_state not in ["IDLE", "SOLVED"]:
        selected_freq = potentiometer.snapped_value
        print(f"Submitted: {selected_freq / 1000.0} MHz")
        if selected_freq == morse_correct_frequency:
            morse_state = "SOLVED"
            neopixels[0] = COLORS["GREEN"]
            print("Correct! Module solved.")
        else:
            strikes += 1
            print(f"Incorrect. Strikes: {strikes}")
        time.sleep(0.2)  # Debounce

    # Morse code state machine
    if morse_state not in ["IDLE", "SOLVED"]:
        if morse_state == "START_SEQUENCE":
            neopixels[0] = COLORS["BLUE"]
            if (now - morse_last_time) >= 1.0:
                neopixels[0] = COLORS["OFF"]
                morse_state = "LETTER_GAP"
                morse_last_time = now

        elif morse_state == "LETTER_GAP":
            # Word gap is 7 units, letter gap is 3.
            # The first gap is always a word gap.
            gap_duration = 7 * morse_time_unit if morse_char_index == 0 else 3 * morse_time_unit
            if (now - morse_last_time) >= gap_duration:
                if morse_char_index >= len(morse_word_to_send):
                    # Loop the word by going back to the start sequence
                    morse_char_index = 0
                    morse_signal_index = 0
                    morse_state = "START_SEQUENCE"
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
            morse_pattern = MORSE_CODE[char]
            if morse_signal_index >= len(morse_pattern):
                morse_char_index += 1
                morse_state = "LETTER_GAP"
            else:
                signal = morse_pattern[morse_signal_index]
                morse_state = "DOT" if signal == '.' else "DASH"
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

    # --- MODULE: Power Sequencer ---
    # The LED at neopixels[1] will flash a sequence of colors.
    # The user must press the correct buttons based on the sequence and serial number.

    if sequencer_state != "SOLVED":
            # State: STARTING -> Initialize the module
            if sequencer_state == "STARTING":
                # Randomly choose one of the 5 sequences
                chosen_color_sequence = random.choice(color_sequences)
                sequencer_sequence = ["WHITE"] + chosen_color_sequence  # Prepend WHITE for start signal

                # Determine the correct button press sequence based on rules
                if chosen_color_sequence == color_sequences[0]:  # R-B-G-Y
                    sequencer_correct_presses = [1, 3] if serial_last_digit_is_even() else [2, 4]
                elif chosen_color_sequence == color_sequences[1]:  # Y-R-B-G
                    sequencer_correct_presses = [4, 2, 1] if serial_has_vowel() else [3, 1]
                elif chosen_color_sequence == color_sequences[2]:  # B-G-Y-R
                    sequencer_correct_presses = [2, 4]
                elif chosen_color_sequence == color_sequences[3]:  # G-Y-R-B
                    sequencer_correct_presses = [1, 2, 3, 4]
                elif chosen_color_sequence == color_sequences[4]:  # R-R-B-Y
                    sequencer_correct_presses = [2, 2, 3] if not serial_last_digit_is_even() else [1, 4]

                print(f"Sequencer Correct: {sequencer_correct_presses}")
                sequencer_state = "SHOW_SEQUENCE"
                sequencer_last_flash_time = now

            # State: SHOW_SEQUENCE -> Flash the colors
            elif sequencer_state == "SHOW_SEQUENCE":
                if (now - sequencer_last_flash_time) >= sequencer_flash_interval:
                    if sequencer_color_index < len(sequencer_sequence):
                        color_name = sequencer_sequence[sequencer_color_index]
                        neopixels[1] = COLORS[color_name]
                        sequencer_color_index += 1
                    else:
                        # Sequence finished, turn off LED and wait for input
                        neopixels[1] = COLORS["OFF"]
                        sequencer_state = "AWAIT_INPUT"
                    sequencer_last_flash_time = now

            # State: AWAIT_INPUT -> Check for button presses
            elif sequencer_state == "AWAIT_INPUT":
                buttons = [sequence_button1, sequence_button2, sequence_button3, sequence_button4]
                for i, button in enumerate(buttons):
                    if not button.value:
                        press = i + 1
                        sequencer_user_presses.append(press)
                        print(f"Sequencer pressed: {press}, Current input: {sequencer_user_presses}")

                        # Check if the press was correct so far
                        if sequencer_user_presses != sequencer_correct_presses[:len(sequencer_user_presses)]:
                            print("Incorrect sequence!")
                            strikes += 1
                            sequencer_user_presses = []  # Reset
                            sequencer_color_index = 0  # Replay sequence
                            sequencer_state = "SHOW_SEQUENCE"

                        # Check for completion
                        elif len(sequencer_user_presses) == len(sequencer_correct_presses):
                            print("Correct! Sequencer solved.")
                            sequencer_state = "SOLVED"
                            neopixels[1] = COLORS["GREEN"]

                        time.sleep(0.2)  # Debounce
                        break  # Process one button at a time

    # Other logic here - accelerometer updates, button presses, etc.

    # --- Potentiometer Value Change ---
    if (now - last_pot_check_time) >= pot_check_interval:
        current_pot_value = potentiometer.snapped_value
        if current_pot_value != last_pot_value:
            formatted_freq = f"{current_pot_value / 1000.0} MHz"
            if Debug:
                print(f"Pot: {formatted_freq}")
            elif pot_text_label is not None:
                pot_text_label.text = formatted_freq
            last_pot_value = current_pot_value
        last_pot_check_time = now

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
