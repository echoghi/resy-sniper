# log_utils.py

def log_error(*args):
    # Join all arguments into a single string with a space separator
    message = ' '.join(str(arg) for arg in args)
    print("\033[31m" + message + "\033[0m")  # Red for errors


def log_success(*args):
    message = ' '.join(str(arg) for arg in args)
    print("\033[32m" + message + "\033[0m")  # Green for success


def log_info(*args):
    message = ' '.join(str(arg) for arg in args)
    print("\033[34m" + message + "\033[0m")  # Blue for information
