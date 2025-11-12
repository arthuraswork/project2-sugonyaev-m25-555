from .consts import AlarmResponse
import time

def handler_confirm(func):
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
    def wrapper(*args, **kwargs):
        result = func(*args,**kwargs)
        print(result.value)
    return wrapper

def hander_timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'длительность операции: {end - start}')
        return result
    return wrapper