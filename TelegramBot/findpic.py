from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time


def get_images(value:str):
    """
    Функция получает ссылку и находит похожие картники
    :return: возвращает список ссылок, либо 'error' в случае ошибки
    """
    try:
        # Создаем экземпляр WebDriver с использованием Chrome
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')

        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.2 Safari/605.1.15"

        chrome_options.add_argument(f"user-agent={user_agent}")
        driver = webdriver.Chrome(options=chrome_options)

        ## Переходим по ссылку
        url = 'https://tineye.com'
        driver.get(url)

        time.sleep(1) ## ждем секунду, чтобы страница прогрузилась

        ## JS код, вводим в поиск ссылку
        xd = f'document.getElementsByClassName("image-url")[0].value="{value}";'
        find = driver.execute_script(xd)

        ## Нажимаем кнопку поиска
        links = driver.execute_script(
        """document.getElementsByClassName("submit-button")[0].click();""")

        time.sleep(5) ## ждем когда страница прогрузится

        ## Находим ссылки и закидываем их в список
        urls = driver.execute_script(
            """let matchRows = document.getElementsByClassName('match-row');
                // Инициализируем пустой массив для хранения ссылок
                let hrefList = [];

                // Перебираем каждый элемент match-row
                for (let matchRow of matchRows) {
                    // Ищем все теги <a> внутри текущего matchRow
                    let anchors = matchRow.getElementsByTagName('a');

                    // Перебираем каждый найденный тег <a>
                    for (let anchor of anchors) {
                        // Добавляем href атрибут в список
                        hrefList.push(anchor.href);
                    }
                }

                // Возвращаем список ссылок
                return hrefList;
                """)

        driver.quit() ## выходим из драйвера

        ## Убираем пустые записи и оставляем уникальные
        unique_links = set()
        for url in urls:
            if url:  # Проверяем, что ссылка не пустая
                unique_links.add(url)

        ## Возвращаем
        return unique_links

    except WebDriverException as e:
        print(f"An error occurred: {e}")
        return 'error'
