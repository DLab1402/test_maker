@echo off

IF EXIST "D:\my_project\myenv\Scripts\activate.bat" (
    CALL "D:\my_project\myenv\Scripts\activate.bat"
) ELSE IF EXIST "D:\my_project\myenv_315\myenv\Scripts\activate.bat" (
    CALL "D:\my_project\myenv_315\myenv\Scripts\activate.bat"
)  ELSE IF EXIST "D:\myvenv\Scripts\activate.bat" (
    CALL "D:\myvenv\Scripts\activate.bat"
) ELSE (
    echo No virtual environment found!
    exit /b 1
)

@REM python "D:\my_project\main.py"