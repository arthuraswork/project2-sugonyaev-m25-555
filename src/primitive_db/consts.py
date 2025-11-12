from enum import Enum


class TokensDML(Enum):
    INSERT = "insert"
    SELECT = "select"
    DELETE = "delete"
    UPDATE = "update"
    LIST   = "list"


class TokensDDL(Enum):
    CREATE = "create"
    TABLE  = "table"
    DROP   = "drop"
    INFO   = "info"

BOOLVALS = ['true', 'false','True','False']

class TokenSymbols(Enum):
    BEGIN_BRACES  = "{"
    END_BRACES    = "}"
    BEGIN_PARENTH = "("
    END_PARENTH   = ")"
    COMMA         = ","
    COLON         = ":"

class TokenDatatype(Enum):
    INT    = "int"
    STRING = "str"
    LOGIC  = "bool"

class TokenServiceWords(Enum):
    HELP = "help"
    EXIT = "exit"
    LIST = "list"


class AlarmResponse(Enum):
    TABLE_EXISTS = "таблица не создана, так как одноименная таблица уже есть"
    PARSE_ERROR  = "ошибка парсинга"  
    CORE_ERROR   = "ошибка в обработке запроса"
    UNKNOWN_ERROR = "неизвестная ошибка"
    
class SuccessfullResponse(Enum):
    TABLE_CREATED = "таблица создана успешно"
    SUCCESSFULL   = "операция выполнена успешно"

DB_COMMANDS = [
    "insert into <имя_таблицы> values {<значение1>, <значение2>, ...} - создать запись",
    "select * from <имя_таблицы> where (<столбец> = <значение>) - прочитать записи по условию",
    "select * from <имя_таблицы> - прочитать все записи",
    "update <имя_таблицы> set {<столбец1> = <новое_значение1>} where (<столбец_условия> = <значение_условия>) - обновить запись",
    "delete from <имя_таблицы> where <столбец> = <значение> - удалить запись",
    "info <имя_таблицы> - вывести информацию о таблице",
    "exit - выход из программы",
    "help - справочная информация",
    "drop table <имя>"
]

COMP_FUNCS = {

    """
    Операции сравнения
    """
    '<': lambda x,y: True if x < y else False,
    '>': lambda x,y: True if x > y else False,
    '>=': lambda x,y: True if x >= y else False,
    '<=': lambda x,y: True if x <= y else False,
    '==': lambda x,y: True if x == y else False,
    '!=': lambda x,y: True if x != y else False,
    '~':  lambda x,y: True if x in y else False 
    }

DATADIR   =  'src/data/'
ALLCOLUMNS = '*'
METAFILE = "src/db_meta.json"