from pycanvas.utils import get_encoded_img, convert_event_data
import tornado.ioloop

class Canvas:
    def __init__(self, socket_connection):
        self.width = 300
        self.height = 150
        self.ioloop = tornado.ioloop.IOLoop.instance()
        self.socket_connection = socket_connection
        self.socket_connection.on_image_loaded = self.on_image_loaded
        self.socket_connection.on_event = self.on_event
        self.canvas_calls = []
        self.variables = []
        self.events = []
        self.images_not_ready = 0

    def set_size(self, width, height):
        self.width = width
        self.height = height
        self.socket_connection.send_one("setup", {"width": self.width, "height": self.height})

    def load_image(self, path, id):
        self.images_not_ready += 1
        self.socket_connection.send_one("image", {"image": get_encoded_img(path), "id": id})
        return id

    def on_image_loaded(self):
        self.images_not_ready -= 1

    def on_event(self, event):
        self.events.append(convert_event_data(event["type"], event["payload"]))

    def get_event(self):
        while len(self.events) > 0:
            yield self.events.pop(0)

    def clear(self):
        self.canvas_calls.append(["draw", {"type": "clearRect", "payload": [0, 0, self.width, self.height]}])

    def clear_rect(self, x, y, width, height):
        self.canvas_calls.append(["draw", {"type": "clearRect", "payload": [x, y, width, height]}])

    def fill_rect(self, x, y, width, height, color):
        self.canvas_calls.append(["draw", {"type": "fillRect", "payload": [x, y, width, height, color]}])

    def stroke_rect(self, x, y, width, height, color):
        self.canvas_calls.append(["draw", {"type": "strokeRect", "payload": [x, y, width, height, color]}])

    def fill_circle(self, x, y, r, color, start_angle=0, end_angle=360):
        self.canvas_calls.append(["draw", {"type": "fillCircle", "payload": [x, y, r, color, start_angle, end_angle]}])

    def stroke_circle(self, x, y, r, color, start_angle=0, end_angle=360):
        self.canvas_calls.append(["draw", {"type": "strokeCircle", "payload": [x, y, r, color, start_angle, end_angle]}])

    def line(self, x1, y1, x2, y2, color, line_width=1):
        self.canvas_calls.append(["draw", {"type": "line", "payload": [x1, y1, x2, y2, color, line_width]}])

    def image(self, img_id, sx=None, sy=None, sw=None, sh=None, dx=None, dy=None, dw=None, dh=None):
        payload = [img_id]+[item for item in [sx, sy, sw, sh, dx, dy, dw, dh] if item is not None]
        self.canvas_calls.append(["draw", {"type": "image", "payload": payload}])

    def start_loop(self, update_function):
        if self.images_not_ready == 0:
            self.canvas_calls = []
            self.variables = update_function(self.variables)
            self.socket_connection.send_batch(self.canvas_calls)
        self.ioloop.call_later(1/60, self.start_loop, update_function)

    def is_running(self):
        return self.socket_connection.is_active

    def create_variable(self, value):
        self.variables.append(value)
        return value