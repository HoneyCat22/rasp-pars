import requests

# Этот модуль отвечает за сбор инфы с сайт вуза

def get_schedule_html(group, week_number):
    
    # Задаем урл и параметры
    
    url = "https://rasp.rea.ru/Schedule/ScheduleCard"                                                           
    my_params = {
    'selection': group,
    'weekNum': week_number,
    'catfilter': 0
    }

    # Задаем заголовки (без них защита сайта нас не пропустит). Заголовки взял с F12 -> Network -> XMR
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0',
        'Referer': 'https://rasp.rea.ru/?q=15.22%D0%B4-%D1%8D01%2F25%D0%B1',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/json, text/javascript, */*; q=0.01'
    }

    # сохраняем куки
    session = requests.Session()

    # Пробуем парсить, если выходит - возвращаем хтмл, куки, заголовки, учебную группу. Не выходит - выдаем ошибку.
    
    try:

        response = session.get(url, params=my_params, headers=headers) 
        response.raise_for_status() 
        html_data = response.text
        
        return html_data, session, headers, my_params['selection']
    
    except requests.exceptions.RequestException as e: 
            print(f"Ошибка при загрузке: {e}") 
            return None, None, None, None 
