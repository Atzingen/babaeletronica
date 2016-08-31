from gevent.wsgi import WSGIServer
from __init__ import app

http_server = WSGIServer(('',5000),app)
http_server .serve_forever()
