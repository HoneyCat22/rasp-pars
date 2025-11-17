@echo off
chcp 65001 > nul

echo === Активация виртуального окружения ===
call venv\Scripts\activate.bat

echo === Запуск парсера и создание .ics файлов ===
python main.py

echo === Добавление .ics файлов в Git ===
git add lectures.ics practice.ics exams.ics

echo === Создание коммита (сохранения) ===
git commit -m "Автоматическое обновление расписания"

echo === Синхронизация ===
git pull origin main

echo === Отправка файлов на GitHub ===
git push origin main

echo === Готово! ===
pause