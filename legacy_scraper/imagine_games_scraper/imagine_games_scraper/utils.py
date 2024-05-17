from datetime import datetime

def is_timestamp(str, format='%Y-%m-%d %H:%M:%S'):
    try:
        datetime.strptime(str, format)
        return True
    except ValueError:
        return False