# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for Research Buddy 5.2
# Updated to include utils directory and handle recent changes

import os
from pathlib import Path

# Get the project root directory
project_root = os.path.dirname(os.path.abspath(SPEC))

a = Analysis(
    ['../enhanced_training_interface.py'],
    pathex=[project_root, os.path.join(project_root, 'utils')],
    binaries=[],
    datas=[
        # Include sample PDFs
        ('../sample_pdfs/*.pdf', 'sample_pdfs'),
        # Include documentation
        ('../README.md', '.'),
        ('../docs/QUICK_START_FOR_GAS.md', 'docs'),
        # Include legal files
        ('../legal/LICENSE', 'legal'),
        ('../legal/LICENSE-ACADEMIC', 'legal'),
        ('../legal/LICENSE-NONCOMMERCIAL', 'legal'),
    ],
    hiddenimports=[
        # Core dependencies
        'PySide6.QtCore',
        'PySide6.QtWidgets', 
        'PySide6.QtGui',
        # Skip QtWebEngineWidgets - causing corrupted binary issues
        # 'PySide6.QtWebEngineWidgets',
        # PDF processing
        'fitz',
        'PyPDF2',
        'pdfplumber',
        # HTTP and API
        'requests',
        'openai',
        'httpx',
        # Utils
        'utils.metadata_extractor',
        'configuration_dialog',
        'github_report_uploader',
        # JSON and data handling
        'json',
        'pathlib',
        'tabulate',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude development/test files
        'tests',
        'archive',
        'build_files',
        # Exclude the removed first_run_setup
        'first_run_setup',
        'utils.first_run_setup',
        # Exclude QtWebEngine due to corrupted universal binary on Intel
        'PySide6.QtWebEngineWidgets',
        'PySide6.QtWebEngineCore',
        'PySide6.QtWebChannel',
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
    name='ResearchBuddy5.2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to True for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,  # Native architecture (ARM64 on GH Actions, works on Intel via Rosetta 2)
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path when available
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ResearchBuddy5.2',
)

# macOS App Bundle (only created on macOS)
app = BUNDLE(
    coll,
    name='ResearchBuddy5.2.app',
    icon=None,
    bundle_identifier='edu.university.researchbuddy',
    info_plist={
        'NSHighResolutionCapable': 'True',
        'NSRequiresAquaSystemAppearance': 'False',
    },
)