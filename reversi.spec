# -*- mode: python -*-

from kivy.deps import sdl2, glew
import sys
from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal, get_deps_all, hookspath, runtime_hooks

block_cipher = None


a = Analysis(['reversi\\main.py'],
             pathex=['.'] + sys.path,
             binaries=[],
             datas=[],
             hookspath=hookspath(),
             runtime_hooks=runtime_hooks(),
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             **get_deps_all())

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          Tree('reversi\\'),
          *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
          name='reversi',
          debug=True,
          strip=False,
          upx=True,
          console=True,
          icon='reversi\\grafika\\ikona.ico')