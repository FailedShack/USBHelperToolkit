@echo off
title USBHelperToolkit - Please wait... This may take a while.
python downloadInjections.py
python downloadCustoms.py
echo Done!
pause >nul