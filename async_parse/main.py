#Асинхронный парсер с применением библиотек asyncio, aiohttp, beautifulsoup4 для парсинга топ-1000 фильмов по данным сайта www.kinoafisha.ru с сохранением данных в .csv и .json файлах

import asyncio
import csv
import datetime
import json
import time
import aiohttp
import pandas as pd
from bs4 import BeautifulSoup as bs
from config_urls import HEADERS, SITE_URL


films_data = []
start_time = time.time()


async def get_page_info(session, page):
  page_url = SITE_URL + f"?page={page}"
  async with session.get(url=page_url, headers=HEADERS) as response:
    soup = bs(await response.text(), "lxml")
    films_items = soup.find("div", class_="ratings_list movieList movieList-rating grid_cell9").find_all("div", class_="movieList_item movieItem movieItem-rating movieItem-position")
    for film in films_items:
      try:
        film_title = film.find('a', class_="movieItem_title").text.strip()
      except:
        film_title = "Нет названия фильма"

      try:
        film_position = film.find('span', class_="movieItem_position").text.strip()
      except:
        film_position = "Нет рейтинга фильма"

      try:
        film_genres = film.find('span', class_="movieItem_genres").text.strip()
      except:
        film_genres = "Нет жанра"

      try:
        film_year_country = film.find('span', class_="movieItem_year").text.strip()
      except:
        film_year_country = "Нет года и страны производства"


      films_data.append(
        {
          "film_title": film_title,
          "film_position": film_position,
          "film_genres": film_genres,
          "film_year_country": film_year_country
        }
      )

    print(f"[INFO] Сраница {page} загружена")



async def gather_tasks_info():
  async with aiohttp.ClientSession() as session:
    response = await session.get(url=SITE_URL, headers=HEADERS)
    soup = bs(await response.text(), "lxml")
    page_count = int(soup.find('nav', class_='ratings_pagination bricks bricks-unite swipe outer-mobile inner-mobile').find_all('a')[-2].get_text())
    tasks = []
    for page in range(1, page_count + 1):
      task = asyncio.create_task(get_page_info(session, page))
      tasks.append(task)

    await asyncio.gather(*tasks)


def main():
  asyncio.run(gather_tasks_info())
  cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

  with open(f'kinoafisha_{cur_time}_async.json', "w") as file:
    sort_data = sorted(films_data, key=lambda x: int(x['film_position']))
    json.dump(sort_data, file, indent=4, ensure_ascii=False)

  with open(f'kinoafisha_{cur_time}_async.csv', "w") as file:
    writer = csv.writer(file)

    writer.writerow(
      (
        "Название фильма",
        "Рейтинг",
        "Жанр",
        "Год и страна производства",
      )
    )

    for film in films_data:
      with open(f'kinoafisha_{cur_time}_async.csv', "a") as file:
        writer = csv.writer(file)
        writer.writerow(
          (
            film["film_title"],
            film["film_position"],
            film["film_genres"],
            film["film_year_country"]
          )
        )

    df = pd.read_csv(f'kinoafisha_{cur_time}_async.csv')
    sorted_df = df.sort_values(by=df.columns[1])
    sorted_df.to_csv(f'kinoafisha_{cur_time}_async.csv', index=False)

    finish_time = time.time()
    work_time = finish_time - start_time
    print(f"Время работы {round(work_time, 1)}")


if __name__ == "__main__":
  main()