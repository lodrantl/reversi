#!/usr/bin/env bash
set -ev #echo on

export PYENV_VERSION=$PYTHON
export PYTHON_CONFIGURE_OPTS="--enable-framework"

# See https://docs.travis-ci.com/user/osx-ci-environment/#A-note-on-upgrading-packages.
brew outdated pyenv || brew upgrade pyenv

pyenv install $PYENV_VERSION
eval "$(pyenv init -)"

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

#Workaround for https://github.com/travis-ci/travis-ci/issues/6522
#Turn off exit on failure.
set +ev