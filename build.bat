@echo off
setlocal enabledelayedexpansion

echo.
echo ------------- Build ------------- Running Nuxt generate...
cd app\nuxt
call npm run generate
if errorlevel 1 (
    echo ------------- Build ------------- Nuxt generate failed/^!
    echo.
    exit /b 1
)

REM Step 2: Identify Nuxt output folder
if exist "nuxt_dist\public" (
    set "NUXT_DIST=nuxt_dist"
    set "NUXT_DIST_PUBLIC=nuxt_dist\public"
) else (
    echo ------------- Build ------------- Could not find Nuxt build output folder/^!
    echo.
    exit /b 1
)

REM Step 3: Prepare destination paths
set "BACKEND_STATIC=..\static"
set "BACKEND_TEMPLATES=..\templates"

REM Step 4: Clear previous build files
echo.
echo ------------- Build ------------- Cleaning old build files...
echo.

if exist "%BACKEND_STATIC%" rmdir /S /Q "%BACKEND_STATIC%"
if exist "%BACKEND_TEMPLATES%" rmdir /S /Q "%BACKEND_TEMPLATES%"

REM Step 5: Copy files
echo ------------- Build ------------- Copying new build files...
echo.

mkdir "%BACKEND_STATIC%"
mkdir "%BACKEND_TEMPLATES%"

REM Step 6: Copy HTML files to templates
copy "%NUXT_DIST_PUBLIC%\index.html" "%BACKEND_TEMPLATES%"
copy "%NUXT_DIST_PUBLIC%\200.html" "%BACKEND_TEMPLATES%" 2>nul
copy "%NUXT_DIST_PUBLIC%\404.html" "%BACKEND_TEMPLATES%" 2>nul

echo.
echo ------------- Build ------------- Copied index.html, 200.html, and 400.html to templates/
echo.

REM Step 7: Copy all other assets to static
xcopy "%NUXT_DIST_PUBLIC%\*" "%BACKEND_STATIC%" /E /I /Y

del /F /Q "%BACKEND_STATIC%\index.html" 2>nul
if exist "app\nuxt\.env" (
    echo ------------- Build ------------- Failed to delete "app\static\index.html".
    echo.
) 

del /F /Q "%BACKEND_STATIC%\200.html" 2>nul
if exist "app\nuxt\.env" (
    echo ------------- Build ------------- Failed to delete "app\static\200.html".
    echo.
) 

del /F /Q "%BACKEND_STATIC%\404.html" 2>nul
if exist "app\nuxt\.env" (
    echo ------------- Build ------------- Failed to delete "app\static\404.html".
    echo.
) 

echo.
echo ------------- Build ------------- Copied other files to static/
echo.

REM Step 8: Remove Nuxt dist folder
rmdir /S /Q "%NUXT_DIST%" 2>nul
if exist "%NUXT_DIST%" (
    echo ------------- Build ------------- Failed to delete %NUXT_DIST%.
    echo.
) 

del /F /Q "app\nuxt\dist" 2>nul
if exist "app\nuxt\dist" (
    echo ------------- Build ------------- Failed to delete "app\nuxt\dist".
    echo.
) 

echo ------------- Build ------------- Deleted dist/
echo.
echo ------------- Build ------------- Deleted nuxt_dist/
echo.
echo ------------- Build ------------- Build complete/^!

exit /b 0