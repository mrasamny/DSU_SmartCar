#!/bin/bash
cd ~/Downloads
git clone https://github.com/mrasamny/DSU_SmartCar
cd DSU_SmartCar
sudo python3 setup.py install
cd ..
rm -r DSU_SmartCar