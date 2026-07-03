"""Groups related routes so they can be registered on the app together.

Defines :class:`Router`, a thin collector of
:class:`~kribton.route.Route` objects — build one up per feature area with
:meth:`Router.append_route`, then hand the whole thing to
:meth:`kribton.core.Kribton.add_router`.

Depends on:
    - :class:`kribton.route.Route` — created by :meth:`append_route`.

Used by:
    - :class:`kribton.core.Kribton` — consumes ``router.routes`` in
      :meth:`~kribton.core.Kribton.add_router`.
"""

from kribton.route import Route


class Router:
    """Collects :class:`~kribton.route.Route` objects for batch registration.

    Example:
        >>> router = Router()
        >>> router.append_route("/ping", ping_handler)
        >>> app.add_router(router)
    """

    def __init__(self):
        """Create a router with an empty ``routes`` list."""
        self.routes = []

    def append_route(self, path, handler):
        """Build a GET route and append it to ``self.routes``.

        Note:
            This does **not** accept a ``methods`` argument, so every route
            created here defaults to :class:`~kribton.route.Route`'s
            built-in ``["GET"]``. For a non-GET route on a router, append a
            ``Route`` directly instead::

                router.routes.append(Route("/items", create_item, methods=["POST"]))

            or register it on the app with
            :meth:`kribton.core.Kribton.add_route`, which does take
            ``methods`` explicitly.

        Args:
            path: URL path to match.
            handler: Async callable taking a
                :class:`~kribton.request.Request` and returning a
                :class:`~kribton.response.Response`.
        """
        self.routes.append(Route(path, handler))