import sys
from cx_Freeze import setup, Executable
from os import listdir
from os.path import isfile, join

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

build_exe_options = {
    "include_msvcr": True,  # skip error msvcr100.dll missing
    "include_files":  ["dlls32/" + f for f in listdir("dlls32/") if isfile(join("dlls32/", f))] if sys.platform == 'win32' else ["dlls64/" + f for f in listdir("dlls64/") if isfile(join("dlls64/", f))]
}
bdist_msi_options = {}

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
