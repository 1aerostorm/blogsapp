#!/bin/sh

set -e

echo "-- Test"
ls

echo "-- Applying migrations..."
python manage.py migrate --noinput

echo "-- Creating Superuser..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
username = "root"
password = "rootroot"
email = "root@root.ru"
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created")
else:
    print("Superuser already exists")
EOF

echo "-- Starting Django..."
exec "$@"