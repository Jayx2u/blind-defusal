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
countdown_time = 300
strikes = 0

# ---------------- Debug Modes ----------------
Debug = False
IgnoreBABRule = False

# ---------------- GPIO pins ----------------

# Display
DISPLAY2_SCK_PIN = board.GP2
DISPLAY2_MOSI_PIN = board.GP3
DISPLAY2_MISO_PIN = board.GP4
DISPLAY2_CS_PIN = board.GP5
DISPLAY2_RST_PIN = board.GP6
DISPLAY2_DC_PIN = board.GP7

DISPLAY1_DIO_PIN = board.GP26
DISPLAY1_CLK_PIN = board.GP27

# BAB Module
BIG_BUTTON_PIN = board.GP8
BIG_BUTTON_LED_PIN = board.GP0

# Gyro Needy Module
ACCELEROMETER_SDA_PIN = board.GP12
ACCELEROMETER_SCL_PIN = board.GP13

# RBG LEDs
NEOPIXEL_PIN = board.GP15

# Speakers
AUDIO_SCK_PIN = board.GP16
AUDIO_WS_PIN = board.GP17
AUDIO_SD_PIN = board.GP18

# Power Sequencer Module
SEQUENCER_BUTTON_PINS = [board.GP19, board.GP20, board.GP21, board.GP22]

# Morse Code Module
POTENTIOMETER_PIN = board.GP28
TRANSMIT_BUTTON_PIN = board.GP10


# ---------------- Helper Classes/Functions ----------------
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

def all_other_modules_solved():
    """Checks if all non-needy, non-BAB modules are solved."""
    return (morse_state == "SOLVED" and
            sequencer_state == "SOLVED")

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

sequence_button1 = DigitalInOut(SEQUENCER_BUTTON_PINS[3])
sequence_button1.direction = Direction.INPUT
sequence_button1.pull = Pull.UP

sequence_button2 = DigitalInOut(SEQUENCER_BUTTON_PINS[2])
sequence_button2.direction = Direction.INPUT
sequence_button2.pull = Pull.UP

sequence_button3 = DigitalInOut(SEQUENCER_BUTTON_PINS[1])
sequence_button3.direction = Direction.INPUT
sequence_button3.pull = Pull.UP

sequence_button4 = DigitalInOut(SEQUENCER_BUTTON_PINS[0])
sequence_button4.direction = Direction.INPUT
sequence_button4.pull = Pull.UP

# Transmit Button (Morse Code Module)
transmit_button = DigitalInOut(TRANSMIT_BUTTON_PIN)
transmit_button.direction = Direction.INPUT
transmit_button.pull = Pull.UP

# Neopixels
neopixels = neopixel.NeoPixel(NEOPIXEL_PIN, 5, brightness=0.2)

# BAB LED
big_button_led = DigitalInOut(BIG_BUTTON_LED_PIN)
big_button_led.direction = Direction.OUTPUT

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
    width=320, height=240,
    rotation=90,
    rowstart=0, colstart=0,
    bgr=True, invert=False
)

# screen = displayio.Group()
screen = displayio.CIRCUITPYTHON_TERMINAL # For Debugging
display2.root_group = screen


# ---------------- Other Config ----------------
Alive = True
game_started = False
game_disarmed = False
Completed = [0, 0, 0, 0, 0]  # Tracks completion of each sequence

# --- IDENTIFICATION: Serial Number ---
possible_serial_numbers = ["SN48K2", "FRQ1A3"]
serial_number = random.choice(possible_serial_numbers)
chosen_serial_index = possible_serial_numbers.index(serial_number)
print(f"Serial Number: {serial_number}")

# --- IDENTIFICATION: Battery ---
num_batteries = random.randint(1, 4)
print(f"Batteries: {num_batteries}")

# Sounds
tick_sound = audiocore.WaveFile(open("/assets/tick.wav", "rb"))
explosion_sound = audiocore.WaveFile(open("/assets/explosion.wav", "rb"))

# Wire Pulling Module
WIRE_PULLING_PINS = [board.GP9, board.GP11, board.GP14, board.GP23, board.GP24, board.GP25]

