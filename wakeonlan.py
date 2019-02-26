
"""Wake machines from LAN."""


import argparse
import configparser
import os
import socket
import struct
import sys


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


def parse_command_line():
    """Command-line parsing.

    Configuration file can be passed using the -c/--config option.
    Default configuration file is $HOME/.wakeonlan.cfg.

    Returns:
        argparse.Namespace: arguments

    Raises:
        argparse.ArgumentError: if configuration file does not exists

    """
    default_cfg = os.path.join(os.environ['HOME'], '.wakeonlan.cfg')
    parser = argparse.ArgumentParser(description=__doc__)
    cfg_arg = parser.add_argument(
        '-c', '--config', default=default_cfg,
        help="configuration file (default: '{}')".format(default_cfg),
    )
    parser.add_argument('--version', action='version', version='1.0.0')
    args = parser.parse_args()
    if not os.path.isfile(args.config):
        err = "invalid configuration file: '{}'".format(default_cfg)
        raise argparse.ArgumentError(cfg_arg, err)
    return args


def get_configuration(configfile):
    """Return configuration.

    Configuration parameters are initialized to some default values and
    read from `configfile`.

    Args:
        configfile (str): path to configuration file to read

    Returns:
        configparser.ConfigParser: configuration parser structure

    """
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'BROADCAST_IP': '255.255.255.255',
                         'DEFAULT_PORT': 9}
    config.read(configfile)
    return config


def wakeup(config):
    """Wake up machines with parameters described in `config`.

    Args:
        config (configparser.ConfigParser): configuration parser structure
    """
    def check_unrecognized_arguments(cfg, args):
        for key in cfg:
            if key not in args:
                err = "{}: unrecognized parameter '{}'".format(machine.strip(),
                                                               key)
                raise ValueError(err)

    def cfg_to_kwargs(cfg):
        cfg = dict(cfg.items())
        args = {
            'macaddress': cfg.pop('mac'),
            'ip': cfg.pop('broadcast_ip'),
            'port': int(cfg.pop('default_port')),
        }
        check_unrecognized_arguments(cfg, args)
        return args

    for machine in config.sections():
        if machine != ' DEFAULT ':
            kwargs = cfg_to_kwargs(config[machine])
            print('waking up {}'.format(machine.strip()), file=sys.stderr)
            send_magic_packet(**kwargs)


def main():
    """Run wakeonlan as a CLI application."""
    args = parse_command_line()
    config = get_configuration(args.config)
    wakeup(config)


if __name__ == '__main__':
    main()
