from .route import Route

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
        for route in self.routes:
            if route.matches(scope):
                await route.handler(scope, receive, send)

        await send({
                "type": "http.response.start",
                "status": 404,
                "headers": [
                    [b'content-type', b'text/plain']
                ]
            })

        await send({
            "type": "http.response.body",
            "body": b'Not Found.'
        })