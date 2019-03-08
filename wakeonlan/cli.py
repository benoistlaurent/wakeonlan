
"""Wake machines from LAN."""


import argparse
import os

import yaml

import wakeonlan


def read_yml_config(path):
    """Read YAML formatted configuration file.

    Args:
        path (str): path to configuration file to read

    Returns:
        dict: machines with attributes

    """
    with open(path, 'rt') as f:
        data = yaml.load(f.read(), Loader=yaml.Loader)
    # Machines are entries with a 'mac' attribute
    data = {machine: desc for machine, desc in data.items() if 'mac' in desc}
    return data


def parse_command_line():
    """Command-line parsing.

    Configuration file can be passed using the -c/--config option.
    Default configuration file is $HOME/.wakeonlan.cfg.

    Returns:
        argparse.Namespace: arguments

    Raises:
        argparse.ArgumentError: if configuration file does not exists

    """
    parser = argparse.ArgumentParser(description=__doc__)
    cfg_arg = parser.add_argument('config', help="YAML configuration file")
    parser.add_argument('machine', nargs='*', help='machines to reboot',
                        default=['all'])
    parser.add_argument('--version', action='version',
                        version=wakeonlan.__version__)
    args = parser.parse_args()
    if not os.path.isfile(args.config):
        err = "invalid configuration file: '{}'".format(args.config)
        raise argparse.ArgumentError(cfg_arg, err)
    return args


def main():
    """Run wakeonlan as a CLI application."""
    args = parse_command_line()
    config = read_yml_config(args.config)
    wakeonlan.wakeup(config, args.machine)


if __name__ == '__main__':
    main()