COLORS = {
    "RED": (255, 0, 0),
    "YELLOW": (255, 255, 0),
    "GREEN": (0, 255, 0),
    "CYAN": (0, 255, 255),
    "BLUE": (0, 0, 255),
    "PURPLE": (180, 0, 255),
    "WHITE": (255, 255, 255),
    "BLACK": (1, 1, 1),  # Using a very dim white for "black"
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
morse_time_unit = 0.5 # seconds for one dot

# Power Sequencer Module State
sequencer_state = "IDLE"  # IDLE, STARTING, SHOW_SEQUENCE, AWAIT_INPUT, SOLVED
sequencer_sequence = []
sequencer_correct_presses = []
sequencer_user_presses = []
sequencer_color_index = 0
sequencer_last_flash_time = 0.0
sequencer_flash_interval = 0.75 # seconds

# Wire Pulling Buttons
wire_buttons = []
for pin in WIRE_PULLING_PINS:
    button = DigitalInOut(pin)
    button.direction = Direction.INPUT
    button.pull = Pull.UP
    wire_buttons.append(button)

# Wire Pulling Module State
wire_pulling_state = "STARTING" # STARTING, AWAIT_INPUT, SOLVED, FAILED
wire_pulling_wires = []
wire_pulling_correct_wire_index = -1 # 0-based index

# Wire Pulling Setup Logic
if wire_pulling_state == "STARTING":
    num_wires = random.randint(3, 6)
    wire_colors = ["RED", "BLUE", "YELLOW", "WHITE", "BLACK"]
    wire_pulling_wires = [random.choice(wire_colors) for _ in range(num_wires)]

    # Determine correct wire to pull based on rules
    # Note: Wire indices are 1-based in rules, 0-based in code.
    if num_wires == 3:
        if "RED" not in wire_pulling_wires:
            wire_pulling_correct_wire_index = 1 # Second wire
        elif wire_pulling_wires[-1] == "WHITE":
            wire_pulling_correct_wire_index = 2 # Last wire
        elif wire_pulling_wires.count("BLUE") > 1:
            # Find index of last blue wire
            wire_pulling_correct_wire_index = len(wire_pulling_wires) - 1 - wire_pulling_wires[::-1].index("BLUE")
        else:
            wire_pulling_correct_wire_index = 2 # Last wire
    elif num_wires == 4:
        if wire_pulling_wires.count("RED") > 1 and not serial_last_digit_is_even():
            wire_pulling_correct_wire_index = len(wire_pulling_wires) - 1 - wire_pulling_wires[::-1].index("RED")
        elif wire_pulling_wires[-1] == "YELLOW" and "RED" not in wire_pulling_wires:
            wire_pulling_correct_wire_index = 0 # First wire
        elif wire_pulling_wires.count("BLUE") == 1:
            wire_pulling_correct_wire_index = 0 # First wire
        else:
            wire_pulling_correct_wire_index = 1 # Second wire
    elif num_wires == 5:
        if wire_pulling_wires[-1] == "BLACK" and not serial_last_digit_is_even():
            wire_pulling_correct_wire_index = 3 # Fourth wire
        elif wire_pulling_wires.count("RED") == 1 and wire_pulling_wires.count("YELLOW") > 1:
            wire_pulling_correct_wire_index = 0 # First wire
        elif "BLACK" not in wire_pulling_wires:
            wire_pulling_correct_wire_index = 1 # Second wire
        else:
            wire_pulling_correct_wire_index = 0 # First wire
    elif num_wires == 6:
        if "YELLOW" not in wire_pulling_wires and not serial_last_digit_is_even():
            wire_pulling_correct_wire_index = 2 # Third wire
        elif wire_pulling_wires.count("YELLOW") == 1 and wire_pulling_wires.count("WHITE") > 1:
            wire_pulling_correct_wire_index = 3 # Fourth wire
        elif "RED" not in wire_pulling_wires:
            wire_pulling_correct_wire_index = 5 # Last wire
        else:
            wire_pulling_correct_wire_index = 3 # Fourth wire

    wire_pulling_state = "AWAIT_INPUT"
    print(f"Wires: {wire_pulling_wires}")
    print(f"Correct Wire: {wire_pulling_correct_wire_index + 1}")

# Big Ass Button Module State
bab_state = "STARTING"  # STARTING, AWAIT_INPUT, HELD, SOLVED
bab_led_is_on = False
bab_correct_action = "" # "PRESS" or "HOLD"
bab_hold_strip_color = "" # "BLUE", "YELLOW", "OTHER"
bab_release_digit = -1

# Big Ass Button Setup Logic
if bab_state == "STARTING":
    # Randomize bomb features for this module
    bab_led_is_on = random.choice([True, False])
    big_button_led.value = bab_led_is_on

    # Determine correct action based on rules
    if bab_led_is_on and num_batteries > 2:
        bab_correct_action = "PRESS"
    elif not bab_led_is_on and num_batteries > 1:
        bab_correct_action = "HOLD"
    elif bab_led_is_on and serial_has_vowel():
        bab_correct_action = "PRESS"
    else:
        bab_correct_action = "HOLD"

    # If holding, determine release rule
    if bab_correct_action == "HOLD":
        # Randomize the color of the "big display" for the release cue
        hold_color_choice = random.choice(["BLUE", "YELLOW", "WHITE", "GREEN", "RED"]) # Using a sample for "OTHER"
        if hold_color_choice == "BLUE":
            bab_hold_strip_color = "BLUE"
            bab_release_digit = 4
        elif hold_color_choice == "YELLOW":
            bab_hold_strip_color = "YELLOW"
            bab_release_digit = 5
        else:
            bab_hold_strip_color = hold_color_choice # Any other color
            bab_release_digit = 1

    bab_state = "AWAIT_INPUT"
    print(f"BAB Batteries: {num_batteries}, LED On: {bab_led_is_on}")
    print(f"BAB Action: {bab_correct_action}, Release Color: {bab_hold_strip_color}, Release Digit: {bab_release_digit}")

# Display and logging settings
pot_check_interval = 0.2  # seconds
last_pot_check_time = 0.0
pot_text_label = None
wire_text_label = None

# Create the display group first
screen = displayio.Group()

# Disarmed Display Group
disarm_screen = displayio.Group()
disarm_label = label.Label(
    terminalio.FONT, text="DISARMED", color=COLORS["GREEN"], scale=5,
    anchor_point=(0.5, 0.5), anchored_position=(display2.width // 2, display2.height // 2)
)
disarm_screen.append(disarm_label)

# Explosion Display Group
explosion_screen = displayio.Group()
explosion_label = label.Label(
    terminalio.FONT, text="YOU DIE :c", color=COLORS["RED"], scale=5,
    anchor_point=(0.5, 0.5), anchored_position=(display2.width // 2, display2.height // 2)
)
explosion_screen.append(explosion_label)


# Serial Number Label (always on)
serial_display_text = serial_number
if Debug:
    serial_display_text = f"Serial {chosen_serial_index + 1}"

serial_label = label.Label(
    terminalio.FONT, text=serial_display_text, color=0xFFFFFF, scale=2,
    anchor_point=(0.0, 0.0), anchored_position=(5, 5)
)
screen.append(serial_label)

# Battery Count Label (always on)
battery_display_text = f"{num_batteries} BATTERIES"
battery_label = label.Label(
    terminalio.FONT, text=battery_display_text, color=0xFFFFFF, scale=2,
    anchor_point=(0.0, 0.0), anchored_position=(5, 35)
)
screen.append(battery_label)


if Debug:
    # In debug mode, we will show the terminal on the display
    # Note: The labels added above will not be visible if the terminal takes over.
    screen = displayio.CIRCUITPYTHON_TERMINAL
else:
    # In normal mode, add the other module info labels
    # Potentiometer Frequency Label
    pot_text_label = label.Label(
        terminalio.FONT, text="", color=0xFFFF00, scale=2,
        anchor_point=(1.0, 0.0), anchored_position=(display2.width - 5, 5)
    )
    screen.append(pot_text_label)

    # Wire Pulling Module Label
    # wire_info_text = f"{len(wire_pulling_wires)} Wires: " + " ".join(w[0] for w in wire_pulling_wires)
    # wire_text_label = label.Label(
    #     terminalio.FONT, text=wire_info_text, color=0x00FFFF, scale=2,
    #     anchor_point=(0.5, 1.0), anchored_position=(display2.width // 2, display2.height - 10)
    # )
    #screen.append(wire_text_label)

    # Logo Label
    logo_info_text = "Blind Defusal"
    logo_text_label = label.Label(
        terminalio.FONT, text=logo_info_text, color=0x00FFFF, scale=2,
        anchor_point=(0.5, 1.0), anchored_position=(display2.width // 2, display2.height - 10)
    )
    screen.append(logo_text_label)

display2.root_group = screen


if Debug:
    # In debug mode, we will show the terminal on the display
    # Note: The labels added above will not be visible if the terminal takes over.
    screen = displayio.CIRCUITPYTHON_TERMINAL
else:
    # In normal mode, add the other module info labels
    # Potentiometer Frequency Label
    pot_text_label = label.Label(
        terminalio.FONT, text="", color=0xFFFF00, scale=2,
        anchor_point=(1.0, 0.0), anchored_position=(display2.width - 5, 5)
    )
    screen.append(pot_text_label)

    # Wire Pulling Module Label
    # wire_info_text = f"{len(wire_pulling_wires)} Wires: " + " ".join(w[0] for w in wire_pulling_wires)
    # wire_text_label = label.Label(
    #     terminalio.FONT, text=wire_info_text, color=0x00FFFF, scale=2,
    #     anchor_point=(0.5, 1.0), anchored_position=(display2.width // 2, display2.height - 10)
    # )
    # screen.append(wire_text_label)

display2.root_group = screen

# Reset Neopixels
neopixels[1] = COLORS["OFF"]

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
            neopixels[1] = COLORS["GREEN"]
            print("Correct! Module solved.")
        else:
            strikes += 1
            print(f"Incorrect. Strikes: {strikes}")
        time.sleep(0.2)  # Debounce

    # Morse code state machine
    if morse_state not in ["IDLE", "SOLVED"]:
        if morse_state == "START_SEQUENCE":
            neopixels[1] = COLORS["BLUE"]
            if (now - morse_last_time) >= 1.0:
                neopixels[1] = COLORS["OFF"]
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
            neopixels[1] = COLORS["WHITE"]
            if (now - morse_last_time) >= morse_time_unit:
                neopixels[1] = COLORS["OFF"]
                morse_state = "SIGNAL_GAP"
                morse_last_time = now

        elif morse_state == "DASH":
            neopixels[1] = COLORS["WHITE"]
            if (now - morse_last_time) >= (3 * morse_time_unit):
                neopixels[1] = COLORS["OFF"]
                morse_state = "SIGNAL_GAP"
                morse_last_time = now

    # --- MODULE: Power Sequencer ---
    # The LED at neopixels[0] will flash a sequence of colors.
    # The user must press the correct buttons based on the sequence and serial number.

    if sequencer_state != "SOLVED":
            # State: IDLE -> Wait for the user to start the sequence
            if sequencer_state == "IDLE":
                if not sequence_button1.value:
                    print("Sequencer started by user.")
                    sequencer_state = "STARTING"
                    time.sleep(0.2)  # Debounce

            # State: STARTING -> Initialize the module
            elif sequencer_state == "STARTING":
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

            # State: SHOW_SEQUENCE -> Flash the colors in a loop
            elif sequencer_state == "SHOW_SEQUENCE":
                if (now - sequencer_last_flash_time) >= sequencer_flash_interval:
                    if sequencer_color_index < len(sequencer_sequence):
                        color_name = sequencer_sequence[sequencer_color_index]
                        neopixels[0] = COLORS[color_name]
                        sequencer_color_index += 1
                    else:
                        # Sequence finished, loop back to the start after a pause
                        neopixels[0] = COLORS["OFF"]
                        sequencer_color_index = 0
                    sequencer_last_flash_time = now

                # Check for button presses while the sequence is showing
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
                            sequencer_user_presses = []  # Reset on incorrect press

                        # Check for completion
                        elif len(sequencer_user_presses) == len(sequencer_correct_presses):
                            print("Correct! Sequencer solved.")
                            sequencer_state = "SOLVED"
                            neopixels[0] = COLORS["GREEN"]

                        time.sleep(0.2)  # Debounce
                        break  # Process one button at a time

    # --- MODULE: Wire Pulling ---

    if wire_pulling_state == "AWAIT_INPUT":
        for i, button in enumerate(wire_buttons):
            # Only check buttons that correspond to an existing wire
            if i < len(wire_pulling_wires) and not button.value:
                print(f"Wire {i + 1} pulled.")
                if i == wire_pulling_correct_wire_index:
                    print("Correct! Wire module solved.")
                    wire_pulling_state = "SOLVED"
                    if wire_text_label is not None:
                        wire_text_label.text = "Wires: SOLVED"
                        wire_text_label.color = COLORS["GREEN"]
                else:
                    print("Incorrect wire! Strike. Module disabled.")
                    strikes += 1
                    wire_pulling_state = "FAILED"
                    if wire_text_label is not None:
                        wire_text_label.text = "Wires: FAILED"
                        wire_text_label.color = COLORS["RED"]
                time.sleep(0.2)  # Debounce
                break

        # --- MODULE: Big Ass Button ---

        if bab_state in ["AWAIT_INPUT", "HELD"]:
            # --- Press Detection ---
            if bab_state == "AWAIT_INPUT" and not big_button.value:
                # If the game hasn't started, this first press just starts the timer.
                if not game_started:
                    print("Timer Started!")
                    game_started = True
                    last_second_tick = now  # Start the timer tick
                    time.sleep(0.2)  # Debounce
                # If the game has already started, this press is an attempt to solve the module.
                else:
                    if not all_other_modules_solved() and not IgnoreBABRule:
                        print("FATAL: Big button pressed too early!")
                        strikes = 99  # Immediate detonation
                        Alive = False
                    elif bab_correct_action == "PRESS":
                        print("Correct! BAB module solved.")
                        bab_state = "SOLVED"
                        game_disarmed = True
                        display2.root_group = disarm_screen
                    else:  # Correct action was "HOLD"
                        print("Button held. Look at the display for release time.")
                        bab_state = "HELD"
                        if Debug:
                            print(f"DEBUG: Release on digit {bab_release_digit}")
                        else:
                            # Change display background color
                            bg_color = COLORS.get(bab_hold_strip_color, COLORS["WHITE"])
                            bg_bitmap = displayio.Bitmap(display2.width, display2.height, 1)
                            bg_palette = displayio.Palette(1)
                            bg_palette[0] = bg_color
                            bg_sprite = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette, x=0, y=0)
                            screen.insert(0, bg_sprite)

                    time.sleep(0.2)  # Debounce

            # --- Release Detection ---
            elif bab_state == "HELD" and big_button.value:
                # The time the user saw on the display before releasing.
                # We add 1 because countdown_time was already decremented for the next tick.
                time_on_display = countdown_time + 1
                minutes, seconds = divmod(time_on_display, 60)
                time_str_on_display = f"{minutes:02d}{seconds:02d}"

                if str(bab_release_digit) in time_str_on_display:
                    print(f"Correct release at {minutes:02d}:{seconds:02d}! BOMB DISARMED.")
                    bab_state = "SOLVED"
                    game_disarmed = True
                    display2.root_group = disarm_screen

                else:
                    minutes, seconds = divmod(time_on_display, 60)
                    print(f"Incorrect release at {minutes:02d}:{seconds:02d}! Strike.")
                    strikes += 1
                    # Revert display background
                    if not Debug and len(screen) > 3:  # Check if bg is present
                        screen.pop(0)

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

    # --- Strike Indicator Lights ---
    if strikes >= 1:
        neopixels[2] = COLORS["RED"]
    if strikes >= 2:
        neopixels[3] = COLORS["RED"]
    if strikes >= 3:
        neopixels[4] = COLORS["RED"]
        Alive = False
        display2.root_group = explosion_screen

    # Update timer display every second and play tick sound
    if game_started and not game_disarmed and countdown_time > 0 and (now - last_second_tick) >= 1.0:
        minutes, seconds = divmod(countdown_time, 60)
        display1.numbers(minutes, seconds, countdown_time % 2 == 0)

        audio_out.play(tick_sound)

        # Wait for the sound to finish
        while audio_out.playing:
            pass

        countdown_time -= 1
        last_second_tick = now

    elif game_started and not game_disarmed and countdown_time == 0 and (now - last_second_tick) >= 1.0:
        Alive = False
        display2.root_group = explosion_screen



display1.numbers(00000, False)
audio_out.play(explosion_sound)

while audio_out.playing:
    pass
