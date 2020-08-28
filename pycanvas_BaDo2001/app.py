from pycanvas.server import create_server, handle_interrupt
import tornado.ioloop
from pycanvas.canvas import Canvas

def start_app(entry_point):
    print("Go to http://127.0.0.1:5000 to visit the canvas.")
    print("Press Ctrl+C to stop.")

    def on_connection(ws_socket_connection):
        entry_point(Canvas(ws_socket_connection))

    server = create_server(on_connection)
    ioloop = tornado.ioloop.IOLoop.instance()
    handle_interrupt(ioloop)

    server.listen(5000)
    ioloop.start()

