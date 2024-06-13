import requests
from bs4 import BeautifulSoup


class Base:
    def __init__(self, url):
        self.base_url = url
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': 'fpestid=9KzYLS2gv_-Nu5avVpd27tcW9Ps3MoYM3kpOmmNBk_SHesktbt1oObLlRRiut2_UsMlyUg; hubspotutk=e155a5670fe68fe35cbb61fe96e17be4; ak_cookieconsent_status=allow; nitroCachedPage=0; _gid=GA1.2.1634874069.1718253370; __hstc=128850451.e155a5670fe68fe35cbb61fe96e17be4.1717653034568.1717653034568.1718253370727.2; __hssrc=1; _ga=GA1.1.1205728877.1717653029; _ga_27MSJXLYFZ=GS1.2.1718253370.2.1.1718253645.0.0.0; __hssc=128850451.2.1718253370727; _ga_4YR50D3B4D=GS1.1.1718253369.2.1.1718253651.0.0.0',
            'priority': 'u=0, i',
            'referer': 'https://franchisesuppliernetwork.com/',
            'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
        }
        self.payload = {}

    def get_resp(self, url):
        response = requests.request("GET", url, headers=self.headers, data=self.payload)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            return soup
        return None
