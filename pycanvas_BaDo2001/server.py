import asyncio
import sys
import os
import signal
import json
import tornado.web
import tornado.websocket
import logging

class WebServer(tornado.web.RequestHandler):
        def get(self):
            self.render("./static/index.html")

class WebSocketConnection(tornado.websocket.WebSocketHandler):
    def initialize(self, on_connection):
        self.on_connection = on_connection
        self.on_image_loaded = None
        self.on_event = None
        self.is_active = False

    def open(self):
        self.is_active = True
        self.on_connection(self)

    def send_one(self, type, payload):
        if self.is_active: self.write_message({"type": type, "payload": payload})

    def send_batch(self, calls):
        if self.is_active: self.write_message({"type": "batch", "payload": calls})

    def on_message(self, message):
        data = json.loads(message)
        if data["type"] == "error":
            print(data["payload"])
        elif data["type"] == "image_loaded":
            self.on_image_loaded()
        elif data["type"] == "event":
            self.on_event(data["payload"])

    def check_origin(self, origin):
        return True

    def on_close(self):
        self.is_active = False

def create_server(on_connection):
    #logging.basicConfig(level=logging.CRITICAL)

    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    return tornado.web.Application([
        (r"/", WebServer),
        (r"/ws", WebSocketConnection, {"on_connection": on_connection})
    ], static_path=os.path.join(os.path.dirname(__file__), "static"))

def handle_interrupt(ioloop):
    def shutdown(*args):
        ioloop.stop()
        
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)
    
    periodic_check = lambda *args: ioloop.call_later(0.1, periodic_check)
    periodic_check()
