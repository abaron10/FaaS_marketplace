import os

def get_base_url():
    return os.environ.get('BASE_URL', '')

