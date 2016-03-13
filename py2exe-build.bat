@echo off

rmdir /q /s dist
c:\python27\python.exe py2exe-setup.py

chdir dist
copy RoguePy\libtcod\libtcod-mingw.dll .
rmdir /q /s build .git
del /q .gitignore
main
cd ..