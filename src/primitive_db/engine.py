import prompt
from prettytable import PrettyTable
from .parser import QueryParser
from dataclasses import dataclass
from .consts import (
    TokensDDL, AlarmResponse, TokenServiceWords, TokensDML
)
from .core import DB

@dataclass
class RuntimeDB:
    parser = QueryParser() 
    db     = DB()
    
    def update_db(self):
        self.db.update_db_metadata()
    
    def user_prompt(self):
        try:
            user_input = prompt.string(prompt="primitive@db:~$")
            self.resulting(self.parser.parse(user_input))
        except Exception as e:
            print(e)

    def unsafe(self):
        user_input = prompt.string(prompt="primitive@db:~!>")
        self.resulting(self.parser.parse(user_input))
        
    def draw_list_results(table_name, tables):
        table = PrettyTable()
        table.field_names = ['table name','columns', 'datatypes']
        for t in list(tables.keys()):
            table.add_row(
                [t,' '.join(tables[t]), ' '.join([v for v in tables[t].values()])]
                )
        print(table)

    def draw_select_results(table_name, names, data=None):
        table = PrettyTable()
        table.field_names = [f'{k}: {v}' for k,v in list(names.items())]
        if data:
            for row in data:
                table.add_row(list(row.values()))
        print(table)

    
    def resulting(self,result: dict):
        response_type = result.get("type")
        if response_type:
            match response_type:
                case TokensDDL.CREATE:
                    self.db.create_table(table_name=result["table_name"], fields=result["fields"])  

                case TokenServiceWords.HELP:
                    self.db.show_commands()
                    
                case TokensDDL.INFO:
                    self.draw_select_results(names=self.db.table_info(result['table_name']))
                
                case TokenServiceWords.LIST:
                    self.draw_list_results(self.db.list_tables())
                
                case TokensDML.UPDATE:
                    print(result)
                    self.db.update(
                        table_name=result["table_name"],
                        column_name=result['condition']['column_name'],
                        operation=result['condition']['operation'],
                        value=result['condition']['value'],
                        new_value=result['new_value'],
                        updating_column=result['updating_column']
                                   )
                
                case TokensDML.SELECT:
                    selecting_result = self.db.select(
                        table_name=result["table_name"], 
                        what=result["what"],
                        condition=result.get('condition')
                        )
                    if selecting_result:
                        self.draw_select_results(
                            data=selecting_result['data'], names=selecting_result['columns']
                        )
                        
                
                case TokensDML.INSERT:
                    self.db.insert(table_name=result["table_name"], fields=result["fields"])
                    
                case TokensDML.DELETE:
                    self.db.delete(
                        table_name=result["table_name"],
                        column_name=result['condition']['column_name'],
                        operation=result['condition']['operation'],
                        value=result['condition']['value']
                                   )
                                
                case TokensDDL.DROP:
                    self.db.drop_table(table_name=result["table_name"])
                case _:
                    ...