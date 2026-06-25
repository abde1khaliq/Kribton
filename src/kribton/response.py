import json

class Response:
    def __init__(self, content, status=200, headers=None):
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
