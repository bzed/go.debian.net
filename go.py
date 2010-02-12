from routes import *
from bottle import run

import sys

def runserver(host='localhost', port=8080):
    try:
        from bottle import PasteServer
    except ImportError:
        run(host=host, port=port)
    else:
        run(host=host, port=port, server=PasteServer)

if __name__ == '__main__':

    if len(sys.argv) > 1:
        host, port = argv[1].split(':')
        runserver(host, port)
    else:
        runserver()

