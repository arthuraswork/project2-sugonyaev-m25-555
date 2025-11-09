from dataclasses import dataclass
from consts import AlarmResponse, SuccessfullResponse, DB_COMMANDS

@dataclass
class Table:
    name: str
    fields: list[tuple[str,str]]
    fields_value: list[tuple]

    def __repr__(self):
        return f"{self.name}: {self.fields}"
    
    def append(self, values):

        inserting_tuple = list()

        for field in self.fields:
            for value in values:

                if field[0] == value[0] and field[1] == field[1]:

                    inserting_tuple.append(value[2])
            else:
                yield "core error"

        else:
            self.fields_value.append(tuple(inserting_tuple))

    def all(self):
        return.self.fields_value()

@dataclass
class DB:
    def __init__(self):
        self.tables = list()
        self.tables_name = list()

    def create_table(self,table_name: str, fields: list):
        if table_name not in self.tables_name:
            new_table = Table(table_name, fields)
            self.tables.append(new_table)
            self.tables_name.append(table_name)
            return SuccessfullResponse.TABLE_CREATED
        else:
            return AlarmResponse.TABLE_EXISTS

    def insert(self, table_name, fields:list):
        for table in self.tables:
            if table.name == table_name:
                return table.append(fields)
                
        return AlarmResponse.CORE_ERROR

    def select(self, what, table_name):
        if 
    
    def update(self, condition, table_name):
        ...
    
    def remove(self, condition, table_name):
        ...
    
    def load_table(self, path):
        ...
    
    def list_tables(self):
        return self.tables
    
    def show_commands(self):
        print("\n" + "\n".join(DB_COMMANDS) + "\n")