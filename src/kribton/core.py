"""The ASGI application core.

Defines :class:`Kribton`, the object you instantiate and hand to an ASGI
server (uvicorn, Hypercorn, Daphne, ...). It owns the flat list of routes
that requests are matched against, and is the actual ASGI callable.

Depends on:
    - :class:`kribton.request.Request` — wraps each incoming scope.
    - :class:`kribton.response.Response` — sent back for unmatched routes.
    - :class:`kribton.route.Route` — created by :meth:`Kribton.add_route`.

Used by:
    - :class:`kribton.router.Router` instances are attached via
      :meth:`Kribton.add_router`.
"""

from kribton.request import Request
from kribton.response import Response
from kribton.route import Route


class Kribton:
    """The application object; also the ASGI entry point.

    Example:
        >>> app = Kribton(title="My API")
        >>> app.add_route("/ping", ping_handler, methods=["GET"])
        # then: uvicorn mymodule:app
    """

    def __init__(self, title=None, description=None):
        """Create an empty application.

        Args:
            title: Optional human-readable name for the app.
            description: Optional short description of the app.

        Sets up:
            routers (list[Router]): Every router registered via
                :meth:`add_router`.
            routes (list[Route]): The flat, ordered list of routes actually
                matched against incoming requests. Populated by both
                :meth:`add_router` and :meth:`add_route`.
        """
        self.title = title
        self.description = description
        self.routers = []
        self.routes = []

    def add_router(self, router):
        """Register a :class:`~kribton.router.Router` and adopt its routes.

        Appends ``router`` to ``self.routers`` and copies every route it has
        collected so far onto ``self.routes``. Routes appended to the router
        *after* this call will not be picked up — finish building the
        router, then register it.

        Args:
            router: A :class:`~kribton.router.Router` populated with
                :class:`~kribton.route.Route` objects.
        """
        self.routers.append(router)
        self.routes.extend(router.routes)

    def add_route(self, path, handler, methods):
        """Register a single route directly on the app.

        Bypasses :class:`~kribton.router.Router` entirely — useful for
        one-off routes, or when you need to pass ``methods`` explicitly
        (see the note on :meth:`Router.append_route
        <kribton.router.Router.append_route>` about its default-only
        behavior).

        Args:
            path: URL path to match, e.g. ``"/users"``.
            handler: Async callable taking a
                :class:`~kribton.request.Request` and returning a
                :class:`~kribton.response.Response`.
            methods: HTTP methods this route responds to, e.g.
                ``["GET", "POST"]``.
        """
        self.routes.append(Route(path, handler, methods))

    async def __call__(self, scope, receive, send):
        """ASGI application callable — invoked by the server per connection.

        Wraps ``scope``/``receive`` in a :class:`~kribton.request.Request`,
        then walks ``self.routes`` in registration order calling
        :meth:`Route.matches <kribton.route.Route.matches>` on each. On the
        first match, awaits ``route.handler(request)`` and sends the
        resulting :class:`~kribton.response.Response`. If nothing matches,
        sends a plain 404.

        Note:
            Route matching is a linear scan with no indexing, so lookup
            time grows with the number of registered routes.

        Args:
            scope: The ASGI connection scope.
            receive: The ASGI receive callable.
            send: The ASGI send callable.
        """
        request = Request(scope, receive)

        for route in self.routes:
            if route.matches(scope):
                response = await route.handler(request)
                await response.send(send)
                return

        response = Response("Not Found", status=404)
        await response.send(send)