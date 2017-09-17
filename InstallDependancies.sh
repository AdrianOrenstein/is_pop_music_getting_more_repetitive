#!/bin/sh

sudo apt install python3-pip

while read p; do
  sudo -H pip3 install $p
done < pip3_requirements.txt