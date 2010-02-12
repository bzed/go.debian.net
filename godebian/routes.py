from bottle import route, view

@route('/')
def index():
    return 'Hello World!'


