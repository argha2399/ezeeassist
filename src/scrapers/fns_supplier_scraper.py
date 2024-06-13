import logging
import pandas as pd
from tqdm import tqdm
from src.scrapers.base import Base as base
from concurrent.futures import ThreadPoolExecutor


class Scraper(base):
    def __init__(self, url="https://franchisesuppliernetwork.com/fsn-suppliers/"):
        super().__init__(url)

    def find_all_outer_pages(self):
        try:
            soup = self.get_resp(url=self.base_url)
            pagination = soup.find('div', class_='wp-pagenavi')
            pagination = pagination.find('span').get_text().split(' ')
            total_pages = int(pagination[-1])
            all_pages = [f'https://franchisesuppliernetwork.com/fsn-suppliers/page/{i}/' for i in range(2, total_pages + 1)]
            all_pages.append(self.base_url)
            return all_pages
        except Exception as e:
            logging.error("Failed to scrape all outer pages", exc_info=e)

    def find_each_inner_page(self):
        try:
            all_pages = self.find_all_outer_pages()
            project_links = []
            for page in all_pages:
                soup = self.get_resp(url=page)
                outer_projects = soup.find_all('div', class_='fs-single-col')
                for proj in outer_projects:
                    project_links.append(proj.find('div', class_='fs-single').find('a')['href'])
            return project_links
        except Exception as e:
            logging.error("Failed to scrape inner page links", exc_info=e)

    def foreach_inner_find_project(self):
        try:
            project_links = self.find_each_inner_page()

            def scrape_inner(x):
                soup = base.get_resp(self, url=x)
                texts = ' '.join([ele.get_text() for ele in soup.find_all('p')])
                images = ' | '.join([ele['src'] for ele in soup.find_all('img')])
                df_inner = pd.DataFrame([images, texts]).T
                df_inner.columns = ["images", "text"]
                return df_inner
            with ThreadPoolExecutor(4) as exe:
                res = list(tqdm(exe.map(scrape_inner, project_links), total=len(project_links)))
            df_final = pd.concat(res, ignore_index=True)
            return df_final
        except Exception as e:
            logging.error("Faled to scrape inner project details", exc_info=e)

    def run(self):
        df = self.foreach_inner_find_project()
        df.drop_duplicates(inplace=True)
        return df
