import RPi.GPIO as GPIO
import time


# BOARD GPIO pins for the ENER314
#   K0     = Encoder input 0
#   K1     = Encoder input 1
#   K2     = Encoder input 2
#   K3     = Encoder input 3
#   MODSEL = Set modulator mode:
#              0 - amplitude-shift keying (ASK)
#              1 - frequency-shift keying (FSK)
#   CE     = Enable modulator
K0 = 11
K1 = 15
K2 = 16
K3 = 13
MODSEL = 18
CE = 22


# 4 sockets can be targetted by the transmitter. A special ID of 5 will be used
# to target all sockets in range (in the case of the on/off commands)
MINIMUM_SOCKET_ID = 1
MAXIMUM_SOCKET_ID = 4
ALL_SOCKETS = 5


# Initialise the GPIO pins
def gpio_init():
    GPIO.setwarnings(False)

    # Use BOARD numbers to address the GPIO pins
    GPIO.setmode(GPIO.BOARD)

    # Set all GPIO pins for output
    GPIO.setup(K0, GPIO.OUT)
    GPIO.setup(K1, GPIO.OUT)
    GPIO.setup(K2, GPIO.OUT)
    GPIO.setup(K3, GPIO.OUT)
    GPIO.setup(MODSEL, GPIO.OUT)
    GPIO.setup(CE, GPIO.OUT)


# Clean up the GPIO session
def gpio_cleanup():
    GPIO.cleanup()


# Enable or disable modulator
def set_modulator_state(state):
    GPIO.output(CE, state)


# Enable modulator
def modulator_on():
    set_modulator_state(True)


# Disable modulator
def modulator_off():
    set_modulator_state(False)


# Set keying mode (ASK/OOK or FSK) of modulator
def set_keying_mode(mode):
    if mode == "ASK":
        GPIO.output(MODSEL, False)
    else:
        GPIO.output(MODSEL, True)


# Send 4-bit code to encoder and transmit
def send_code(k_3=0, k_2=0, k_1=0, k_0=0):
    GPIO.output(K0, k_0)
    GPIO.output(K1, k_1)
    GPIO.output(K2, k_2)
    GPIO.output(K3, k_3)

    # Encoder requires time to settle
    time.sleep(0.1)

    # Enable the modulator for a bit
    modulator_on()
    time.sleep(0.25)
    modulator_off()


# Initialise the transmitter board
def transmitter_init(keying_mode="ASK"):
    modulator_off()
    set_keying_mode(keying_mode)
    send_code()


# Reset the state of the transmitter board
def transmitter_cleanup():
    transmitter_init()


# Turn socket on or off. If socket number is ALL_SOCKETS, the change is
# applied to all
def set_socket_state(socket, state):
    if socket != ALL_SOCKETS:
        if socket > MAXIMUM_SOCKET_ID:
            socket = MAXIMUM_SOCKET_ID
        elif socket < MINIMUM_SOCKET_ID:
            socket = MINIMUM_SOCKET_ID

    control_code = 0b1111 - (socket - 1)

    if not state:
        control_code -= 0b1000

    k_0 = (control_code >> 0) & 1
    k_1 = (control_code >> 1) & 1
    k_2 = (control_code >> 2) & 1
    k_3 = (control_code >> 3) & 1

    send_code(k_3, k_2, k_1, k_0)


# Enable socket
def socket_on(socket=ALL_SOCKETS):
    set_socket_state(socket, True)


# Disable socket
def socket_off(socket=ALL_SOCKETS):
    set_socket_state(socket, False)
