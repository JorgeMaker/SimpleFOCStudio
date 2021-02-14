# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['simpleFOCStudio.py'],
             pathex=['/Users/Jorge/Documents/PycharmProjects/SimpleFOCStudioUpdate'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
a.datas += [('src/gui/resources/add.png', 'src/gui/resources/add.png', 'DATA'),]
a.datas += [('src/gui/resources/alert.png', 'src/gui/resources/alert.png', 'DATA'),]
a.datas += [('src/gui/resources/bluedot.png', 'src/gui/resources/bluedot.png', 'DATA'),]
a.datas += [('src/gui/resources/configure.png', 'src/gui/resources/configure.png', 'DATA'),]
a.datas += [('src/gui/resources/connect.png', 'src/gui/resources/connect.png', 'DATA'),]
a.datas += [('src/gui/resources/continue.png', 'src/gui/resources/continue.png', 'DATA'),]
a.datas += [('src/gui/resources/delete.png', 'src/gui/resources/delete.png', 'DATA'),]
a.datas += [('src/gui/resources/disconnect.png', 'src/gui/resources/disconnect.png', 'DATA'),]
a.datas += [('src/gui/resources/edit.png', 'src/gui/resources/edit.png', 'DATA'),]
a.datas += [('src/gui/resources/greendot.png', 'src/gui/resources/greendot.png', 'DATA'),]
a.datas += [('src/gui/resources/motor.png', 'src/gui/resources/motor.png', 'DATA'),]
a.datas += [('src/gui/resources/open.png', 'src/gui/resources/open.png', 'DATA'),]
a.datas += [('src/gui/resources/pause.png', 'src/gui/resources/pause.png', 'DATA'),]
a.datas += [('src/gui/resources/purpledot.png', 'src/gui/resources/purpledot.png', 'DATA'),]
a.datas += [('src/gui/resources/reddot.png', 'src/gui/resources/reddot.png', 'DATA'),]
a.datas += [('src/gui/resources/save.png', 'src/gui/resources/save.png', 'DATA'),]
a.datas += [('src/gui/resources/send.png', 'src/gui/resources/send.png', 'DATA'),]
a.datas += [('src/gui/resources/start.png', 'src/gui/resources/start.png', 'DATA'),]
a.datas += [('src/gui/resources/statistics.png', 'src/gui/resources/statistics.png', 'DATA'),]
a.datas += [('src/gui/resources/stop.png', 'src/gui/resources/stop.png', 'DATA'),]
a.datas += [('src/gui/resources/zoomall.png', 'src/gui/resources/zoomall.png', 'DATA'),]
a.datas += [('src/gui/resources/consoletool.png', 'src/gui/resources/consoletool.png', 'DATA'),]
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='SimpleFOCStudio',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          windowed=True)
app = BUNDLE(exe,
             name='SimpleFOCStudio.app',
             icon='src/gui/resources/studioicon.icns',
             bundle_identifier=None)
