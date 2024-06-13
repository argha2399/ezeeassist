import io
import logging
import requests
from PIL import Image
from pathlib import Path
from src.scrapers.base import Base


def process_image(element):
    try:
        url = element['itm']
        parent = Base(url=url)
        resp = requests.request("GET", url, headers=parent.headers, data=parent.payload).content
        image_file = io.BytesIO(resp)
        image = Image.open(image_file).convert("RGB")
        file_path = Path("images", str(element["num"]) + ".png")
        image.save(file_path, "PNG", quality=80)
    except Exception:
        logging.info("Failed to save file: ", url)
