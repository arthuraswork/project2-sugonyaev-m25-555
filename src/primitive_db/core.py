from dataclasses import dataclass
from consts import AlarmResponse, SuccessfullResponse, DB_COMMANDS, COMP_FUNCS
from utils import *
    
    
@dataclass
class DB:
    def __init__(self):
        self.tables: dict = dict()
    def create_table(self, table_name, fields: list[tuple[str,str]]):
        if ('id','int') not in fields:
            fields.insert(0,('id','int'))
        field_dict = {field[0]:field[1] for field in fields}
        table_dict = {}
        table_dict['data'] = []
        table_dict['columns'] = field_dict
        self.tables[table_name] = field_dict
        self.save_db_metadata()
        save_table_metadata(table_dict,table_name)
        
    def insert(self, table_name, fields: dict):
        if table_name not in self.tables.keys():
            return AlarmResponse.CORE_ERROR
        table_fields = list(self.tables.get(table_name).keys())
        inserting_data = {}
        for field in fields:
            if field in table_fields:
                inserting_data[field] = fields[field]
            else:
                return AlarmResponse.CORE_ERROR
        self.updata_table(inserting_data,table_name)
    def delete(self, table_name, column_name, operation, value):
        table_data = load_table_data(table_name)
        print(table_data['data'])
        results = []
        for row in table_data['data']:
            if column_name not in row:
                continue
            row_value = row[column_name]
            if operation in COMP_FUNCS:
                if not COMP_FUNCS[operation](row_value, value):
                    print(row_value, value)
                    results.append(row)
        print(results)
        table_data['data'] = results
        self.rewrite_table(table_data, table_name)
    def update(self, table_name):
        ...
    def select_on_condition(self, table_name, column_name, operation, value):
        table_data = load_table_data(table_name)
        results = []
        for row in table_data['data']:
            if column_name not in row:
                continue
            row_value = row[column_name]
            
            if operation in COMP_FUNCS:
                if COMP_FUNCS[operation](row_value, value):
                    results.append(row)
        return results
    
    def select(self,table_name, what, condition):
        if table_name not in self.tables.keys():
            return AlarmResponse.CORE_ERROR
        if condition:
            return self.select_on_condition(table_name, condition['column_name'],condition['operation'],condition['value'])
        else:
            if what == '*':
                return load_table_data(table_name)
            
    def update_db_metadata(self):
        self.tables = load_metadata()
    def updata_table(self,new_data,table_name):
        table_data = load_table_data(table_name)
        new_data['id'] = len(table_data['data'])+1
        table_data['data'].append(new_data)
        save_table_metadata(table_data,table_name)
    def rewrite_table(self,new_data,table_name):
        save_table_metadata(new_data,table_name)
    def save_db_metadata(self):
        save_metadata(self.tables)
    def list_tables(self):
        print(load_metadata())
    def show_commands(self):
        print('\n'.join(DB_COMMANDS))
        
    def drop_table(self,table_name):
        if table_name not in self.tables.keys():
            return AlarmResponse.CORE_ERROR
        del self.tables[table_name]
        save_metadata(self.tables)