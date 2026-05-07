import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

from config import CATEGORIES


def pars_texno(category):
    texno_data=[]
    load_dotenv()

    URL = os.getenv("URL")
    HOST = os.getenv("HOST")
    HEADERS = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
    }
    html = requests.get(URL + category, headers=HEADERS).text
    soup = BeautifulSoup(html, 'html.parser')
    blocks = soup.find_all('div', class_='w-full [&:hover_.actions]:!flex tablet:max-w-full bg-light laptop:p-[15px] p-2.5 rounded-[16px] border-[1px] border-solid border-stroke overflow-hidden mobileS:max-w-full relative product-cart flex flex-col h-full laptop:max-w-[274px]')

    for block in blocks:
        images_link = block.find('div', class_='LazyLoad is-visible aspect-square w-full h-full')
        images = images_link.find('img').get('data-src')
        title = block.find('p', class_='text-dark tablet:text-[14px] font-[400] leading-[150%] mt-[12px] line-clamp-2 min-h-[38px] text-left text-[12px]').get_text()
        price = block.find('span', class_='tablet:text-[18px] font-[500] text-dark block text-[14px]').get_text(strip=True)

        texno_data.append({
            'images': images,
            'title': title,
            'price': price,
        })
    return texno_data


pars_texno('products/category/telefonlar-17/smartfonlar-40')
