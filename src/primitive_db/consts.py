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
    LOAD   = "load"

class TokenSymbols(Enum):
    BEGIN_BRACES  = "{"
    ENG_BRACES    = "}"
    BEGIN_PARENTH = "("
    ENG_PARENTH   = ")"
    COMMA         = ","

class TokenDatatype(Enum):
    INT    = "int"
    STRING = "string"
    LOGIC  = "logic"
    ID     = "id"

class TokenServiceWords(Enum):
    HELP = "help"
    EXIT = "exit"
    LIST = "listing"


class AlarmResponse(Enum):
    TABLE_EXISTS      = "таблица не создана, так как одноименная таблица уже есть"
    NO_FIELDS         = "в таблице не может не быть полей"
    NO_FIELDS_SELECT  = "в запросе не указаны поля или таблица"

class SuccessfullResponse(Enum):
    TABLE_CREATED = "таблица создана успешно"