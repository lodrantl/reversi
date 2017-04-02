#!/usr/bin/env bash
set -ev #echo on

export PYENV_VERSION=$PYTHON
export PYTHON_CONFIGURE_OPTS="--enable-shared"

# Per the `pyenv homebrew recommendations <https://github.com/yyuu/pyenv/wiki#suggested-build-environment>`_.
brew install openssl readline

# See https://docs.travis-ci.com/user/osx-ci-environment/#A-note-on-upgrading-packages.
# I didn't do this above because it works and I'm lazy.
brew outdated pyenv || brew upgrade pyenv

pyenv install $PYENV_VERSION
export PATH="/Users/travis/.pyenv/shims:${PATH}"

# A manual check that the correct version of Python is running.
python --version

# Upgrade pip
python -m pip install --upgrade pip virtualenv setuptools

#Install kivy dependencies
brew install --build-bottle sdl2 sdl2_image sdl2_ttf sdl2_mixer
python -m pip install -I Cython==0.23

#Install pyinstaller and upx
brew install upx
python -m pip install pyinstaller pytest

#Install kivy master branch
USE_OSX_FRAMEWORKS=0 python -m pip install https://github.com/kivy/kivy/archive/master.zip

#Build executable files
python -m PyInstaller reversi.spec