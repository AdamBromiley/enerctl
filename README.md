# Enerctl
Transmit control sequences to legacy Energenie 433 MHz radio controlled wall sockets with a Raspberry Pi and ENER314 Pi-mote control board.

## Dependencies
* The Raspberry Pi GPIO module  
`python3 -m pip install RPi.GPIO`

## Usage
### Initialisation
1. Connect the transmitter board to the Raspberry Pi's GPIO pins, ensuring correct alignment.
2. Plug the Energenie radio controlled plug into a wall socket. If using multiple plugs, ensure they are spaced at least 2 metres from each other to limit signal interference.
3. Ensure the unit is in factory state to enable its learning mode.
4. Any valid control code will pair the unit to the respective transmitter. A unit can pair with up to 2 transmitters. The transmitter can control 4 units at once.
5. When a code is accepted, the socket's red LED will flash quickly and then extinguish

### Enerctl console
Enter the console for enerctl with `python3 main.py`. At the prompt, enter a command and hit return. To exit, use `quit`.

Help can be provided with `help`:
```
COMMAND [OPTION]...
Send COMMAND to a legacy Energenie 433 MHz radio controlled wall socket.

Commands:
  cmd SEQUENCE   Send a custom 4-bit binary code to the socket
  off [SOCKET]   Turn SOCKET off
  on [SOCKET]    Turn SOCKET on

Miscellaneous:
  h, help        Display this help message
  q, quit        Exit the console

Omitting the socket number means on/off commands will be accepted by all
sockets within range of the transmitter.

Examples:
  on
  cmd 1001
  off 3
```

### Control codes
The following is a list of 4-bit control codes accepted by the legacy sockets:
```
0011 - All sockets ON
1011 - All sockets OFF

1111 - Socket 1 ON
0111 - Socket 1 OFF

1110 - Socket 2 ON
0110 - Socket 2 OFF

1101 - Socket 3 ON
0101 - Socket 3 OFF

1100 - Socket 4 ON
0100 - Socket 4 OFF
```
