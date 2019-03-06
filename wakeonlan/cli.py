
"""Wake machines from LAN."""


import argparse
import configparser
import os

from wakeonlan import wakeup


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


def main():
    """Run wakeonlan as a CLI application."""
    args = parse_command_line()
    config = get_configuration(args.config)
    wakeup(config)


if __name__ == '__main__':
    main()
