# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['enhanced_training_interface.py'],
    pathex=['/Users/todd/research-buddy'],
    binaries=[],
    datas=[
        ('utils', 'utils'),
        ('sample_pdfs', 'sample_pdfs'),
        ('interface_settings.json', '.'),
    ],
    hiddenimports=['pkg_resources.py2_warn'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ResearchBuddy4.0',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

app = BUNDLE(
    exe,
    name='ResearchBuddy4.0.app',
    icon=None,
    bundle_identifier='com.researchbuddy.app',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeName': 'PDF',
                'CFBundleTypeIconFile': 'pdf.icns',
                'LSItemContentTypes': ['com.adobe.pdf'],
                'LSHandlerRank': 'Alternate'
            }
        ]
    }
)