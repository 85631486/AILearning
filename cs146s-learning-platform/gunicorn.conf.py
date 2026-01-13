# Gunicorn配置文件
import multiprocessing
import os

# 路径配置
LOG_DIR = "/var/log/cs146s"
RUN_DIR = "/var/run/cs146s"
APP_USER = os.getenv('GUNICORN_USER', 'www-data')
APP_GROUP = os.getenv('GUNICORN_GROUP', 'www-data')

# 服务器配置
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50

# 超时配置
timeout = 30
keepalive = 10

# 日志配置
loglevel = "info"
accesslog = os.path.join(LOG_DIR, "access.log")
errorlog = os.path.join(LOG_DIR, "error.log")
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# 进程配置
user = APP_USER
group = APP_GROUP
tmp_upload_dir = "/tmp"
proc_name = "cs146s-learning-platform"

# 应用配置
pidfile = os.path.join(RUN_DIR, "gunicorn.pid")
