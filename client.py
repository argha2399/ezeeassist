import os
import warnings
from tqdm import tqdm
import logging as _logging
from src.image_scraper.image_process import process_image
from concurrent.futures import ThreadPoolExecutor
from src.scrapers.home_scraper import Scraper as home
from src.scrapers.resources_scraper import Scraper as resource
from src.scrapers.fns_supplier_scraper import Scraper as fns_supplier


def log_level():
    _log_level = os.getenv('LOG_LEVEL', 'INFO')
    return _log_level


logging = _logging.getLogger()
logging.setLevel(level=log_level())
warnings.filterwarnings(action="ignore")


if __name__ == '__main__':
    logging.info("Scraping Home Page and related pages...")
    obj = home()
    df3 = obj.run()
    df3.to_csv("sample_3.csv", index=None)
    logging.info("Done...")

    logging.info("Scraping FSN Supplier Tables...")
    obj = fns_supplier()
    df2 = obj.run()
    df2.to_csv("sample_2.csv", index=None)
    logging.info("Done...")

    logging.info("Scraping Resource Page...")
    obj = resource()
    df1 = obj.run()
    df1.to_csv("sample_1.csv", index=None)
    logging.info("Done...")

    logging.info("Processing Images...")
    images_1 = list(df1['image_thumbnail'])
    images_2 = list(df1['image_link'])
    images_3 = list(df2['images'])
    images_4 = list(df3['all_images'])
    all_images_pre = [*images_1, *images_2, *images_3, *images_4]
    all_images_post = []

    def process_img(x):
        all_images_post.extend(x.split(' | '))
    with ThreadPoolExecutor(20) as exe:
        list(tqdm(exe.map(process_img, all_images_pre), total=len(all_images_pre)))

    all_images_post = list(set(all_images_post))
    num_itm_dict = [{"num": num, "itm": itm} for num, itm in enumerate(all_images_post)]
    with ThreadPoolExecutor(20) as exe:
        list(tqdm(exe.map(process_image, num_itm_dict), total=len(num_itm_dict)))
    logging.info("Done...")
