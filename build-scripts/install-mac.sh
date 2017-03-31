#!/usr/bin/env bash

#Install and check python
brew install python3
#Install kivy dependencies
brew install --build-bottle sdl2 sdl2_image sdl2_ttf sdl2_mixer
pip3 install -I Cython==0.23

#Install pyinstaller and upx
brew install upx
pip3 install pyinstaller

#Install kivy master branch
USE_OSX_FRAMEWORKS=0 pip3 install https://github.com/kivy/kivy/archive/master.zip