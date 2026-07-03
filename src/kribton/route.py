"""A single path/handler binding.

Defines :class:`Route`, the smallest routing unit in the framework: a path,
an async handler, and the HTTP methods it responds to.

Used by:
    - :class:`kribton.core.Kribton` — creates a ``Route`` in
      :meth:`~kribton.core.Kribton.add_route`, and matches against every
      route in :meth:`~kribton.core.Kribton.__call__`.
    - :class:`kribton.router.Router` — creates a ``Route`` in
      :meth:`~kribton.router.Router.append_route`.
"""


class Route:
    """A single URL path bound to an async handler.

    Example:
        >>> async def create_item(request):
        ...     return Response({"ok": True}, status=201)
        >>> route = Route("/items", create_item, methods=["POST"])
    """

    def __init__(self, path, handler, methods=None):
        """Create a route.

        Args:
            path: Exact URL path to match, e.g. ``"/items"``. Matching is a
                strict string comparison — no path parameters are parsed
                here.
            handler: Async callable taking a
                :class:`~kribton.request.Request` and returning a
                :class:`~kribton.response.Response`.
            methods: HTTP methods this route responds to, e.g.
                ``["GET", "POST"]``. Defaults to ``["GET"]`` when omitted or
                falsy.
        """
        self.path = path
        self.handler = handler
        self.methods = methods or ["GET"]

    def matches(self, scope):
        """Check whether an ASGI scope matches this route.

        Compares ``scope["path"]`` for an exact match against ``self.path``,
        and checks that the uppercased ``scope["method"]`` is in
        ``self.methods``.

        Args:
            scope: The ASGI connection scope, as passed to
                :meth:`kribton.core.Kribton.__call__`.

        Returns:
            bool: ``True`` if both the path and method match.
        """
        return (
            self.path == scope["path"]
            and scope["method"].upper() in self.methods
        )