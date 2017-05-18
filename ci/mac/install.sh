#!/usr/bin/env bash
set -ev #echo on

export PYENV_VERSION=$PYTHON
export PYTHON_CONFIGURE_OPTS="--enable-framework"

# See https://docs.travis-ci.com/user/osx-ci-environment/#A-note-on-upgrading-packages.
brew outdated pyenv || brew upgrade pyenv

# Import codesign certificate
export CERTIFICATE_P12=ci/mac/ReversiBundle.p12;
export KEYCHAIN=build.keychain;
openssl aes-256-cbc -K $encrypted_80406b3fc467_key -iv $encrypted_80406b3fc467_iv -in ci/mac/ReversiBundle.p12.enc -out $CERTIFICATE_P12 -d

echo "Create keychain"
security create-keychain -p mysecretpassword $KEYCHAIN;

echo "Importing certificates into $KEYCHAIN"
security import $CERTIFICATE_P12 -k $KEYCHAIN -P reversi -T /usr/bin/codesign;


echo "Unlock keychain"
security unlock-keychain -p mysecretpassword $KEYCHAIN;

echo "Increase keychain unlock timeout"
security set-keychain-settings -lut 7200 $KEYCHAIN;

echo "Add keychain to keychain-list"
security list-keychains -s $KEYCHAIN;
security default-keychain -s $KEYCHAIN;

# Install python
pyenv install $PYENV_VERSION
eval "$(pyenv init -)"

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

#Workaround for https://github.com/travis-ci/travis-ci/issues/6522
#Turn off exit on failure.
set +ev
