# log_utils.py

import datetime


def get_current_time():
    return datetime.datetime.now().strftime('[%H:%M:%S]')


def log_error(*args):
    current_time = get_current_time()
    message = ' '.join(str(arg) for arg in args)
    print("\033[31m" + current_time + " " + message + "\033[0m")


def log_success(*args):
    current_time = get_current_time()
    message = ' '.join(str(arg) for arg in args)
    print("\033[32m" + current_time + " " + message + "\033[0m")


def log_info(*args):
    current_time = get_current_time()
    message = ' '.join(str(arg) for arg in args)
    print("\033[34m" + current_time + " " + message + "\033[0m")
