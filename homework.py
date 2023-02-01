import logging
import os
import time

import requests
import telegram
from dotenv import load_dotenv

from exceptions import (KeyHWError, RequestError, StatusCodeError,
                        StatusHWError, TokensError)

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logging.basicConfig(
    level=logging.DEBUG,
    filename='main.log',
    filemode='a',
    format='%(asctime)s %(levelname)s %(message)s'
)


def check_tokens():
    """Проверяет доступность переменных окружения."""
    if all((PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)):
        return True
    return False


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.debug(f'Бот отправил сообщение "{message}"')
    except Exception as error:
        logging.error(f'Бот на смог отправить сообщение "{message}". {error}')


def get_api_answer(timestamp):
    """Делает запрос к эндпоинту API-сервиса Практикум.Домашка."""
    try:
        response = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params={'from_date': timestamp}
        )
    except requests.RequestException as error:
        raise RequestError(error)

    if response.status_code != 200:
        raise StatusCodeError(
            f'Эндпоинт {response.url} недоступен.'
            'Код ответа API: {response.status_code}.'
        )

    return response.json()


def check_response(response):
    """Проверяет ответ API на соответствие документации."""
    if not isinstance(response, dict):
        raise TypeError(
            'В ответе API структура данных не соответствует ожиданиям:'
            'например, получен список вместо ожидаемого словаря.'
        )

    homework = response.get('homeworks', None)
    if not homework:
        raise KeyHWError('В ответе API домашки нет ключа `homeworks`.')
    if not isinstance(homework, list):
        raise TypeError(
            'В ответе API домашки под ключом `homeworks`'
            'данные приходят не в виде списка.'
        )
    return True


def parse_status(homework):
    """Извлекает статус последней домашней работы."""
    homework_name = homework.get('homework_name', None)
    if not homework_name:
        raise KeyHWError('В ответе API домашки нет ключа `homework_name`')

    verdict = HOMEWORK_VERDICTS.get(homework.get('status'), None)
    if not verdict:
        raise StatusHWError(
            'API домашки возвращает недокументированный'
            'статус домашней работы либо домашку без статуса'
        )

    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    try:
        if check_tokens():
            bot = telegram.Bot(token=TELEGRAM_TOKEN)
            timestamp = int(time.time())
        else:
            raise TokensError('Отсутствует обязательная переменная окружения.')
    except TokensError as error:
        logging.critical(f'{error} Программа принудительно остановлена.')
        exit()

    hw_previous_status = ''
    while True:
        try:
            timestamp = int(time.time())
            response = get_api_answer(timestamp)

            if check_response(response):
                last_homework = response.get('homeworks')[0]

                homework_status = parse_status(last_homework)

                if hw_previous_status != homework_status:
                    send_message(bot, homework_status)

                hw_previous_status = homework_status

        except Exception as error:
            logging.error(f'Сбой в работе программы: {error}')
            send_message(bot, str(error))

        time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
