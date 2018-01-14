#!/bin/bash

set -euo pipefail

INSTALL_DIR="/opt/zpui"

if test "$EUID" -ne 0
then
   echo "This script must be run as root, exiting..."
   exit 1
fi

test -f config.json || cp default_config.json config.json

apt-get install \
  libjpeg-dev \
  nmap
  python \
  python-dev \
  python-pip \
  python-pygame \
  python-serial \
  python-smbus \
  python-systemd

pip2 install -r requirements.txt

mkdir -p "$INSTALL_DIR"

cp ./. "$INSTALL_DIR" -R

cd "$INSTALL_DIR"

cp zpui.service /etc/systemd/system/

systemctl daemon-reload
systemctl enable zpui.service
systemctl start zpui.service
