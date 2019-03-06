
"""wakeonlan - Main Module."""

import socket
import struct
import sys

BROADCAST_IP = '255.255.255.255'
DEFAULT_PORT = 9


def create_magic_packet(macaddress):
    """Create a magic packet.

    Magic packet is used to wake up a computer using he wake on lan protocol.
    The packet is constructed from the mac address given as a parameter.

    Args:
        macaddress (str): mac address

    Returns:
        str: magic packet
    """
    if len(macaddress) == 17:
        sep = macaddress[2]
        macaddress = macaddress.replace(sep, '')
    elif len(macaddress) != 12:
        err = "Incorrect MAC address format: '{}'".format(macaddress)
        raise ValueError(err)

    data = b'FFFFFFFFFFFF' + (macaddress * 16).encode()
    send_data = b''

    # Split up the hex values in pack
    for i in range(0, len(data), 2):
        send_data += struct.pack(b'B', int(data[i:i + 2], 16))
    return send_data


def send_magic_packet(macaddress, ip, port):
    """Wake up computer using its mac address.

    Args:
        macaddress (str): mac address of the computer to wake up
        ip (str): host ip address
        port (int): host port
    """
    packet = create_magic_packet(macaddress)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.connect((ip, port))
    sock.send(packet)
    sock.close()


def wakeup(config):
    """Wake up machines with parameters described in `config`.

    Args:
        config (dict): maps machines name and parameters such as mac address.
    """
    for machine, params in config.items():
        do_wakeonline = params.get('wakeonlan', False)
        if do_wakeonline:
            print('waking up {}'.format(machine), file=sys.stderr)
            args = {'macaddress': params['mac'],
                    'ip': BROADCAST_IP,
                    'port': DEFAULT_PORT}
            send_magic_packet(**args)
