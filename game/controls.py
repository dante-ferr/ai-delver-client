from pyglet import window


class Controls:
    keys: window.key.KeyStateHandler

    def __init__(self, keys: window.key.KeyStateHandler):
        self.keys = keys

    def update(self, dt):
        if self.keys[window.key.LEFT]:
            self.skeleton.set_angle(self.skeleton.angle - 2)
        elif self.keys[window.key.RIGHT]:
            self.skeleton.set_angle(self.skeleton.angle + 2)
