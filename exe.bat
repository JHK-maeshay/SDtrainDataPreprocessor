@echo off
chcp 65001 > nul
echo Python 환경 설정 및 GUI 실행 스크립트
echo =====================================

:: Python 설치 확인
python --version > nul 2>&1
if %errorlevel% == 0 (
    echo Python이 설치되어 있습니다.
    set PYTHON_CMD=python
    goto check_venv
)

:: Python이 없으면 conda 확인
conda --version > nul 2>&1
if %errorlevel% == 0 (
    echo Conda가 설치되어 있습니다.
    set PYTHON_CMD=conda run python
    goto check_venv
) else (
    echo 오류: Python 또는 Conda가 설치되어 있지 않습니다.
    echo Python 또는 Anaconda/Miniconda를 먼저 설치해주세요.
    pause
    exit /b 1
)

:check_venv
:: venv 폴더 확인 및 생성
if not exist "venv" (
    echo 가상환경이 존재하지 않습니다. 새로 생성합니다...
    %PYTHON_CMD% -m venv venv
    if %errorlevel% neq 0 (
        echo 오류: 가상환경 생성에 실패했습니다.
        pause
        exit /b 1
    )
    echo 가상환경이 성공적으로 생성되었습니다.
) else (
    echo 기존 가상환경을 사용합니다.
)

:: 가상환경 활성화
echo 가상환경을 활성화합니다...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo 오류: 가상환경 활성화에 실패했습니다.
    pause
    exit /b 1
)

:: requirements.txt 확인 및 패키지 설치
if exist "requirements.txt" (
    echo requirements.txt에서 의존 패키지를 설치합니다...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo 오류: 패키지 설치에 실패했습니다.
        pause
        exit /b 1
    )
    echo 패키지 설치가 완료되었습니다.
) else (
    echo 경고: requirements.txt 파일이 없습니다. 패키지 설치를 건너뜁니다.
)

:: gui.py 실행
if exist "gui.py" (
    echo gui.py를 실행합니다...
    python gui.py
    if %errorlevel% neq 0 (
        echo 오류: gui.py 실행에 실패했습니다.
        pause
        exit /b 1
    )
) else (
    echo 오류: gui.py 파일이 없습니다.
    pause
    exit /b 1
)

echo.
echo 프로그램이 종료되었습니다.
pause