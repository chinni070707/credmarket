#!/usr/bin/env bash
# Build script for Render

set -o errexit  # Exit on error
set -o pipefail # Exit on pipe failure
set -o nounset  # Exit on undefined variable

echo "==> Validating environment..."
python validate_env.py

echo "==> Installing dependencies..."
pip install -r requirements.txt

echo "==> Running database migrations..."
python manage.py migrate --no-input

echo "==> Collecting static files..."
python manage.py collectstatic --no-input

echo "==> Setting up production data..."
python manage.py setup_production

echo "==> Adding category images..."
python manage.py add_category_images

# Prelaunch mode setup - create dummy data for demo
if [ "$PRELAUNCH_MODE" = "true" ] || [ "$PRELAUNCH_MODE" = "True" ]; then
    echo "==> PRELAUNCH MODE DETECTED - Creating dummy data..."
    
    echo "==> Creating dummy users..."
    python manage.py create_dummy_users
    
    echo "==> Creating dummy listings..."
    python manage.py create_dummy_listings
    
    echo "==> ✅ Prelaunch dummy data created successfully!"
else
    echo "==> Skipping dummy data (PRELAUNCH_MODE not set)"
fi

#echo "==> Deleting old mahchi01@cadence.com user if exists..."
#python manage.py shell -c "from accounts.models import User; User.objects.filter(email='mahchi01@cadence.com').delete(); print('User deleted if existed')"

#echo "==> Fixing user statuses for approved companies..."
#python fix_user_status.py
