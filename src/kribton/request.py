"""Wraps an incoming ASGI scope/receive pair for handler code.

Defines :class:`Request`, the object every route handler receives as its
argument.

Used by:
    - :class:`kribton.core.Kribton` — constructed once per connection in
      :meth:`~kribton.core.Kribton.__call__` and passed to the matched
      route's handler.
"""

import json


class Request:
    """A single incoming HTTP request, wrapping the raw ASGI scope.

    Attributes:
        path (str): ``scope["path"]``.
        method (str): ``scope["method"]``.
        headers (list[tuple[str, str]]): Decoded ``(name, value)`` header
            pairs from ``scope["headers"]``.

    Note:
        The body is *not* read at construction time — it's pulled lazily
        from ``receive`` the first time :meth:`body` or :meth:`json` is
        called, then cached.
    """

    def __init__(self, scope, receive):
        """Wrap an ASGI scope/receive pair.

        Args:
            scope: The ASGI connection scope.
            receive: The ASGI receive callable, used lazily by
                :meth:`body`.
        """
        self._scope = scope
        self._receive = receive
        self._body = None
        self.path = self._scope["path"]
        self.method = self._scope["method"]
        self.headers = [
            (m.decode(), n.decode()) for m, n in self._scope.get("headers", [])
        ]

    async def body(self):
        """Read and return the full request body as bytes.

        Drains ``receive`` message by message until ``more_body`` is falsy,
        concatenating each chunk. The result is cached on ``self._body``, so
        calling this more than once only reads the wire once.

        Returns:
            bytes: The raw request body.
        """
        if self._body is None:
            chunks = []
            while True:
                message = await self._receive()
                if message["type"] == "http.request":
                    chunks.append(message.get("body", b""))
                    if not message.get("more_body", False):
                        break
            self._body = b"".join(chunks)
        return self._body

    async def json(self):
        """Read the body and parse it as JSON.

        Calls :meth:`body`, decodes it as UTF-8, then ``json.loads`` it.

        Note:
            Any failure — empty body, invalid UTF-8, malformed JSON — is
            swallowed and results in ``{}`` rather than an exception. A
            missing body and a malformed one therefore look identical to
            the caller; parse ``body()`` directly if you need to tell them
            apart.

        Returns:
            dict | list: The parsed JSON, or ``{}`` on any failure.
        """
        try:
            return json.loads((await self.body()).decode("utf-8"))
        except Exception:
            return {}