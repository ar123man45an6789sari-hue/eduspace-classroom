#!/bin/bash
echo ""
echo "======================================"
echo "   ZoomingCLS - Auto Setup Script"
echo "======================================"
echo ""

# Create virtual environment
echo "[1/4] Creating virtual environment..."
python -m venv venv

# Activate it
echo "[2/4] Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "[3/4] Installing requirements..."
pip install -r requirements.txt -q

# Migrate database
echo "[4/4] Setting up database..."
python manage.py migrate --run-syncdb

echo ""
echo "✅ Setup complete!"
echo ""
echo "   Creating a superuser for admin panel..."
python manage.py createsuperuser

echo ""
echo "🚀 Starting server at http://127.0.0.1:8000 ..."
echo "   Press Ctrl+C to stop."
echo ""
python manage.py runserver
