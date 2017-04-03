#!/usr/bin/env bash
set -ev #echo on

#Print Ubuntu version info
sudo lsb_release -a

#Install kivy dependencies via apt
sudo add-apt-repository -y ppa:mc3man/trusty-media
sudo apt-get update
sudo apt-get install -y  build-essential upx-ucl git ffmpeg libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev

# Update pip
pip install --upgrade pip virtualenv setuptools

# Install kivy dependencies
pip install Cython==0.23
pip install pygments docutils pyinstaller

#Install kivy master branch
pip install git+https://github.com/kivy/kivy.git@master

#Workaround for https://github.com/travis-ci/travis-ci/issues/6522
#Turn off exit on failure.
set +ev
