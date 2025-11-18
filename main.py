import parser
import logic
import calendar_creator

# Главный модуль

def main():
    
    # Передаем группу и недели для записи в файл. Делается через редактор кода, так как пока необходимости в пользовательском вводе нет
    
    group_to_parse = '15.22д-э01/25б'
    weeks_to_parse = range(12, 19) 
    
    master_schedule_list = [] 
    
    print(f"Начинаю парсинг {group_to_parse} для недель {weeks_to_parse.start}-{weeks_to_parse.stop - 1}...")

    for week in weeks_to_parse:
        
        print(f"--- Получаю HTML для недели {week} ---")
        
        # А теперь парсим каждую неделю поочередно
        
        html_data, session, headers, selection = parser.get_schedule_html(
            group=group_to_parse, 
            week_number=week
        )
        
        if html_data and session:
            
            schedule_for_one_week = logic.extract_schedule(html_data, session, headers, selection)
            master_schedule_list.extend(schedule_for_one_week)
            print(f"Неделя {week} обработана.")
            
        else:
            print(f"Ошибка: Не удалось получить данные для недели {week}. Пропускаю.")

    if master_schedule_list:
        print("\nВсе недели обработаны. Создаю .ics файлы...")
        calendar_creator.create_ics_files(master_schedule_list)
        print("Готово!")
    else:
        print("Не удалось собрать никакие данные. Файлы не созданы.")


if __name__ == "__main__":
    main()
    
    # Готово! Теперь у нас есть икс файлы с расписаниеп всех недель. Синхронизация с гитом сама подгружаем их в репозиторий каждый день в 21:00
    # В гугл календаь вводятся три ссылки на икс файлы из репозитория => синхронизация готова!