Scrolly
=======

This repository provides sample code for a scrollbot from pimoroni_.
The python library scrollphathd_ can be used to control the display.

The bot listens to MQTT messages and events from the BlueDot_ App.
The BlueDot event will only shutdown the robot, while MQTT messages
can be used to control the display. Look into the python documentation
of scrolly for further information: especially to which topic scrolly 
will be listening to.

A simple installation could add a cronjob at reboot:

    @reboot sleep 10 && /usr/bin/python3 /path/to/scrolly/scrolly.py &>> /path/to/logdir/scrolly.log


.. _pimoroni: https://shop.pimoroni.com/products/scroll-bot-pi-zero-w-project-kit
.. _scrollphathd: https://github.com/pimoroni/scroll-phat-hd
.. _BlueDot: https://bluedot.readthedocs.io/en/latest/gettingstarted.html
