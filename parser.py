import requests

def get_schedule_html(group, week_number):

    url = "https://rasp.rea.ru/Schedule/ScheduleCard"
    my_params = {
    'selection': group,
    'weekNum': week_number,
    'catfilter': 0
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0',
        'Referer': 'https://rasp.rea.ru/?q=15.22%D0%B4-%D1%8D01%2F25%D0%B1',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/json, text/javascript, */*; q=0.01'
    }

    session = requests.Session()

    try:

        response = session.get(url, params=my_params, headers=headers)
        response.raise_for_status() 
        html_data = response.text
        
        # Код, чтобы сохранить html файл страницы 
        # with open("schedule.html", "w", encoding="utf-8") as f:
        #     f.write(response.text)
        
        return html_data, session, headers, my_params['selection']
    
    except requests.exceptions.RequestException as e: 
            print(f"Ошибка при загрузке: {e}") 
            return None, None, None, None 
