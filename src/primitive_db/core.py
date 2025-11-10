from dataclasses import dataclass
from consts import AlarmResponse, SuccessfullResponse, DB_COMMANDS, COMP_FUNCS

@dataclass
class Table:
    """
    Описывает одну таблицу
    name отвечает за имя таблицы
    fields отвечает за содержание таблицы
    """
    name: str
    fields: dict[str, list]
    
    def __repr__(self):
        return f"{self.name}: {self.fields}"
    
    def post(self, values: tuple):
        """добавляет значения в таблицу"""
        copied_table = dict(self.fields)
        for field, datatype, value in values:
            key = '-'.join((field,datatype))
            if key in self.fields:
                copied_table[key].append(value)
            else:
                return AlarmResponse.CORE_ERROR
        self.fields = copied_table
        self.fields['id-int'].append(len(self.fields['id-int'])+1)
    
    def all(self):
        """возвращает все данные таблицы"""
        return self.fields
    
    def with_condition(self, column_name, operation, value):
        resultings = [] 
        vals = list(self.fields.values())
        print(column_name, operation, value)
        if isinstance(value, int):
            dt = 'int'
        elif isinstance(value, str):
            dt = 'string'
        elif isinstance(value, bool):
            dt = 'logic'
        else:
            return AlarmResponse.CORE_ERROR
        typed_column = column_name+'-'+dt
        if self.fields.get(typed_column):
            key = self.fields[typed_column]
            for f,v in enumerate(zip(*vals)):
                if COMP_FUNCS[operation](value,key[f]):
                    resultings.append(v)

        return resultings 
@dataclass
class DB:
    def __init__(self):
        self.tables = dict()

    def create_table(self, table_name: str, fields: list):
        if table_name not in self.tables:
            if ('id','int') not in fields:
                fields.insert(0, ('id','int'))
            fields_dict = {'-'.join(field): [] for field in fields}
 
            new_table = Table(table_name, fields_dict)
            self.tables[table_name] = new_table
            print(self.tables)
            return SuccessfullResponse.TABLE_CREATED
        else:
            return AlarmResponse.TABLE_EXISTS
        
    def insert(self, table_name, fields: tuple):  
        table = self.tables.get(table_name)
        if table:  
            table.post(fields)
            return SuccessfullResponse.SUCCESSFULL
        return AlarmResponse.CORE_ERROR

    def select(self, what, table_name, condition=None):
        if what == '*':
            table = self.tables.get(table_name)
            if table:
                if condition:
                    return table.with_condition(condition['column_name'], condition['operation'],condition['value'])
                return table.all()
            else:
                print(f"Таблица {table_name} не существует")
    
    def update(self, condition, table_name):
        pass
    
    def remove(self, condition, table_name):
        pass
    def commit(self):
        ...
        
    def drop(self,table_name:str):
        table = self.tables.get(table_name)
        if table:  
            del self.tables[table_name]
            return SuccessfullResponse.SUCCESSFULL
        return AlarmResponse.CORE_ERROR
    
    def list_tables(self):
        print(self.tables)    
    def show_commands(self):
        print("\n" + "\n".join(DB_COMMANDS) + "\n")