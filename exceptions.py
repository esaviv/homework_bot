class StatusCodeError(Exception):
    """Вызывается, когда API домашки возвращает код, отличный от 200."""

    pass


class RequestError(Exception):
    """Обрабатываются любые другие сбои при запросе к эндпоинту API домашки."""

    pass
