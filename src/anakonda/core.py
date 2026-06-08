from anakonda.route import Route
from anakonda.request import Request
from anakonda.response import Response

class Konda:
    def __init__(self, title=None, description=None):
        self.title = title
        self.description = description
        self.routers = []
        self.routes = []

    def add_router(self, router):
        self.routers.append(router)
        self.routes.extend(router.routes)

    def add_route(self, path, handler):
        self.routes.append(Route(path, handler))

    async def __call__(self, scope, receive, send):
        request = Request(scope, receive)

        for route in self.routes:
            if route.matches(scope):
                response = await route.handler(request)
                await response.send(send)
                return


        response = Response("Not Found", status=404)
        await response.send(send)