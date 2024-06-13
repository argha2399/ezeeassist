import logging
import pandas as pd
from tqdm import tqdm
from src.scrapers.base import Base as base
from concurrent.futures import ThreadPoolExecutor


class Scraper(base):
    def __init__(self, url="https://franchisesuppliernetwork.com/"):
        super().__init__(url)

    def scrape_data(self):
        try:
            soup = self.get_resp(url=self.base_url)
            headers = soup.find('header', class_='header')
            header_elements = headers.find_all('ul', class_='slimmenu')
            header_links = [header.find('a')['href'] for header in header_elements]
            header_links = []
            for ele in header_elements[0].find_all('a'):
                header_links.append(ele['href'])

            def scrape_general(x):
                df_dict = {
                    "url": [],
                    "all_text": [],
                    "all_images": []
                }
                soup = self.get_resp(url=x)
                all_text = ' '.join([tag.get_text() for tag in soup.find_all('p')])
                all_img = ' | '.join([tag['src'] for tag in soup.find_all('img')])
                df_dict['all_text'].append(all_text)
                df_dict['all_images'].append(all_img)
                df_dict['url'].append(x)
                return pd.DataFrame(df_dict)
            with ThreadPoolExecutor(20) as exe:
                res = list(tqdm(exe.map(scrape_general, header_links), total=len(header_links)))
            df_final = pd.concat(res, ignore_index=True)
            return df_final
        except Exception as e:
            logging.error("Failed to scrape home page", exc_info=e)

    def run(self):
        df = self.scrape_data()
        return df
