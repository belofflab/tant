from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .utils.scraper import start_scrape
import base64

app = FastAPI()


@app.get("/matrix/{date}")
async def matrix_date(date: str) -> None:
    screenshot_binary, matrix = await start_scrape(
        url=f"https://matrix.belofflab.com/?date={date}"
    )
    matrix_data = {
        "matrix": matrix,  # Add other data fields as needed
    }

    image_data = base64.b64encode(screenshot_binary.read()).decode("utf-8")
    matrix_data["image"] = image_data

    return JSONResponse(content=matrix_data, media_type="application/json")
