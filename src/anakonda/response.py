class Response:
    def __init__(self, content, status=200, headers=None):
        self.content = content.encode("utf-8") if isinstance(content, str) else content
        self.status = status
        self.headers = headers or [(b"content-type", b"text/plain")]

    async def send(self, send):
        headers = [[m, n] for (m, n) in self.headers]
        await send(
            {"type": "http.response.start", "status": self.status, "headers": headers}
        )

        await send({"type": "http.response.body", "body": self.content})
