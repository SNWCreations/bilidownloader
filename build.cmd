@echo off

if exist "dist" (rd /s /q dist)

echo ****** EXECUTE PYINSTALLER ******
pyinstaller main.py -w -D -i="./icon.ico" -n bilidownloader --version-file file_version_info.txt --clean

call cleanup.cmd

echo ********** COPY FFMPEG **********

copy /Y .\ffmpeg.exe .\dist\bilidownloader

echo ***** BUILDING SUCCESSFULLY *****
echo You can find the executable files
echo (Main executable file is main.exe)
echo in (Current directory)/dist/main.
echo ************* STOP **************

