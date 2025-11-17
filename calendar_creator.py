from ics import Calendar, Event
from datetime import datetime
import re
import pytz

MOSCOW_TZ = pytz.timezone("Europe/Moscow")

def create_ics_files(full_schedule):

    print("Создаю .ics файлы...")
    
    c_lectures = Calendar()
    c_practice = Calendar()
    c_exams = Calendar()
    
    for day in full_schedule:
        
        date_match = re.search(r'(\d{2}\.\d{2}\.\d{4})', day['day'])
        if not date_match:
            continue 
        
        date_str = date_match.group(1) # "01.09.2025"
        
        for lesson in day['lessons']:
            
            if not lesson['start_time'] or not lesson['end_time']:
                continue
                
            try:
                start_dt_naive = datetime.strptime(
                    f"{date_str} {lesson['start_time']}", 
                    "%d.%m.%Y %H:%M"
                )
                end_dt_naive = datetime.strptime(
                    f"{date_str} {lesson['end_time']}", 
                    "%d.%m.%Y %H:%M"
                )

                start_dt_aware = MOSCOW_TZ.localize(start_dt_naive)
                end_dt_aware = MOSCOW_TZ.localize(end_dt_naive)

            except ValueError as e:
                print(f"Ошибка конвертации времени: {e}. Пропускаю пару.")
                continue
            
            e = Event()
            e.name = f"{lesson['title']}"
            e.begin = start_dt_aware
            e.end = end_dt_aware
            e.location = lesson['location']
            e.description = f"Тип: {lesson['type']}\nАудитория: {lesson['location']}"
            
            if 'Лекция' in lesson['type']:
                c_lectures.events.add(e)
            elif 'Практическое занятие' in lesson['type']:
                c_practice.events.add(e)
            else:
                c_exams.events.add(e)                

    try:
        with open('lectures.ics', 'w', encoding='utf-8') as f:
            f.write(c_lectures.serialize())
        print("Успех! Файл 'lectures.ics' создан.")
        
        with open('practice.ics', 'w', encoding='utf-8') as f:
            f.write(c_practice.serialize())
        print("Успех! Файл 'practice.ics' создан.")
        
        with open('exams.ics', 'w', encoding='utf-8') as f:
            f.write(c_exams.serialize())
        print("Успех! Файл 'exams.ics' создан.")    
        
    except Exception as e:
        print(f"Ошибка при сохранении файлов: {e}")