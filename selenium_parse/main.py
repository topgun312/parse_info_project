import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from config_urls import SITE_URL


service = Service(
    executable_path="/home/topgun/PycharmProjects/parse_info/selenium_parse/chromedriver_linux64/chromedriver"
)
driver = webdriver.Chrome(service=service)


def get_page_info(URL):
    cur_time = datetime.now().strftime("%d_%m_%Y_%H_%M")
    driver.get(URL)

    film_title = driver.find_elements(By.CLASS_NAME, "movieItem_title")
    film_rating = driver.find_elements(
        By.CLASS_NAME, "movieItem_itemRating.miniRating.miniRating-good"
    )
    film_position = driver.find_elements(By.CLASS_NAME, "movieItem_position")
    film_genres = driver.find_elements(By.CLASS_NAME, "movieItem_genres")
    film_year_country = driver.find_elements(By.CLASS_NAME, "movieItem_year")
    with open(f"kinoafisha_{cur_time}_top.txt", "a", encoding="utf-8") as file:
        for film_num in range(0, len(film_title)):
            file.write(
                f"{film_position[film_num].text}. Название: {film_title[film_num].text}\n "
                f"Рейтинг: {film_rating[film_num].text}\n Жанр: {film_genres[film_num].text}\n"
                f"Год и страна производства: {film_year_country[film_num].text}\n"
            )


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
            print(f"Страница номер {page} обработана.")
        time.sleep(2)
        break


def main():
    get_page_numb()


if __name__ == "__main__":
    start_time = time.time()
    main()
    finish_time = time.time()
    work_time = round(finish_time - start_time, 1)
    print(f"Данные успешно получены. Время работы: {work_time} секунд")
