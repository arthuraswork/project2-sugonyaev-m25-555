from dataclasses import dataclass
from consts import AlarmResponse, SuccessfullResponse

@dataclass
class Table:
    name: str
    fields: list[tuple[str,str],list]

    def __repr__(self):
        return f"{self.name}: {self.fields}"
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

    def insert(self, table_name, fields:dict):
        ...
    
    def select(self, what, table_name):
        ...
    
    def update(self, condition, table_name):
        ...
    
    def remove(self, condition, table_name):
        ...
    
    def load_table(self, path):
        ...
    def list_tables(self):
        return self.tables