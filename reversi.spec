# -*- mode: python -*-

import sys
import os
from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal, get_deps_all, hookspath, runtime_hooks
block_cipher = None

def filter_binaries(all_binaries):
    '''Exclude binaries provided by system packages, and rely on .deb dependencies
    to ensure these binaries are available on the target machine.

    We need to remove OpenGL-related libraries so we can distribute the executable
    to other linux machines that might have different graphics hardware. If you
    bundle system libraries, your application might crash when run on a different
    machine with the following error during kivy startup:

    Fatal Python Error: (pygame parachute) Segmentation Fault

    If we strip all libraries, then PIL might not be able to find the correct _imaging
    module, even if the `python-image` package has been installed on the system. The
    easy way to fix this is to not filter binaries from the python-imaging package.

    We will strip out all binaries, except libpython2.7, which is required for the
    pyinstaller-frozen executable to work, and any of the python-* packages.
    '''

    print('Excluding system libraries')
    import subprocess
    excluded_pkgs  = set()
    excluded_files = set()
    whitelist_prefixes = ('libpython', 'python-')
    binaries = []

    for b in all_binaries:
        try:
            output = subprocess.check_output(['dpkg', '-S', b[1]], stderr=open('/dev/null')).decode('ascii')
            package, system, path = output.split(':', 2)
            if not package.startswith(whitelist_prefixes):
                excluded_pkgs.add(package)
                excluded_files.add(b[0])
                print(' excluding {f} from package {p}'.format(f=b[0], p=package))
        except Exception as e:
            pass

    print('Your exe will depend on the following packages:')
    print(excluded_pkgs)

    inc_libs = set(['libpython2.7.so.1.0'])
    binaries = [x for x in all_binaries if x[0] not in excluded_files]
    return binaries


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
          filter_binaries(a.binaries),
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
                 name='reversi.app',
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
              name='reversi',
              debug=True,
              strip=False,
              upx=True,
              console=True,
              icon=os.path.join('reversi', 'grafika', 'ikona.ico'))