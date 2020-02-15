# -*- mode: python -*-

block_cipher = None


a = Analysis(['flow_transcribe_controlpanel.py'],
             pathex=['/Users/charlielangrall/Desktop/Technical/Programming/python/Projects/flow-env/flow_transcribe_controlpanel'],
             binaries=[],
             datas=[('./defaults.cfg', '.'), ('./images', './images')],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='flow_transcribe_controlpanel',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='flow_transcribe_controlpanel.app',
             icon=None,
             bundle_identifier=None)
