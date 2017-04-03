#!/usr/bin/env bash
set -ev #echo on

# Run tests
python -m pytest
# Build executables with pyinstaller
python -m PyInstaller -y reversi.spec

# Build dmg
hdiutil create -srcfolder dist/reversi.app dist/reversi.dmg

# Move to final dir
mkdir dist/final
mv dist/reversi.dmg dist/final/reversi-${VERSION}-${TRAVIS_OS_NAME}.dmg

# Show files
ls -la dist/
ls -la dist/final

#Workaround for https://github.com/travis-ci/travis-ci/issues/6522
#Turn off exit on failure.
set +ev
