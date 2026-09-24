# -*- mode: python ; coding: utf-8 -*-
import os
import sys
import streamlit
from PyInstaller.utils.hooks import copy_metadata  # INCLUSÃO CRÍTICA

# Localiza a pasta do Streamlit para copiar os ficheiros estáticos (HTML/JS/CSS)
streamlit_pkg_dir = os.path.dirname(streamlit.__file__)
streamlit_static_dir = os.path.join(streamlit_pkg_dir, "static")

block_cipher = None

# Copia os metadados de instalação do Streamlit (resolve o erro PackageNotFoundError)
metadata_files = copy_metadata('streamlit')

# Une todos os ficheiros de dados obrigatórios
added_files = [
    (streamlit_static_dir, "streamlit/static"),
    ("app.py", "."),  
] + metadata_files

a = Analysis(
    ['run_app.py'],  
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'streamlit',
        'streamlit.runtime',
        'streamlit.runtime.scriptrunner',
        'streamlit.runtime.scriptrunner.magic_funcs',
        'pypdf',
        'reportlab',
        'reportlab.pdfgen.canvas',
        'reportlab.lib.pagesizes',
        'fitz',  
    ],
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
    [],
    exclude_binaries=True,
    name='PDF_Advanced_Suite',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PDF_Advanced_Suite',
)
