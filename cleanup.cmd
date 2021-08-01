@echo off

echo *** CLEAN UP ***

del DownloadHistory.txt
del bilidownloader.spec
rd /s /q Downloads
rd /s /q __pycache__

echo ****** OK ******
