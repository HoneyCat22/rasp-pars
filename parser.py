import requests
import config

# Этот модуль отвечает за сбор инфы с сайт вуза

def get_schedule_html(group, week_number):
    
    # Задаем урл и параметры
    
    url = config.base_url                                                        
    my_params = {
    'selection': group,
    'weekNum': week_number,
    'catfilter': 0
    }

    # Задаем заголовки (без них защита сайта нас не пропустит). Заголовки взял с F12 -> Network -> XMR

    # сохраняем куки
    session = requests.Session()

    # Пробуем парсить, если выходит - возвращаем хтмл, куки, заголовки, учебную группу. Не выходит - выдаем ошибку.
    
    try:

        response = session.get(url, params=my_params, headers=config.headers) 
        response.raise_for_status() 
        html_data = response.text
        
        return html_data, session, config.headers, my_params['selection']
    
    except requests.exceptions.RequestException as e: 
            print(f"Ошибка при загрузке: {e}") 
            return None, None, None, None 
