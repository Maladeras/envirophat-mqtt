#!/bin/bash

apt-get -q update
apt-get -qy install --no-install-recommends ca-certificates python python-pip python-smbus python-dev gcc python-setuptools
apt-get -qy clean all

pip install wheel
pip install rpi.gpio
pip install influxdb
pip install envirophat



./monitor.py

