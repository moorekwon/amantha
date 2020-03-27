daemon = False
chdir = '/srv/amantha/app'
bind = 'unix:run/amantha.sock'
accesslog = '/var/log/gunicorn/amantha-access.log'
errorlog = '/var/log/gunicorn/amantha-error.log'
