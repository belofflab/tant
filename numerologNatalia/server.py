import aiohttp_cors
from data.config import DATABASE_URL
from aiohttp import web
from aiohttp.web_request import Request
from database import models
from data.config import SERVER_PORT


async def create_db(app):
    await models.db.set_bind(DATABASE_URL)


app = web.Application()
app.on_startup.append(create_db)


async def create_user_template(name, users):
    user_template = await models.UserTemplate.create(name=name)
    bot_users = [user.idx for user in await models.User.query.gino.all()]
    for user in users:
        if user.get("id") not in bot_users:
            continue
        await models.UserUserTemplateAssociation.create(
            user_template_id=user_template.idx, user_id=user.get("id")
        )
    return user_template


async def send_message_to_user(request: Request):
    data = await request.json()
    user_template = await create_user_template(
        data.get("template_name"), data.get("users")
    )
    return web.json_response({"user_template": user_template.idx})


app.router.add_post("/api", send_message_to_user)

if __name__ == "__main__":
    cors = aiohttp_cors.setup(
        app,
        defaults={
            "https://tant.belofflab.com": aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers="*", allow_headers="*"
            )
        },
    )

    for route in list(app.router.routes()):
        cors.add(route)
    web.run_app(app, port=SERVER_PORT)
