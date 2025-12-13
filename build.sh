#!/usr/bin/env bash
# Build script for Render

set -o errexit  # Exit on error
set -o pipefail # Exit on pipe failure
set -o nounset  # Exit on undefined variable

echo "==> Installing dependencies..."
pip install -r requirements.txt

echo "==> Collecting static files..."
python manage.py collectstatic --no-input

echo "==> Running database migrations..."
python manage.py migrate --no-input

# Setup production data (only runs if needed)
python manage.py setup_production
