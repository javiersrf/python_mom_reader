from cx_Freeze import setup, Executable
import sys

build_exe_option = {"packages":["os", "sched", "time", "datetime", "mysql.connector", "lxml", "bs4", "shutil", "json", "logging"]}

# ada
base = None
if sys.platform == "win32":
    base = "Win32GUI"




setup(
    name="mom_reader",
    version='0.0.5',
    description ='Tradutor de arquivos mom',
    options = {"build_exe":build_exe_option},
    executables = [Executable("mom_reader.py",base=base)]
)
