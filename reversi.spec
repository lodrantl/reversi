# -*- mode: python -*-

import sys
import os
from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal, get_deps_all, hookspath, runtime_hooks
block_cipher = None

a = Analysis([os.path.join('reversi', 'main.py')],
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

if sys.platform == "linux" or sys.platform == "linux2":
    exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          Tree(os.path.join('reversi', '')),
          name='reversi',
          debug=True,
          strip=False,
          upx=True,
          console=True)

elif sys.platform == "darwin":
    exe = EXE(pyz,
              a.scripts,
              exclude_binaries=True,
              name='reversi',
              debug=True,
              strip=False,
              upx=True,
              console=True,
              icon=os.path.join('reversi', 'grafika', 'ikona.icns'))

    coll = COLLECT(exe,
                   Tree(os.path.join('reversi', '')),
                   a.binaries,
                   a.zipfiles,
                   a.datas,
                   strip=False,
                   upx=True,
                   name='reversi')

    app = BUNDLE(coll,
                 name='Reversi.app',
                 icon=os.path.join('reversi', 'grafika', 'ikona.icns'),
                 bundle_identifier=None)

elif sys.platform == "win32":
    from kivy.deps import sdl2, glew
    exe = EXE(pyz,
              a.scripts,
              a.binaries,
              a.zipfiles,
              a.datas,
              Tree(os.path.join('reversi', '')),
              *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
              name='Reversi',
              debug=True,
              strip=False,
              upx=True,
              console=True,
              icon=os.path.join('reversi', 'grafika', 'ikona.ico'))