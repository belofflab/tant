import aiohttp_cors
from pathlib import Path
from aiohttp import web

BASE_DIR = Path(__name__).resolve()

if __name__ == "__main__":

    app = web.Application()
    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers="*", allow_headers="*"
            )
        },
    )
    cors.add(app.router.add_static('/static/', path='./static/', name='static'))
    web.run_app(app, host="0.0.0.0", port=3490)
