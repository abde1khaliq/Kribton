class Route:
    def __init__(self, path, handler):
        self.path = path
        self.handler = handler

    def matches(self, scope):
        return self.path == scope['path']