@echo off
echo.
echo ======================================
echo    ZoomingCLS - Auto Setup Script
echo ======================================
echo.

echo [1/4] Creating virtual environment...
python -m venv venv

echo [2/4] Activating virtual environment...
call venv\Scripts\activate

echo [3/4] Installing requirements...
pip install -r requirements.txt

echo [4/4] Setting up database...
python manage.py migrate

echo.
echo Setup complete!
echo.
echo Creating a superuser for admin panel...
python manage.py createsuperuser

echo.
echo Starting server at http://127.0.0.1:8000 ...
python manage.py runserver
