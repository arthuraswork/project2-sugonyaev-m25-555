from dataclasses import dataclass
from consts import AlarmResponse, SuccessfullResponse, DB_COMMANDS

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
        for field, datatype, value in values:
            key = '-'.join((field,datatype))
            if key in self.fields:
                self.fields[key].append(value)
        self.fields['id-#'].append(len(self.fields['id-#'])+1)
    
    def all(self):
        """возвращает все данные таблицы"""
        return self.fields

@dataclass
class DB:
    def __init__(self):
        self.tables = dict()

    def create_table(self, table_name: str, fields: list):
        if table_name not in self.tables:
            fields_dict = {'-'.join(field): [] for field in fields}
            if ('id','#') not in fields:
                fields_dict['-'.join(('id','#'))] = list()
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

    def select(self, what, table_name):
        if what == '*':
            table = self.tables.get(table_name)
            if table:
                print(table.all())
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