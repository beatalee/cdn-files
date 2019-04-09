import random

from .models import WebServerHost

def get_random_port():
    _port = 20000 + int(33000 * (random.random()))

    if _port in [x.server_port for x in WebServerHost.objects.all() ]:
        get_random_port()

    return _port