web: python manage.py migrate --noinput && python manage.py collectstatic --noinput --clear && gunicorn core.wsgi --bind 0.0.0.0:$PORT
