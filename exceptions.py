class TokensError(Exception):
    """Вызывается, когда отсутствуют обязательные переменные окружения."""

    pass


class StatusCodeError(Exception):
    """Вызывается, когда API домашки возвращает код, отличный от 200."""

    pass


class RequestError(Exception):
    """Обрабатываются любые другие сбои при запросе к эндпоинту API домашки."""

    pass


class StatusHWError(KeyError):
    """Вызывается, когда API домашки возвращает недокументированный статус
    домашней работы либо домашку без статуса.
    """

    pass


class KeyHWError(KeyError):
    """Вызывается, когда в ответе API домашки нет ключа `homework_name`."""

    pass
