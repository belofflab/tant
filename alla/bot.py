import aiohttp_cors
import json
from datetime import datetime, timedelta
from aiohttp.web_app import Application
from aiohttp_cors import CorsViewMixin
from aiogram.dispatcher.webhook import get_new_configured_app
from loader import dp, bot, analytics
from database.models import db, User, ServiceType, Service
from dataclasses import dataclass, fields
import jinja2
from decimal import Decimal
import aiohttp_jinja2
from data.config import (
    BASE_DIR,
    WEB_APP_DOMAIN,
    WEB_APP_HOST,
    WEB_APP_PORT,
    WEB_APP_WEBHOOK,
)
from aiohttp import web

WEBHOOK_URL = WEB_APP_DOMAIN + WEB_APP_WEBHOOK

@dataclass
class Serializer:
    @classmethod
    async def serialize(cls, model_instance):
        data = {}
        for column in model_instance.__table__.columns:
            field_value = getattr(model_instance, column.name)
            if isinstance(field_value, Decimal):
                field_value = str(field_value)
            data[column.name] = field_value
        return data


class IndexView(web.View, CorsViewMixin):
    async def get(self):
        context = {"page_name": "Аналитика"}
        response = aiohttp_jinja2.render_template(
            "index.html", self.request, context=context
        )
        return response

class ServiceTypesView(web.View, CorsViewMixin):
    async def get(self):
        response = aiohttp_jinja2.render_template(
            "service-types.html", self.request, context={"page_name": "Категории"}
        )
        return response

class ServicesView(web.View, CorsViewMixin):
    async def get(self):
        response = aiohttp_jinja2.render_template(
            "services.html", self.request, context={"page_name": "Услуги"}
        )
        return response


async def on_startup(app: Application):
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(BASE_DIR / "templates"))
    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers="*", allow_headers="*"
            )
        },
    )
    cors.add(app.router.add_view("/", IndexView))
    cors.add(app.router.add_view("/service/types/", ServiceTypesView))
    cors.add(app.router.add_view("/services/", ServicesView))


    webhook = await bot.get_webhook_info()
    if webhook.url != WEBHOOK_URL:
        if not webhook.url:
            await bot.delete_webhook()
        await bot.set_webhook(WEBHOOK_URL)


if __name__ == "__main__":
    import handlers
    app = get_new_configured_app(dp, path=WEB_APP_WEBHOOK)
    app.on_startup.append(on_startup)
    web.run_app(app, host=WEB_APP_HOST, port=WEB_APP_PORT)
