import sys

from enerctl import *


def usage():
    print("""COMMAND [OPTION]...
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
  off 3""")


def cleanup():
    transmitter_cleanup()
    gpio_cleanup()


def main():
    gpio_init()
    transmitter_init()

    try:
        while True:
            cmd = input("> ")

            cmd = [item.lower() for item in cmd.split()]

            if not cmd:
                continue
            elif ("help" in cmd) or ("h" in cmd):
                usage()
                continue

            base_cmd = cmd.pop(0)

            if base_cmd == "cmd":
                if not cmd:
                    print("ERROR: Control sequence required")
                    continue
                elif len(cmd) > 1:
                    print("ERROR: Too many arguments")
                    continue

                code_str = cmd.pop(0)

                if len(code_str) != 4:
                    print("ERROR: Invalid control sequence")
                    continue

                try:
                    code = int(code_str, 2)
                except ValueError:
                    print("ERROR: Invalid control sequence")
                    continue

                k_0 = (code >> 0) & 1
                k_1 = (code >> 1) & 1
                k_2 = (code >> 2) & 1
                k_3 = (code >> 3) & 1

                send_code(k_3, k_2, k_1, k_0)

                print(f"Control code {code_str} transmitted")
                continue
            elif base_cmd == "quit":
                cleanup()
                sys.exit(0)

            # Default socket ID is 5 (for all)
            sock_id = ALL_SOCKETS

            if cmd:
                try:
                    sock_id = int(cmd.pop(0))
                except ValueError:
                    print("ERROR: Invalid socket ID")
                    continue

                if cmd:
                    print("ERROR: Too many arguments")
                    continue

            if sock_id != ALL_SOCKETS:
                if not MINIMUM_SOCKET_ID <= sock_id <= MAXIMUM_SOCKET_ID:
                    print(f"ERROR: Socket ID ({sock_id}) out of range. Must be {MINIMUM_SOCKET_ID}-{MAXIMUM_SOCKET_ID}")
                    continue

            if base_cmd == "off":
                socket_off(sock_id)

                if sock_id == ALL_SOCKETS:
                    print("All sockets powered off")
                else:
                    print(f"Socket {sock_id} powered off")
            elif base_cmd == "on":
                socket_on(sock_id)

                if sock_id == ALL_SOCKETS:
                    print("All sockets powered on")
                else:
                    print(f"Socket {sock_id} powered on")
            else:
                print(f"ERROR: {base_cmd} is an invalid command")
    except KeyboardInterrupt:
        print("")
        cleanup()


if __name__ == "__main__":
    main()
