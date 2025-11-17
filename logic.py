from bs4 import BeautifulSoup
import requests
import re

def extract_schedule(html_text, session, headers, selection_value):
    soup = BeautifulSoup(html_text, 'html.parser')
    
    day_tables = soup.find_all('table', class_='table-light')
    
    full_schedule = []
    
    for day_table in day_tables:
        
        day_title_tag = day_table.find('h5')
        
        if not day_title_tag:
            continue # Пропускаем, если у таблицы нет шапки
            
        day_title = day_title_tag.text.strip()

        date_match = re.search(r'(\d{2}\.\d{2}\.\d{4})', day_title)
        if not date_match:
            continue # Если не нашли дату, пропускаем день
        
        date = date_match.group(1) # "01.09.2025"
        
        day_schedule = {
            'day': day_title,
            'lessons': []
        }
        
        slots = day_table.find_all('tr', class_='slot')
        
        for slot in slots:
            if 'load-empty' in slot.get('class', []):
                continue 
            
            if slot.find('h5', text='Занятия отсутствуют'):
                continue 

            time_cell = slot.find('td')
            if not time_cell:
                continue

            time_raw_text = time_cell.get_text(separator='\n').strip()
            time_parts = time_raw_text.split('\n')
            
            pair_num = time_parts[0] if len(time_parts) > 0 else "н/д"
            start_time = time_parts[1] if len(time_parts) > 1 else ""
            end_time = time_parts[2] if len(time_parts) > 2 else ""
            
            info_cell = slot.find('a', class_='task')
            if not info_cell:
                continue 

            lesson_title = info_cell.contents[0].strip()
            
            lesson_type_tag = info_cell.find('i')
            lesson_type = lesson_type_tag.text.strip() if lesson_type_tag else "н/д"
            
            location = ""
            subgroup_tag = info_cell.find('strong') 

            if subgroup_tag and "+ подгруппы" in subgroup_tag.text:
                
                try:
                    time_slot = pair_num.split(' ')[0] # "1 пара" -> "1"

                    sub_params = {
                        'selection': selection_value, # '15.22д-э01/25б'
                        'date': date,                 # '01.09.2025'
                        'timeSlot': time_slot         # '1'
                    }
                    
                    sub_response = session.get(
                        "https://rasp.rea.ru/Schedule/GetDetails",
                        params=sub_params,
                        headers=headers
                    )
                    sub_response.raise_for_status()
                    
                    sub_soup = BeautifulSoup(sub_response.text, 'html.parser')

                    subgroup_blocks = sub_soup.find_all('div', class_='element-info-body')
                    
                    locations_list = []
                    
                    for block in subgroup_blocks:
                        
                        subgroup_name = block.get('data-subgroup', 'н/д')
                        
                        block_text = block.get_text()
                        
                        match = re.search(
                            r'Аудитория:\s*(.*?)\s*Площадка:', 
                            block_text, 
                            re.DOTALL | re.IGNORECASE
                        )
                        
                        if match:
                            location_dirty = match.group(1).strip() # " 9 корпус - \n 3.13 "
                            location_clean = ' '.join(location_dirty.split()) # "9 корпус - 3.13"
                            locations_list.append(f"{subgroup_name}: {location_clean}")
                        else:
                            locations_list.append(f"{subgroup_name}: ауд. не найдена")

                    if locations_list:
                        location = ' / '.join(locations_list)
                    else:
                        location = "Подгруппы (не удалось найти)"
            
                except Exception as e:
                    print(f"Ошибка при загрузке подгруппы: {e}")
                    location = "Ошибка загрузки подгруппы"
            
            else:

                all_info_text = info_cell.text.strip()
                location = all_info_text.replace(lesson_title, '').replace(lesson_type, '').strip()
                location = ' '.join(location.split())
                if not location:
                    location = "н/д"


            day_schedule['lessons'].append({
                'pair_num': pair_num,
                'start_time': start_time,
                'end_time': end_time,
                'title': lesson_title,
                'type': lesson_type,
                'location': location.replace(', пл. Основная', '')
            })
            
        full_schedule.append(day_schedule)

    return full_schedule