from .consts import AlarmResponse
cached_comands: dict = {}

def handler_caching(func):

    def wrapper(*args,**kwargs):
        
        print(*args,**kwargs)
        func(*args,**kwargs)

    return wrapper

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
