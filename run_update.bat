@echo off
chcp 65001 > nul

echo === Активация... ===
call venv\Scripts\activate.bat

echo === Запуск парсера... ===
python main.py

echo === Добавление файлов в Git ===
rem --- Добавляем ВСЕ ---
git add .

echo === Создание коммита... ===
git commit -m "Ручное обновление расписания"

echo === Синхронизация... ===
git pull origin main

echo === Отправка файлов на GitHub ===
git push origin main

echo === Готово! ===
pause