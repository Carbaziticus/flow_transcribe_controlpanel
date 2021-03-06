# -*- mode: python -*-

block_cipher = None


a = Analysis(['flow_transcribe_controlpanel.py'],
             pathex=['/Users/charlielangrall/Desktop/Technical/Programming/python/Projects/flow-env/flow_transcribe_controlpanel'],
             binaries=[('/System/Library/Frameworks/Tcl.framework/Tcl', 'tcl'), ('/System/Library/Frameworks/Tk.framework/Tk', 'tk')],
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
          console=False , icon='images/AsaProIcons.icns')
app = BUNDLE(exe,
             name='Flow Transcribe Control Panel.app',
             icon='./images/AsaProIcons.icns',
             bundle_identifier=None)
