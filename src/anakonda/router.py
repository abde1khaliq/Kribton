from .route import Route

class Router:
    def __init__(self):
        self.routes = []

    def append_route(self, path, handler):
        self.routes.append(Route(path, handler))