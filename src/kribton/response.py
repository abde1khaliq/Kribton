"""Builds and sends the outgoing ASGI response.

Defines :class:`Response`, returned by route handlers and sent back to the
client by :meth:`kribton.core.Kribton.__call__`.

Used by:
    - :class:`kribton.core.Kribton` — sends a 404 ``Response`` directly when
      no route matches, and calls :meth:`Response.send` on whatever a
      handler returns.
"""

import json


class Response:
    """An HTTP response, built from arbitrary Python content.

    The content type is chosen automatically from the type of ``content``
    unless ``headers`` is supplied, in which case it's used as-is (it
    replaces the default entirely rather than merging with it).

    | ``content`` type          | Encoding                     | Default ``Content-Type``   |
    | -------------------------- | ----------------------------- | ---------------------------- |
    | ``dict`` / ``list``         | ``json.dumps`` -> UTF-8        | ``application/json``         |
    | ``str``                    | UTF-8 encode                  | ``text/plain``               |
    | ``bytes`` / ``bytearray``   | used as-is                    | ``application/octet-stream`` |
    | anything else               | ``str(content)`` -> UTF-8      | ``text/plain``                |
    """

    def __init__(self, content, status=200, headers=None):
        """Build a response.

        Args:
            content: The response body — a ``dict``/``list`` (JSON-encoded),
                a ``str`` (UTF-8 text), ``bytes``/``bytearray`` (sent as-is),
                or anything else (stringified).
            status: HTTP status code. Defaults to ``200``.
            headers: Raw ``(name: bytes, value: bytes)`` header pairs. When
                given, overrides the type-based default ``Content-Type``
                entirely — remember to set your own if you customize
                headers on a JSON/text response.
        """
        if isinstance(content, (dict, list)):
            self.content = json.dumps(content).encode("utf-8")
            self.headers = headers or [(b"content-type", b"application/json")]
        elif isinstance(content, str):
            self.content = content.encode("utf-8")
            self.headers = headers or [(b"content-type", b"text/plain")]
        elif isinstance(content, (bytes, bytearray)):
            self.content = content
            self.headers = headers or [(b"content-type", b"application/octet-stream")]
        else:
            self.content = str(content).encode("utf-8")
            self.headers = headers or [(b"content-type", b"text/plain")]

        self.status = status

    async def send(self, send):
        """Send this response over ASGI.

        Emits the standard two-message sequence: ``http.response.start``
        (status + headers) followed by ``http.response.body`` (the encoded
        content).

        Args:
            send: The ASGI send callable.
        """
        headers = [[m, n] for (m, n) in self.headers]
        await send({
            "type": "http.response.start",
            "status": self.status,
            "headers": headers,
        })
        await send({
            "type": "http.response.body",
            "body": self.content,
        })