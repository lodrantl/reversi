#!/usr/bin/env bash
set -x #echo on

#Install and check python
brew update
# Per the `pyenv homebrew recommendations <https://github.com/yyuu/pyenv/wiki#suggested-build-environment>`_.
brew install openssl readline
# See https://docs.travis-ci.com/user/osx-ci-environment/#A-note-on-upgrading-packages.
# I didn't do this above because it works and I'm lazy.
brew outdated pyenv || brew upgrade pyenv

pyenv install $PYENV_VERSION

# I would expect something like ``pyenv init; pyenv local $PYTHON`` or
# ``pyenv shell $PYTHON`` would work, but ``pyenv init`` doesn't seem to
# modify the Bash environment. ??? So, I hand-set the variables instead.
export PYENV_VERSION=$PYTHON
pyenv init

# A manual check that the correct version of Python is running.
python --version

# Upgrade pip
python -m pip install --upgrade pip virtualenv setuptools

#Install kivy dependencies
brew install --build-bottle sdl2 sdl2_image sdl2_ttf sdl2_mixer
python -m pip install -I Cython==0.23

#Install pyinstaller and upx
brew install upx
python -m pip install pyinstaller

#Install kivy master branch
USE_OSX_FRAMEWORKS=0 python -m pip install https://github.com/kivy/kivy/archive/master.zip

#Build executable files
python -m PyInstaller reversi.spec