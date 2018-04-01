#!/usr/bin/env python

from bottle import Bottle, BaseRequest, template


def get_app():
    app = Bottle()
    app.get('/health', callback=health)
    app.get('/hello/<name>', callback=index)
    return app


def health():
    return 'I am doing perfectly fine.'


def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)


BaseRequest.MEMFILE_MAX = 1024 * 512 * 2
app = get_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=True)
