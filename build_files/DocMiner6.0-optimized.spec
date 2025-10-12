# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for DocMiner 6.0 - OPTIMIZED BUILD
# Excludes unnecessary ML/scientific libraries to reduce size

import os
import sys
from pathlib import Path

# Get the project root directory (parent of build_files)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(SPEC)))

a = Analysis(
    ['../enhanced_training_interface.py'],
    pathex=[project_root, os.path.join(project_root, 'utils')],
    binaries=[],
    datas=[
        # Include sample PDFs
        ('../sample_pdfs/about.pdf', 'sample_pdfs'),
        # Include documentation
        ('../README.md', '.'),
        ('../docs/QUICK_START_FOR_GAS.md', 'docs'),
        # Include legal files
        ('../legal/LICENSE', 'legal'),
        ('../legal/LICENSE-ACADEMIC', 'legal'),
        ('../legal/LICENSE-NONCOMMERCIAL', 'legal'),
    ],
    hiddenimports=[
        # Core dependencies ONLY - no ML libraries
        'PySide6.QtCore',
        'PySide6.QtWidgets', 
        'PySide6.QtGui',
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
        # ========================================
        # EXCLUDE HEAVY ML/SCIENTIFIC LIBRARIES
        # These are auto-detected but NOT needed
        # ========================================
        
        # Machine Learning frameworks
        'torch',
        'torchvision',
        'torchaudio',
        'transformers',
        'tensorflow',
        'keras',
        
        # Scientific computing (not needed for this app)
        'numpy',
        'scipy',
        'pandas',
        'matplotlib',
        'sympy',
        'numba',
        'llvmlite',
        
        # Image processing (PyMuPDF handles our PDFs)
        'PIL',
        'Pillow',
        'skimage',
        'cv2',
        'imageio',
        
        # Data science extras
        'pyarrow',
        'altair',
        'jsonschema',
        'narwhals',
        
        # Web frameworks (keep anyio - needed by httpx/openai)
        'uvicorn',
        'websockets',
        # 'anyio',  # KEEP - needed by httpx
        
        # Testing/dev tools
        'pytest',
        'unittest',
        'doctest',
        
        # Development/test files
        'tests',
        'archive',
        'build_files',
        
        # Exclude QtWebEngine (causes corrupted binaries)
        'PySide6.QtWebEngineWidgets',
        'PySide6.QtWebEngineCore',
        'PySide6.QtWebChannel',
        
        # Tkinter (we use PySide6)
        'tkinter',
        '_tkinter',
        'Tkinter',
        
        # Jupyter/IPython
        'IPython',
        'jupyter',
        'notebook',
        
        # Database drivers (not needed)
        'sqlite3',
        'psycopg2',
        'pymongo',
        
        # Other heavy libs
        'lxml.etree',
        'cryptography',
        'pycparser',
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
    name='DocMiner6.0',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,  # Native architecture (ARM64, works on Intel via Rosetta 2)
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(project_root, 'build_files', 'icon.icns') if sys.platform == 'darwin' else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DocMiner6.0',
)

# macOS App Bundle (only created on macOS)
app = BUNDLE(
    coll,
    name='DocMiner6.0.app',
    icon=os.path.join(project_root, 'build_files', 'icon.icns'),
    bundle_identifier='edu.university.docminer',
    info_plist={
        'CFBundleName': 'DocMiner',
        'CFBundleDisplayName': 'DocMiner',
        'CFBundleShortVersionString': '6.0',
        'CFBundleVersion': '6.0.0',
        'NSHighResolutionCapable': 'True',
        'NSRequiresAquaSystemAppearance': 'False',
    },
)
