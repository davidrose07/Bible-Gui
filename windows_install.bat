@echo off
setlocal enabledelayedexpansion

set "APP_NAME=bible-gui"
set "WRAPPER=%ProgramData%\bible-gui.cmd"

echo ========================================
echo Welcome to Bible-GUI Setup
echo ========================================
echo.
echo Choose how you'd like to run the app:
echo   1. Run with Docker (recommended for isolation)
echo   2. Install and run locally with Python
echo   3. Cancel
echo.

set /p choice=Enter your choice (1-3): 

if "%choice%"=="1" goto docker
if "%choice%"=="2" goto local
if "%choice%"=="3" goto end

echo ❌ Invalid choice. Exiting.
goto end

:docker
echo.
echo 📦 Checking for Docker...
where docker >nul 2>nul
if "%errorlevel%"=="0" (
    echo ✅ Docker is already installed.
    goto build_docker
)

echo ❌ Docker not found.
echo.
echo Choose Docker installation method:
echo   1. Install using winget
echo   2. Install using Chocolatey
echo   3. Open Docker download page
echo   4. Cancel

set /p dchoice=Enter your choice (1-4): 

if "%dchoice%"=="1" (
    where winget >nul 2>nul
    if "%errorlevel%"=="0" (
        echo 🚀 Installing Docker with winget...
        winget install -e --id Docker.DockerDesktop
        goto waitfordocker
    ) else (
        echo ❌ winget not found. Visit https://aka.ms/getwinget
        goto end
    )
) else if "%dchoice%"=="2" (
    where choco >nul 2>nul
    if "%errorlevel%"=="0" (
        echo 🚀 Installing Docker with Chocolatey...
        choco install docker-desktop -y
        goto waitfordocker
    ) else (
        echo ❌ Chocolatey not found. Visit https://chocolatey.org/install
        goto end
    )
) else if "%dchoice%"=="3" (
    echo 🌐 Opening Docker download page...
    start https://www.docker.com/products/docker-desktop
    goto end
) else (
    echo ❌ Canceled.
    goto end
)

:waitfordocker
echo 🕒 Waiting for Docker to start...
timeout /t 10 >nul
docker info >nul 2>nul
if "%errorlevel%" NEQ "0" (
    echo ❌ Docker is not running. Please start Docker Desktop manually.
    goto end
)

:build_docker
echo 🔧 Building Docker image...
docker build -t %APP_NAME% .

echo 🖥️ Creating wrapper script: %WRAPPER%
echo @echo off > "%WRAPPER%"
echo docker run -it --rm %APP_NAME% >> "%WRAPPER%"

echo ✅ Docker setup complete. Run your app with:
echo    %WRAPPER%
goto end

:local
echo 🔍 Setting up local environment...

where python >nul 2>nul
if "%errorlevel%" NEQ "0" (
    echo ❌ Python not found. Download from https://www.python.org/
    goto end
)

echo 🛠️ Installing package from setup.py...
python setup.py install
if "%errorlevel%" NEQ "0" (
    echo ❌ setup.py failed.
    goto end
)

REM Check for PyQt5
(
    echo try:
    echo     import PyQt5
    echo except ImportError:
    echo     print("missing:PyQt5")
) > %TEMP%\_check_pyqt.py

for /f %%i in ('python %TEMP%\_check_pyqt.py') do (
    if "%%i"=="missing:PyQt5" (
        echo Installing PyQt5...
        pip install PyQt5
    )
)
del %TEMP%\_check_pyqt.py

REM Check for curses
(
    echo try:
    echo     import curses
    echo except ImportError:
    echo     print("missing:curses")
) > %TEMP%\_check_curses.py

for /f %%i in ('python %TEMP%\_check_curses.py') do (
    if "%%i"=="missing:curses" (
        echo Installing windows-curses...
        pip install windows-curses
    )
)
del %TEMP%\_check_curses.py

echo ✅ Local setup complete. Run your app with:
echo    python -m your_module_name
goto end

:end
endlocal
exit /b
