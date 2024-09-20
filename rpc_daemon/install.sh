#!/usr/bin/env bash 
# TODO: Make this a system service

set -Eeuo pipefail

# yeah, I know. dunno how to do this safely to run in a service though. 
sudo pip3 install ../ --break-system-packages

id -u k3ng_rotator &>/dev/null || sudo useradd -r -s /bin/false k3ng_rotator

sudo mkdir -p /usr/local/lib/k3ng_rotator
sudo cp -f rpc_daemon.py /usr/local/lib/k3ng_rotator/rpc_daemon.py
sudo chmod 655 /usr/local/lib/k3ng_rotator/rpc_daemon.py

sudo cp -f k3ng_rotator.service /etc/systemd/system/k3ng_rotator.service
sudo chown root:root /etc/systemd/system/k3ng_rotator.service
sudo chmod 644 /etc/systemd/system/k3ng_rotator.service

sudo systemctl daemon-reload
sudo systemctl enable k3ng_rotator 
sudo systemctl restart k3ng_rotator 

printf "\nService installed!\n"
