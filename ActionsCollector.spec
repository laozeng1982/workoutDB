# -*- mode: python -*-

import sys
sys.setrecursionlimit(5000)

block_cipher = None


a = Analysis(['ActionsCollector.py'],
             pathex=['d:\\codingProjects\\python\\workoutDB'],
             binaries=[],
             datas=[
             ('Mandarin.dat', '.'),
             ('chromedriver.exe', '.'),
             ('images', './images')
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='ActionsCollector',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          icon='favicon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='ActionsCollector')
