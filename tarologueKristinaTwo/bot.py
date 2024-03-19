import aiohttp_cors
import json
from datetime import datetime, timedelta
from aiohttp.web_app import Application
from aiohttp_cors import CorsViewMixin
from aiogram.dispatcher.webhook import get_new_configured_app
from loader import dp, bot
from database.models import db, User, ServiceType, Service
from dataclasses import dataclass, fields
import jinja2
from decimal import Decimal
import aiohttp_jinja2
from data.config import (
    BASE_DIR,
    DATABASE_URL,
    WEB_APP_DOMAIN,
    WEB_APP_HOST,
    WEB_APP_PORT,
    WEB_APP_WEBHOOK,
)
from aiohttp import web

WEBHOOK_URL = WEB_APP_DOMAIN + WEB_APP_WEBHOOK


class ShortCutView(web.View, CorsViewMixin):
    async def get(self):
        return web.Response(status=200)


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
        users = await User.query.gino.all()
        today = datetime.now() - timedelta(days=1)
        active_users_today = await User.query.where(
            User.last_active >= today
        ).gino.all()
        services = await Service.query.gino.all()
        service_types = await ServiceType.query.gino.all()
        context = {
            "users": users,
            "active_users_today": active_users_today,
            "services": services,
            "service_types": service_types,
        }
        response = aiohttp_jinja2.render_template(
            "index.html", self.request, context=context
        )

        return response


class ServiceTypesAPIView(web.View, CorsViewMixin):
    async def get(self):
        service_types = await ServiceType.query.gino.all()

        return web.json_response(
            [await Serializer.serialize(service_type) for service_type in service_types]
        )

    async def delete(self):
        idx = self.request.query.get("idx")
        if not idx:
            return web.json_response({"status": False})
        await ServiceType.delete.where(ServiceType.idx == int(idx)).gino.status()
        return web.json_response({"status": True})

    async def put(self):
        idx = self.request.query.get("idx")
        name = self.request.query.get("serviceTypeName")
        if idx:
            await ServiceType.update.values(name=name).where(
                ServiceType.idx == int(idx)
            ).gino.status()
            service_type = await ServiceType.query.where(
                ServiceType.idx == int(idx)
            ).gino.first()
        else:
            service_type = await ServiceType.create(name=name)

        return web.json_response(
            {"status": True, "data": await Serializer.serialize(service_type)}
        )


class ServiceTypesView(web.View, CorsViewMixin):
    async def get(self):
        response = aiohttp_jinja2.render_template(
            "service-types.html", self.request, context={}
        )

        return response


class ServicesAPIView(web.View, CorsViewMixin):
    async def get(self):
        service_types = await ServiceType.query.gino.all()
        services = await Service.query.gino.all()

        return web.json_response(
            {
                "status": True,
                "service_types": [
                    await Serializer.serialize(service) for service in service_types
                ],
                "services": [
                    await Serializer.serialize(service) for service in services
                ],
            }
        )

    async def delete(self):
        idx = self.request.query.get("idx")
        if not idx:
            return web.json_response({"status": False})
        await Service.delete.where(Service.idx == int(idx)).gino.status()
        return web.json_response({"status": True})

    async def put(self):
        idx = self.request.query.get("idx")
        name = self.request.query.get("servicesName")
        servicesDescription = self.request.query.get("servicesDescription")
        servicesPrice = self.request.query.get("servicesPrice")
        servicesType = self.request.query.get("type")
        if servicesType == "null" or servicesType is None: 
            servicesType = None
        else:
            servicesType = int(servicesType)
        if idx:
            await Service.update.values(
                name=name, description=servicesDescription, amount=servicesPrice, type=servicesType
            ).where(Service.idx == int(idx)).gino.status()
            service = await Service.query.where(
                Service.idx == int(idx)
            ).gino.first()
        else:
            service = await Service.create(
                name=name, description=servicesDescription, amount=servicesPrice, type=servicesType
            )

        return web.json_response(
            {"status": True, "data": await Serializer.serialize(service)}
        )


class ServicesView(web.View, CorsViewMixin):
    async def get(self):
        response = aiohttp_jinja2.render_template(
            "services.html", self.request, context={}
        )

        return response


class BillingView(web.View, CorsViewMixin):
    async def get(self):
        context = {"current_date": "January 27, 2017"}
        response = aiohttp_jinja2.render_template(
            "billing.html", self.request, context=context
        )

        return response


class ProfileView(web.View, CorsViewMixin):
    async def get(self):
        context = {"current_date": "January 27, 2017"}
        response = aiohttp_jinja2.render_template(
            "profile.html", self.request, context=context
        )

        return response


class DashboardView(web.View, CorsViewMixin):
    async def get(self):
        context = {"current_date": "January 27, 2017"}
        response = aiohttp_jinja2.render_template(
            "dashboard.html", self.request, context=context
        )

        return response


class TablesView(web.View, CorsViewMixin):
    async def get(self):
        context = {"current_date": "January 27, 2017"}
        response = aiohttp_jinja2.render_template(
            "tables.html", self.request, context=context
        )

        return response


async def on_startup(app: Application):
    await db.set_bind(DATABASE_URL)
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(BASE_DIR / "templates"))
    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers="*", allow_headers="*"
            )
        },
    )
    cors.add(app.router.add_view("/s/{shortcut_id}", ShortCutView))
    cors.add(app.router.add_view("/", IndexView))
    cors.add(app.router.add_view("/service/types/", ServiceTypesView))
    cors.add(app.router.add_view("/services/", ServicesView))
    cors.add(app.router.add_view("/pages/billing", BillingView))
    cors.add(app.router.add_view("/pages/profile", ProfileView))
    cors.add(app.router.add_view("/pages/tables", TablesView))
    cors.add(app.router.add_view("/pages/dashboard", DashboardView))

    cors.add(app.router.add_view("/api/service/types/", ServiceTypesAPIView))
    cors.add(app.router.add_view("/api/services/", ServicesAPIView))

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
