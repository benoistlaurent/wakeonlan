wakeonlan
#########

Wake-up computers using wakeonlan protocol.


Usage
=====

After setting-up the target computer BIOS properly, the program uses a
configuration file from which is read every machine that should be awaken
and the appropriate parameters:

::

    usage: wakeonlan.py [-h] [-c CONFIG]

    Wake machines from LAN.

    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            configuration file (default:
                            '/Users/benoist/.wakeonlan.cfg')

Credits
=======

Authors:

* Benoist LAURENT


This package has been heavily inspired by `pywakeonlan`_.


.. _pywakeonlan: https://github.com/remcohaszing/pywakeonlan