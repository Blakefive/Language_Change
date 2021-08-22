@echo off

set REL_PATH=dist
set ABS_PATH=

rem // Save current directory and change to target directory
pushd %REL_PATH%

rem // Save value of CD variable (current directory)
set ABS_PATH=%CD%

rem // Restore original directory
popd

echo Relative path: %REL_PATH%
echo Maps to path: %ABS_PATH%
echo check1: "D:\Programming\python\projects\typing sound\dist"
echo check2: "%ABS_PATH%"

start /d "%ABS_PATH%" /b language.exe