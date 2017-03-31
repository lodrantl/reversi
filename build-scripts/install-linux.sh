#!/usr/bin/env bash

#Print Ubuntu version info
sudo lsb_release -a

#Install kivy dependencies
sudo add-apt-repository -y ppa:mc3man/trusty-media
sudo apt-get update
sudo apt-get install -y  build-essential  git ffmpeg libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev
pip3 install --upgrade pip virtualenv setuptools
pip3 install Cython
pip3 install pygments docutils pyinstaller

#Install kivy master branch
pip3 install git+https://github.com/kivy/kivy.git@master