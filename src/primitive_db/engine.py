import prompt
from parser import QueryParser
from dataclasses import dataclass
from consts import (
    TokensDDL, AlarmResponse, TokenServiceWords, TokensDML)
from core import DB
from logger import log

@dataclass
class RuntimeDB:
    parser = QueryParser() 
    db     = DB()
    def user_prompt(self):
        try:
            user_input = prompt.string(prompt="primitive@db:~$ ")
            self.resulting(self.parser.parse(user_input))
        except Exception as e:
            print(e)

    def unsafe(self):
        user_input = prompt.string(prompt="primitive@db:~$")
        self.resulting(self.parser.parse(user_input))

    def resulting(self,result: dict):
        match result["type"]:
            case TokensDDL.CREATE:
                returns = self.db.create_table(table_name=result["table_name"], fields=result["fields"])  
                if isinstance(returns, AlarmResponse):
                    log.alarm(returns.value)
                else:
                    log.info(returns.value)  

            case TokenServiceWords.HELP.value:
                log.info(TokenServiceWords.HELP)
            
            case TokenServiceWords.LIST.value:
                for table in self.db.list_tables():
                    print(table)
            
            case AlarmResponse.NO_FIELDS_SELECT:
                print(AlarmResponse.NO_FIELDS_SELECT.value)
            
            case TokensDML.SELECT:
                ...
            
            case TokensDML.INSERT:
                ...
            
            case _:
                ...