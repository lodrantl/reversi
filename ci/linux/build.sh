#!/usr/bin/env bash
set -ev #echo on

python -m pytest
# Build executables with pyinstaller
python -m PyInstaller -y reversi.spec

# Move to final dir
mkdir dist/final
mv dist/reversi dist/final/

# Run tests
ls -la dist/final


#Workaround for https://github.com/travis-ci/travis-ci/issues/6522
#Turn off exit on failure.
set +ev
