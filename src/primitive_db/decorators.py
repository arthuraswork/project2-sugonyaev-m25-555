import time

from .consts import AlarmResponse


def handler_confirm(func):
    """
    Добавляет условие - согласие при удалении таблицы
    """
    def wrapper(*args, **kwargs):
        print('Подтвердить удаление таблицы (y / n)')
        confirm = input('>>>').lower()
        if confirm == 'y':
            return func(*args,**kwargs)
        else:
            print('Операция отменена')
            return AlarmResponse.UNKNOWN_ERROR
    return wrapper

def hander_log(func):
    """
    печатает результат операции
    """
    def wrapper(*args, **kwargs):
        result = func(*args,**kwargs)
        print(result.value)
    return wrapper

def hander_timer(func):
    """
    замеряет длительность операции
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'длительность операции: {end - start}')
        return result
    return wrapper