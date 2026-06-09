# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_all

block_cipher = None

# Collect data files from heavy packages
datas = []
datas += collect_data_files('pyvista')
datas += collect_data_files('pyvistaqt')
datas += collect_data_files('vtk')
datas += collect_data_files('vtkmodules')
datas += collect_data_files('matplotlib')
datas += collect_data_files('PIL')

# Project data directories
datas += [
    ('TC_Data', 'TC_Data'),
    ('Images', 'Images'),
    ('Forms', 'Forms'),
    ('Modulus', 'Modulus'),
]

# Platform-specific compiled C binaries
if sys.platform == 'win32':
    _sources = [
        ('Sources/ch2d_alloy.exe',      'Sources'),
        ('Sources/ch3d_alloy.exe',      'Sources'),
        ('Sources/ch2d_qualitative.exe','Sources'),
        ('Sources/hkl_2d.exe',          'Sources'),
        ('Sources/hkl_3d.exe',          'Sources'),
        ('Sources/libfftw3-3.dll',      'Sources'),
    ]
    # ch1d.exe is optional — include only if it exists
    if os.path.isfile('Sources/ch1d.exe'):
        _sources.append(('Sources/ch1d.exe', 'Sources'))
else:
    _sources = [
        ('Sources/ch2d_alloy.o',       'Sources'),
        ('Sources/ch3d_alloy.o',       'Sources'),
        ('Sources/ch2d_qualitative.o', 'Sources'),
        ('Sources/hkl_2d.o',           'Sources'),
        ('Sources/hkl_3d.o',           'Sources'),
    ]
    if os.path.isfile('Sources/ch1d.o'):
        _sources.append(('Sources/ch1d.o', 'Sources'))

hiddenimports = [
    'vtkmodules',
    'vtkmodules.all',
    'vtkmodules.qt.QVTKRenderWindowInteractor',
    'vtkmodules.util',
    'vtkmodules.util.numpy_support',
    'pyvista',
    'pyvistaqt',
    'matplotlib.backends.backend_qt5agg',
    'matplotlib.backends.backend_agg',
    'PIL._imaging',
    'yaml',
    'ffmpeg',
]

a = Analysis(
    ['mu2mech.py'],
    pathex=['.'],
    binaries=_sources,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'IPython', 'ipykernel', 'jupyter'],
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
    name='mu2mech',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='Images/app_icon.png' if os.path.isfile('Images/app_icon.png') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='mu2mech',
)
