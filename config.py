import pytz

# Настройки расписания
group_to_parse = "15.22д-э01/25б"
weeks_to_parse = range(10, 21)

# Сетевые настройки
base_url = "https://rasp.rea.ru/Schedule/ScheduleCard"
details_url = "https://rasp.rea.ru/Schedule/GetDetails"

timezone = pytz.timezone("Europe/Moscow")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0",
    "Referer": "https://rasp.rea.ru/",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "application/json, text/javascript, */*; q=0.01",
}