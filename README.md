# uwsgi


How to install uwsgi

        $ pip install uwsgi

How to run a simple app

        $ uwsgi --http :9090 --wsgi-file foobar.py --master --processes 4 --threads 2

        $ cat foobar.py

        def application(env, start_response):
          start_response('200 OK', [('Content-Type','text/html')])
          return [b"Hello World"]

How to convert the command line params to config file

        $ cat uwsky.ini
        [uwsgi]
        http-socket = 0.0.0.0:3031
        wsgi-file = foobar.py
        processes = 4
        threads = 2
        stats = 0.0.0.0:9191
        buffer-size=32768

        http-socket -> can be accessed over http and unix socket if frontended by nginx
        process -> number of workers

        stats -> default stats url -> this will give a ton of info
        $ telnet 0.0.0.0 9191

How to put it on a real sample app

Let us take a bottle app

        $ cat server.py
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

This app has 2 uris

        /health -> just says that the app is fine
        /hello/name -> just says hello world


The configuration file for this app

        [uwsgi]
        socket = :3032
        master = True
        stats = 127.0.0.1:9192
        vacuum = True
        pythonpath = /Users/mcbobs/projects/bottle
        chdir = /Users/mcbobs/projects/bottle
        module = server
        callable = app

nginx conf for this app

        location /bapp/ {
            rewrite /bapp/(.+) /$1 break;
            include uwsgi_params;
            uwsgi_pass localhost:3032;
        }

