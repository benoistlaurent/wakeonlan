
"""wakeonlan - Top-level package for wakeonline.

Provides functions to wake a machine using the wakeonlan protocol.
"""

__author__ = 'Benoist LAURENT'
__email__ = 'benoist.laurent@ibpc.fr'
__version__ = '1.0.0'

from .wakeonlan import create_magic_packet, send_magic_packet, wakeup

__all__ = ['create_magic_packet', 'send_magic_packet', 'wakeup']
