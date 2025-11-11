from dataclasses import dataclass
from .consts import AlarmResponse, DB_COMMANDS, COMP_FUNCS, ALLCOLUMNS
from .utils import *
    
    
@dataclass
class DB:
    """
    Главный класс - отвечает за операции с файлами
    Все операции ниже работают по принципу - 
        загрузи, прочитай, [переделай], [запиши]
    """
    def __init__(self):
        self.tables: dict = dict()
    def create_table(self, table_name, fields: list[tuple[str,str]]):
        """
        Создание базы данных - сохраняет метаданные и данные таблицы в разные файлы
        """
        if ('id','int') not in fields:
            fields.insert(0,('id','int'))
        field_dict = {field[0]:field[1] for field in fields}
        table_dict = {}
        table_dict['data'] = []
        table_dict['columns'] = field_dict
        self.tables[table_name] = field_dict
        self.save_db_metadata()
        save_table_metadata(table_dict,table_name)
        
    def table_info(self,table_name):
        """
        Возвращает информацию о таблице
        """
        if table_name not in self.tables.keys():
            return AlarmResponse.CORE_ERROR
        return self.tables[table_name]
        
    def insert(self, table_name, fields: dict):
        """
        Вставка записи в таблицу
        """
        if table_name not in self.tables.keys():
            return AlarmResponse.CORE_ERROR
        table_fields = list(self.tables.get(table_name).keys())
        inserting_data = {}
        for field in fields:
            if field in table_fields:
                inserting_data[field] = fields[field]
            else:
                return AlarmResponse.CORE_ERROR
        self.update_table(inserting_data,table_name)
    def delete(self, table_name, column_name, operation, value):
        """
        Удаление записей из таблицы по условию
        """
        table_data = load_table_data(table_name)
        results = []
        for row in table_data['data']:
            if column_name not in row:
                continue
            row_value = row[column_name]
            if operation in COMP_FUNCS:
                if not COMP_FUNCS[operation](row_value, value):
                    results.append(row)
        table_data['data'] = results
        self.rewrite_table(table_data, table_name)
        
    def update(self, table_name, updating_column, new_value, column_name, operation, value):
        """
        Обновление данных в записях по условию
        """
        table_data = load_table_data(table_name)
        results = []
        for row in table_data['data']:
            if column_name not in row:
                continue
            cond_value = row[column_name]
            if operation in COMP_FUNCS:
                if COMP_FUNCS[operation](cond_value, value):
                    row[updating_column] = new_value
            results.append(row)
        table_data['data'] = results
        self.rewrite_table(table_data, table_name)
        
    def select_on_condition(self, table_name, column_name, operation, value):
        """
        Выбор записей из таблицы по условию
        """
        table_data = load_table_data(table_name)
        results = []
        for row in table_data['data']:
            if column_name not in row:
                continue
            row_value = row[column_name]
            
            if operation in COMP_FUNCS:
                if COMP_FUNCS[operation](row_value, value):
                    results.append(row)
        table_data['data'] = results
        return table_data
    def select(self,table_name, what, condition):
        """
        Выбор всех записей из таблицы если нет условия
        или отправка в функцию выборки с условием
        """
        if table_name not in self.tables.keys():
            return AlarmResponse.CORE_ERROR
        if condition:
            return self.select_on_condition(table_name, condition['column_name'],condition['operation'],condition['value'])
        else:
            if what == ALLCOLUMNS:
                return load_table_data(table_name)
            
    def update_db_metadata(self):
        """
        При загрузке добавляет метаинформацию о таблицах
        """
        self.tables = load_metadata()
    def update_table(self,new_data,table_name):
        """
        Обновляет данные таблицы
        """
        table_data = load_table_data(table_name)
        new_data['id'] = len(table_data['data'])+1
        table_data['data'].append(new_data)
        save_table_metadata(table_data,table_name)
    def rewrite_table(self,new_data,table_name):
        """
        Перезаписывает результат в файл таблицы
        """
        save_table_metadata(new_data,table_name)
    def save_db_metadata(self):
        """
        Перезаписывает метаинформацию о таблицах в файл
        """
        save_metadata(self.tables)
        
    def list_tables(self):
        """
        Выводит информацию о таблицах
        """
        return load_metadata()
    def show_commands(self):
        """
        Выводит список комманд
        """
        print('\n'.join(DB_COMMANDS))
        
    def drop_table(self,table_name):
        """
        Удаление таблицы из метафайла и кэша
        """
        if table_name not in self.tables.keys():
            return AlarmResponse.CORE_ERROR
        del self.tables[table_name]
        save_metadata(self.tables)
    