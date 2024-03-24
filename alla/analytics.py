import logging
import json
import sys
import requests
import shutil
from data.config import ANALYTICS_TOKEN, SERVER_URL, BASE_DIR, WDATA_PATH


logging.basicConfig(
  format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
  datefmt="%H:%M:%S",
  level=logging.DEBUG,
)


class Analytics(requests.Session):
  def __init__(self) -> None:
    super().__init__()
    self.headers.update({"Authorization": f"Bearer {ANALYTICS_TOKEN}"})
    self.logger = logging.getLogger("analytics")

  def send_request(self, url, params: dict | None = None, json: dict | None = None) -> dict | None:
    data = None
    try:
      response = self.get(SERVER_URL + url, params=params, json=json)
      response.raise_for_status()
      data = response.json()
    except requests.exceptions.RequestException as ex:
      self.logger.error(f"Не удалось получить информацию {url}: {ex}")
    return data
  
  @staticmethod
  def set_worker_data(wdata: dict) -> None:
    with open(BASE_DIR / WDATA_PATH, "w", encoding="utf-8") as f:
      json.dump(wdata, f, ensure_ascii=False)

  @staticmethod
  def get_worker_data() -> dict:
    return json.loads( open(BASE_DIR / WDATA_PATH, "r", encoding="utf-8").read())
  
  def start(self):
    MEDIA_SERVER_URL = SERVER_URL.replace("/api/v1", "/")
    wdata = self.send_request("/worker/bots/")
    if not wdata:
      sys.exit(1)
    self.set_worker_data(wdata)
    wimres = self.get(MEDIA_SERVER_URL + wdata["bot"]["main_photo"])
    if wimres.status_code == 200:
      with open(BASE_DIR / "media/worker.jpg",'wb') as f:
        shutil.copyfileobj(wimres.raw, f)
      self.logger.info(f'Image sucessfully Downloaded')
    else:
      self.logger.info('Image Couldn\'t be retrieved')
    
    


if __name__ == "__main__":
  anal = Analytics()
  print(anal.start())