# Production Gunicorn Configuration for Kitab Backend
# Bu faylı production server-də istifadə edin

import multiprocessing
import os

# Server Socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker Processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
preload_app = True

# Timeout Settings
timeout = 30
keepalive = 2
graceful_timeout = 30

# Logging
# Heroku-da log faylları yoxdur, stdout/stderr istifadə edirik
accesslog = "-"  # stdout
errorlog = "-"   # stderr
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process Naming
proc_name = "kitab_backend"

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Performance
worker_tmp_dir = "/dev/shm"
forwarded_allow_ips = "*"

# SSL (if using HTTPS)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Environment Variables
raw_env = [
    "DJANGO_SETTINGS_MODULE=kitab_backend.settings",
]

# Pre-fork hooks
def pre_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def pre_exec(server):
    server.log.info("Forked child, re-executing.")

def when_ready(server):
    server.log.info("Server is ready. Spawning workers")

def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")

def pre_request(worker, req):
    worker.log.debug("%s %s", req.method, req.path)

def post_request(worker, req, environ, resp):
    worker.log.debug("%s %s - %s", req.method, req.path, resp.status)

def worker_abort(worker):
    worker.log.info("worker received SIGABRT signal") 