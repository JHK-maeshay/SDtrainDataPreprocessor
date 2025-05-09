@echo off
chcp 65001 > nul
echo [debug] gradio 실행 준비 중...
REM
IF EXIST "%USERPROFILE%\anaconda3\Scripts\activate.bat" (
    CALL "%USERPROFILE%\anaconda3\Scripts\activate.bat" venv
) ELSE (
    REM
    for /f "delims=" %%i in ('where conda') do set CONDA_EXE=%%i
    IF DEFINED CONDA_EXE (
        CALL "%CONDA_EXE%\..\..\Scripts\activate.bat" venv
    ) ELSE (
        echo [ERROR] conda 경로를 찾을 수 없습니다.
        pause
        exit /b
    )
)

python gui.py
CALL conda deactivate
pause