import sys
from cx_Freeze import setup, Executable
from os import listdir
from os.path import isfile, join

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

build_exe_options = {
    "include_msvcr": True,  # skip error msvcr100.dll missing
    "include_files": ["dlls/" + f for f in listdir("dlls/") if isfile(join("dlls/", f))]
}
install_exe_options = {
    "install_dir": "D:/work/build"
}
bdist_msi_options = {
    'add_to_path': True
}

executables = [
    Executable('furunotogpx.py',
               base=base,
               copyright="Copyright (C) 2017 russkiy78@gmail.com",
               shortcutName='Furuno <-> GPX Converter',
               shortcutDir='ProgramMenuFolder'
               )
]

setup(name='readfuruno',
      version='1.0',
      description='Furuno <-> GPX Converter',
      options={"build_exe": build_exe_options, "bdist_msi": bdist_msi_options},
      executables=executables
      )
