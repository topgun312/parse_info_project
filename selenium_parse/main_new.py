import csv
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from config_urls import SITE_URL


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
films_data = []


def get_page_info(URL):
    driver.get(URL)

    try:
        films = driver.find_elements(
            By.CLASS_NAME,
            "movieList_item.movieItem.movieItem-rating.movieItem-position",
        )
        films_items = [film.text.split("\n") for film in films]
        for film in films_items:
            films_data.append(
                {
                    "film_rating": film[0],
                    "film_position": film[1],
                    "film_title": film[2],
                    "film_genres": film[3],
                    "film_year_country": film[4],
                }
            )
    except Exception as ex:
        print(ex)


def get_page_numb():
    driver.get(SITE_URL)

    pages = driver.find_element(
        By.CLASS_NAME,
        "ratings_pagination.bricks.bricks-unite.swipe.outer-mobile.inner-mobile",
    )
    page_num = pages.find_elements(By.TAG_NAME, "a")
    while True:
        for page in range(len(page_num[1:])):
            get_page_info(SITE_URL + f"?page={page}")
            print(f"Страница {page} обработана")
        time.sleep(2)
        break


def main():
    get_page_numb()
    cur_time = datetime.now().strftime("%d_%m_%Y_%H_%M")

    with open(f"kinoafisha_{cur_time}_async.csv", "w") as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                "Позиция" "Название фильма",
                "Рейтинг",
                "Жанр",
                "Год и страна производства",
            )
        )

        for film in films_data:
            with open(f"kinoafisha_{cur_time}_async.csv", "a") as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        film["film_position"],
                        film["film_title"],
                        film["film_position"],
                        film["film_genres"],
                        film["film_year_country"],
                    )
                )


if __name__ == "__main__":
    start_time = time.time()
    main()
    finish_time = time.time()
    work_time = round(finish_time - start_time, 1)
    print(f"Данные успешно получены. Время работы: {work_time} секунд")
