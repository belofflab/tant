import requests
from data.config import WEB_APP_WEBHOOK, WEB_APP_DOMAIN, BOT_TOKEN

WEB_APP_URL = WEB_APP_DOMAIN + WEB_APP_WEBHOOK

res = requests.get(
    f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEB_APP_URL}"
)

print(res.json())
