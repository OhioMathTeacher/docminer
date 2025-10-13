# -*- mode: python ; coding: utf-8 -*-
# MINIMAL PyInstaller spec file for DocMiner 6.1.0 - Fast build
# Skips problematic hooks

import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(SPEC)))

a = Analysis(
    ['../enhanced_training_interface.py'],
    pathex=[project_root, os.path.join(project_root, 'utils')],
    binaries=[],
    datas=[
        ('../sample_pdfs/aboutDM.pdf', 'sample_pdfs'),
        ('../images/robbie_anim_1.png', 'images'),
        ('../images/robbie_anim_2.png', 'images'),
        ('../images/robbie_anim_3.png', 'images'),
        ('../README.md', '.'),
        ('../docs/QUICK_START_FOR_GAS.md', 'docs'),
        ('../legal/LICENSE', 'legal'),
        ('../legal/LICENSE-ACADEMIC', 'legal'),
        ('../legal/LICENSE-NONCOMMERCIAL', 'legal'),
    ],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtWidgets', 
        'PySide6.QtGui',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'torch', 'tensorflow', 'numpy', 'pandas', 'matplotlib',
        'PIL', 'tkinter', 'IPython', 'jupyter',
        'PySide6.QtWebEngineWidgets',
        'PySide6.QtWebEngineCore',
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='DocMiner6.1',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Disable UPX to speed up build
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,  # Disable UPX
    upx_exclude=[],
    name='DocMiner6.1',
)
