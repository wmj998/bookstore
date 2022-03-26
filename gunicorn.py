bind = '0.0.0.0:5000'

worker_class = 'gevent'
workers = 4

chdir = '/home/book'

pidfile = 'gunicorn.pid'

loglevel='warning'
accesslog = 'log/access.log'
errorlog = 'log/error.log'
