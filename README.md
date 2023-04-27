# Бот-ассистент
### Описание
Telegram-бота, оповещающий о статусе домашнего задания.
### Технологии
Python 3.9, python-dotenv 0.19.0, python-telegram-bot 13.7
### Автор
esaviv
### Запуск проекта в dev-режиме
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/esaviv/homework_bot.git
```
```
cd homework_bot
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv venv | python -m venv venv
```
```
source env/bin/activate | source venv/Scripts/activate
```
```
python3 -m pip install --upgrade pip | python -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Создать файл .env и заполните по образцу .env.example.

В папке с файлом homework.py выполнить команду:
```
python homework.py | python3 homework.py
```
