import multiprocessing
wsgi_app = 'app:app'
bind = "0.0.0.0:8081"
#daemon = True
workers = multiprocessing.cpu_count() * 2 + 1
#accesslog = "./log/access_log"
#errorlog = "./log/error_log"