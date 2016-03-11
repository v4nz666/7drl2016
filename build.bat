@echo off

rmdir /q /s dist
c:\python27\python.exe setup.py

chdir dist
copy RoguePy\libtcod\*.dll .
copy RoguePy\libtcod\lucida12x12_gs_tc.png .
rmdir /q /s build
main
cd ..