#!/usr/bin/env bash
set -ev #echo on

export PYENV_VERSION=$PYTHON
export PYTHON_CONFIGURE_OPTS="--enable-framework"

# See https://docs.travis-ci.com/user/osx-ci-environment/#A-note-on-upgrading-packages.
brew outdated pyenv || brew upgrade pyenv

pyenv install $PYENV_VERSION
eval "$(pyenv init -)"

#Decrypt cert

export CERTIFICATE_P12=ci/mac/ReversiBundle.p12;
export KEYCHAIN=build.keychain;
openssl aes-256-cbc -K $encrypted_63872960bbdb_key -iv $encrypted_63872960bbdb_iv -in ci/mac/ReversiBundle.p12.enc -out $CERTIFICATE_OSX_P12 -d

pwd
ls -la
ls -la ci
ls -la ci/mac

security create-keychain -p mysecretpassword $KEYCHAIN;
security default-keychain -s $KEYCHAIN;
security unlock-keychain -p mysecretpassword $KEYCHAIN;
security import $CERTIFICATE_P12 -k $KEYCHAIN -P reversi -T /usr/bin/codesign;

# A manual check that the correct version of Python is running.
python --version

# Upgrade pip
python -m pip install --upgrade pip virtualenv setuptools

#Install kivy dependencies
brew install --build-bottle pkg-config sdl2 sdl2_image sdl2_ttf sdl2_mixer
python -m pip install -I Cython==0.23

#Install pyinstaller and upx
brew install upx
python -m pip install pyinstaller pytest

#Install kivy master branch
#USE_OSX_FRAMEWORKS=0 python -m pip install https://github.com/kivy/kivy/archive/master.zip

#Install kivy stable
USE_OSX_FRAMEWORKS=0 python -m pip install kivy

#Prepare codesign certificate



#Workaround for https://github.com/travis-ci/travis-ci/issues/6522
#Turn off exit on failure.
set +ev
