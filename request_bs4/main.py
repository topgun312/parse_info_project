#Парсер с применением библиотек requests, beautifulsoup4 для парсинга топ-1000 фильмов по данным сайта www.kinoafisha.ru с сохранением данных в .txt файле

import time
import datetime
from typing import Dict
import requests
from bs4 import BeautifulSoup as bs
from config_urls import HEADERS, SITE_URL


def parse_page_count() -> int:
    response = requests.get(SITE_URL, headers=HEADERS, timeout=10)
    html = response.content
    soup = bs(html, 'lxml')
    pages_paginate = int(soup.find('nav', class_='ratings_pagination bricks bricks-unite swipe outer-mobile inner-mobile').find_all('a')[-2].get_text())
    return pages_paginate


def parse_page():
    params: Dict[str, int] = {"page": 1}
    pages: int = parse_page_count()
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    while params["page"] <= pages:
        act_page: int = params["page"]
        if act_page == 1:
            response = requests.get(SITE_URL, headers=HEADERS, timeout=10)
        else:
            response = requests.get(SITE_URL + f'?page={act_page}', params=params, headers=HEADERS, timeout=10)
        html = response.content
        soup = bs(html, 'lxml')
        items = soup.find("div", class_="ratings_list movieList movieList-rating grid_cell9").find_all("div", class_="movieList_item movieItem movieItem-rating movieItem-position")


        with open(f'kinoafisha_{cur_time}_info.txt', 'a', encoding='utf-8') as file:
            for i in items:
                itemTitle = i.find('a', class_="movieItem_title").text
                genresItem = i.find('span', class_="movieItem_genres").text
                raitingItem = i.find('span', class_="movieItem_position").text
                year_countryItem = i.find('span', class_="movieItem_year").text
                file.write(f"{raitingItem}. Название: {itemTitle}\n Жанр:  {genresItem}\n Год и страна производства: {year_countryItem}\n")
            params["page"] += 1
            print(f'Страница номер {act_page} обработана.')

if __name__ == "__main__":
    start_time = time.time()
    parse_page()
    finish_time = time.time()
    work_time = round(finish_time - start_time, 1)
    print(f'Данные успешно получены. Время работы: {work_time} секунд')
