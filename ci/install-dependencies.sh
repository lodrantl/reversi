#!/usr/bin/env bash
set -ev #echo on

if [[ $TRAVIS_OS_NAME == "osx" ]]; then
    export PYENV_VERSION=$PYTHON
    export PYTHON_CONFIGURE_OPTS="--enable-shared"

    # See https://docs.travis-ci.com/user/osx-ci-environment/#A-note-on-upgrading-packages.
    brew outdated pyenv || brew upgrade pyenv
https://github.com/lodrantl/reversi.git
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
fi

if [[ $TRAVIS_OS_NAME == "linux" ]]; then
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
fi

#Workaround for https://github.com/travis-ci/travis-ci/issues/6522
#Turn off exit on failure.
set +ev
