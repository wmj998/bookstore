bind = '0.0.0.0:5000'
workers = 4
worker_class = 'gevent'
chdir = '/home/book/'
pidfile = 'gunicorn.pid'
accesslog = 'log/access.log'
errorlog = 'log/error.log'
loglevel='warning'
