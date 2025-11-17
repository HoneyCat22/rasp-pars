import parser
import logic
import calendar_creator

def main():
    print("Получаю HTML...")
    
    html_data, session, headers, selection = parser.get_schedule_html()
    
    if html_data and session:
        
        schedule = logic.extract_schedule(html_data, session, headers, selection)
        
        calendar_creator.create_ics_files(schedule)
        
        # print("--- Готовое расписание ---")
        
        # for day in schedule:
        #     print(f"\n=== {day['day']} ===")
            
        #     if len(day['lessons']) > 0: 
        #         for lesson in day['lessons']:
        #             # ... твой код вывода (он в порядке) ...
        #             print(f"{lesson['pair_num']} ({lesson['start_time']}-{lesson['end_time']})")
        #             print(f"  Предмет: {lesson['title']}")
        #             print(f"  Тип:     {lesson['type']}")
        #             print(f"  Место:   {lesson['location']}\n")
        #     else:
        #         print('Занятий нет')
        # print()

if __name__ == "__main__":
    main()