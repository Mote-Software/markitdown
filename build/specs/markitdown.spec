# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for markitdown binary
# This spec file is configured to bundle all dependencies including ONNX models

import sys
import os
from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_submodules

block_cipher = None

# Collect all data files and dependencies for packages with data files
datas = []
binaries = []
hiddenimports = []

# Collect magika (includes ONNX models and data files)
magika_datas, magika_binaries, magika_hiddenimports = collect_all('magika')
datas += magika_datas
binaries += magika_binaries
hiddenimports += magika_hiddenimports

# Collect onnxruntime
onnx_datas, onnx_binaries, onnx_hiddenimports = collect_all('onnxruntime')
datas += onnx_datas
binaries += onnx_binaries
hiddenimports += onnx_hiddenimports

# Collect all markitdown submodules (especially converters)
hiddenimports += collect_submodules('markitdown')
hiddenimports += collect_submodules('markitdown.converters')

# Additional hidden imports for dynamically loaded modules
hiddenimports += [
    'markitdown.__main__',
    'markitdown.converters',
    'beautifulsoup4',
    'bs4',
    'bs4.builder._htmlparser',
    'bs4.builder._lxml',
    'requests',
    'markdownify',
    'charset_normalizer',
    'defusedxml',
    # Optional dependencies
    'pptx',
    'mammoth',
    'pandas',
    'openpyxl',
    'xlrd',
    'lxml',
    'lxml.etree',
    'lxml._elementpath',
    'pdfminer',
    'pdfminer.six',
    'olefile',
    'pydub',
    'speech_recognition',
    'youtube_transcript_api',
    'azure.ai.documentintelligence',
    'azure.identity',
    # Additional dependencies
    'pkg_resources',
    'pkg_resources.py2_warn',
]

# Collect data files for other packages that may need them
try:
    pdfminer_datas = collect_data_files('pdfminer')
    datas += pdfminer_datas
except Exception:
    pass

try:
    mammoth_datas = collect_data_files('mammoth')
    datas += mammoth_datas
except Exception:
    pass

a = Analysis(
    ['entry_point.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='markitdown',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
