release: python manage.py migrate
release: python manage.py makemigrations

web: gunicorn messages_system.wsgi --log-file -
