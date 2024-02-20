release: python manage.py migrate
release: python manage.py makemigrations

web: gunicorn messaging_system.wsgi --log-file -
