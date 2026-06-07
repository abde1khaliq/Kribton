class Konda:
    def __init__(self, title=None, description=None):
        self.title = title
        self.description = description

    async def __call__(self, scope, receive, send):
        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [
                [b'content-type', b'text/plain']
            ]
        })

        await send({
            "type": "http.response.body",
            "body": b"Hello World"
        })