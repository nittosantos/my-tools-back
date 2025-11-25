web: python manage.py migrate --noinput && mkdir -p staticfiles && python manage.py collectstatic --noinput --clear && gunicorn core.wsgi --bind 0.0.0.0:$PORT

