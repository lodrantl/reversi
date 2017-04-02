#!/usr/bin/env bash
set -ev #echo on

if [[ $TRAVIS_OS_NAME == "osx" ]]; then
  - python -m pytest
  # Build executables with pyinstaller
  - python -m PyInstaller -y reversi.spec
  # Run tests
  - ls -la dist/
  - ls -la dist/reversi

fi

if [[ $TRAVIS_OS_NAME == "linux" ]]; then
  - python -m pytest
  # Build executables with pyinstaller
  - python -m PyInstaller -y reversi.spec
  # Run tests
  - ls -la dist/
  - ls -la dist/reversi

fi

#Workaround for https://github.com/travis-ci/travis-ci/issues/6522
#Turn off exit on failure.
set +ev
