web: python manage.py migrate; mkdir -p staticfiles; python manage.py collectstatic --noinput || true; gunicorn core.wsgi --bind 0.0.0.0:$PORT

