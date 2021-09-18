web: gunicorn univ_blog.wsgi:application --log-file - --log-level debug
python manage.py collectstatic --noinput
manage.py migrate