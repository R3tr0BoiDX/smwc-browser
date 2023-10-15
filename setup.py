import os

from cx_Freeze import setup, Executable

# todo: needs some fine tuning
build_exe_options = {
    "excludes": [
        "tkinter",
        "unittest",
        "asyncio",
        "tk86t",
        "tk8.6",
    ],
}

target = Executable(script="source/main.py", icon="resources\windows_icon.ico")

setup(
    name="smwc-browser",
    version="1.0",
    description="A browser for SMW Central",
    executables=[target],
    options={"build_exe": build_exe_options},
)
