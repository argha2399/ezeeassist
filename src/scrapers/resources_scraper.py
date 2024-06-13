import logging
import pandas as pd
from tqdm import tqdm
from src.scrapers.base import Base as base
from concurrent.futures import ThreadPoolExecutor


class Scraper(base):
    def __init__(self, url="https://franchisesuppliernetwork.com/resources/"):
        super().__init__(url)

    def find_all_projects(self):
        try:
            soup = self.get_resp(url=self.base_url)
            nav_text = soup.find('div', class_='wp-pagenavi').find('span', class_='pages')
            total_pages = int(nav_text.get_text().split(' ')[-1])
            all_outer_pages = [self.base_url + 'page/' + str(i) for i in range(2, total_pages + 1)]
            all_outer_pages.append(self.base_url)

            def get_all_details(page):
                headings = []
                short_desc = []
                proj_link = []
                proj_thumbnail = []
                detail_text_in_page = []
                all_images_in_page = []
                soup = self.get_resp(url=page)
                projects_lst = soup.find_all('div', class_='single-news Post')
                for proj in projects_lst:
                    headings.append(proj.find('h3').get_text())
                    short_desc.append(proj.find('p').get_text())
                    proj_link.append(proj.find('a')['href'])
                    proj_thumbnail.append(proj.find('img')['src'])
                for url in proj_link:
                    soup = self.get_resp(url=url)
                    text_in_page = [soup.find_all('p')[i].get_text() for i in range(len(soup.find_all('p')))]
                    text_in_page = ', '.join(text_in_page)
                    text_in_page = text_in_page.replace('\n', '')
                    images_in_page = [soup.find_all('img')[i] for i in range(len(soup.find_all('img')))]
                    images_in_page = [image.get('src') for image in images_in_page]
                    images_in_page = ' | '.join(images_in_page)
                    detail_text_in_page.append(text_in_page)
                    all_images_in_page.append(images_in_page)
                df_outer_table = pd.DataFrame([headings, short_desc, proj_link, proj_thumbnail, detail_text_in_page, all_images_in_page]).T
                df_outer_table.columns = ['heading', 'short_desc', 'project_url', 'image_thumbnail', 'detail_text', 'image_link']
                return df_outer_table
            with ThreadPoolExecutor(4) as exe:
                res = list(tqdm(exe.map(get_all_details, all_outer_pages), total=len(all_outer_pages)))
            df_final = pd.concat(res, ignore_index=True)
            return df_final
        except Exception as e:
            logging.error("Failed to scrape resources tables", exc_info=e)

    def run(self):
        df = self.find_all_projects()
        df.drop_duplicates(inplace=True)
        return df
