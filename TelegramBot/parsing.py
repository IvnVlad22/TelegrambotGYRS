from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

def get_teachers(type:str):
    """
    Функция получает текущую валюту на веб-странице.
    :return: ключ: значение (преподаватель: ссылка на его рассписание), либо 'error' в случае ошибки
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

        ## Ссылка либо на преподавателей, либо на группу
        if type == 'teach':
            url = 'https://www.asu.ru/timetable/lecturers/16/103'
        else:
            url = 'https://www.asu.ru/timetable/students/16/'

        ## Переходмм по ссылке
        driver.get(url)


        ## Находим список преподавателей (групп)
        elementCords = driver.execute_script(
    """return Array.from(document.querySelectorAll('.list-item-link')).map(link => link.textContent);""")

        ## Находим ссылки для каждого преподавателя (группы)
        links = driver.execute_script(
    """return Array.from(document.querySelectorAll('.list-item-link')).map(link => link.href);""")

        ## Закидываем ФИО преподов и ссылку в "ключ: значение"
        link_dict = dict(zip(elementCords, links))

        ## Завершаем работу драйвера
        driver.quit()
        return link_dict

    except WebDriverException as e:
        print(f"An error occurred: {e}")
        return 'error'





def get_lessons(link: str) -> float:
    """
    Функция получает ссылку
    :return: список обьектов с расписание, либо 'error' в случае ошибки
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

        # Открываем страницу с курсом доллара к батам
        driver.get(link)

        ## Получаем список обьектов
        times = driver.execute_script("""
        var blocks = document.querySelectorAll('.schedule_table-body-rows_group');
var scheduleData = []; // Создаем пустой список для хранения данных

blocks.forEach(function(block) {
    var dateElement = block.querySelector('.schedule_table-date-wd');
    var dateDMElement = block.querySelector('.schedule_table-date-dm');
    var dateWD = dateElement ? dateElement.textContent.trim() : "";
    var dateDM = dateDMElement ? dateDMElement.textContent.trim() : "";
    var date = dateWD + " " + dateDM;

    var scheduleBlocks = block.querySelectorAll('.schedule_table-body-row');

    // Проходимся по каждому блоку
    scheduleBlocks.forEach(function(scheduleBlock) {
        try {
            // Находим элементы с временем, названием занятия и аудиторией
            var timeElement = scheduleBlock.querySelector('.schedule_table-cell[data-type="time"]');
            var subjectElement = scheduleBlock.querySelector('.schedule_table-cell[data-type="subject"]');
            var roomElement = scheduleBlock.querySelector('.schedule_table-cell[data-type="room"] a');

            // Извлекаем текст из элементов с проверкой на существование
            var time = timeElement ? timeElement.textContent.trim() : "";
            var subject = subjectElement ? subjectElement.childNodes[subjectElement.childNodes.length - 1].textContent.trim() : "";
            var room = roomElement ? roomElement.textContent.trim() : "";

            // Добавляем информацию о занятии в список
            scheduleData.push({
                date: date,
                time: time,
                subject: subject,
                room: room
            });
        } catch (error) {
            // Если элементы не найдены, присваиваем пустые строки
            console.error("Ошибка при обработке блока: ", error);
        }
    });
});

// Возвращаем список данных
return(scheduleData);


        """)

        ## Завершаем работу драйвера
        driver.quit()
        return times

    except WebDriverException as e:
        print(f"An error occurred: {e}")
        return 'error'