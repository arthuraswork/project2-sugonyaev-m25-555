import prompt
from prettytable import PrettyTable
from parser import QueryParser
from dataclasses import dataclass
from consts import (
    TokensDDL, AlarmResponse, TokenServiceWords, TokensDML
)
from core import DB

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

    def draw_select_results(table_name, data, names):
        table = PrettyTable()

    
    def resulting(self,result: dict):
        response_type = result.get("type")
        print(result['type'])
        if response_type:
            match response_type:
                case TokensDDL.CREATE:
                    self.db.create_table(table_name=result["table_name"], fields=result["fields"])  

                case TokenServiceWords.HELP:
                    self.db.show_commands()
                
                case TokenServiceWords.LIST:
                    self.db.list_tables()
                
                case TokensDML.SELECT:
                    print(self.db.select(table_name=result["table_name"], what=result["what"], condition=result.get('condition')))
                
                case TokensDML.INSERT:
                    self.db.insert(table_name=result["table_name"], fields=result["fields"])
                case TokensDDL.DROP:
                    self.db.drop(table_name=result["table_name"])
                case _:
                    ...