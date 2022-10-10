"""Gunicorn *development* config file"""

# Django WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
wsgi_app = "Economic_Indicators.wsgi:application"
# The granularity of Error log outputs
loglevel = "debug"
# The number of worker processes for handling requests
workers = 2
# The socket to bind
bind = "0.0.0.0:8015"
# Restart workers when code changes (development only!)
reload = False
preload = True
# Write access and error info to /var/log
accesslog = errorlog = "/Users/dawidpylak/Documents/Economic_Indicators/conf/dev.log"
# Redirect stdout/stderr to log file
capture_output = True
# PID file so you can easily fetch process ID
pidfile = "/Users/dawidpylak/Documents/Economic_Indicators/conf/dev.pid"
# Daemonize the Gunicorn process (detach & enter background)
daemon = True
