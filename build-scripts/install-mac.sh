#!/usr/bin/env bash

#Install and check python
brew install python3@3.5.2

#Install kivy dependencies
brew install sdl2 sdl2_image sdl2_ttf sdl2_mixer gstreamer
pip3 install -I Cython==0.23

#Install pyinstaller
pip3 install pyinstaller

#Install kivy master branch
USE_OSX_FRAMEWORKS=0 pip3 install https://github.com/kivy/kivy/archive/master.zip