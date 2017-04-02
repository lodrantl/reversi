#!/usr/bin/env bash
set -ev #echo on

# Run tests
python -m pytest
# Build executables with pyinstaller
python -m PyInstaller -y reversi.spec

# Build dmg
hdiutil create -srcfolder dist/Reversi.app dist/Reversi.dmg

# Move to final dir
mkdir dist/final
mv dist/Reversi.dmg dist/final/

# Show files
ls -la dist/
ls -la dist/reversi
ls -la dist/final

#Workaround for https://github.com/travis-ci/travis-ci/issues/6522
#Turn off exit on failure.
set +ev
