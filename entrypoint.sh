python manage.py makemigrations --noinput
python manage.py migrate --noinput
gunicorn foodbook.wsgi:application --bind 0.0.0.0:8000

