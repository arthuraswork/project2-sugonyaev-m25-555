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
        log.info(result)
        match result.get("type"):
            case TokensDDL.CREATE:
                returns = self.db.create_table(table_name=result["table_name"], fields=result["fields"])  
                if isinstance(returns, AlarmResponse):
                    log.alarm(returns.value)
                else:
                    log.info(returns.value)  

            case TokenServiceWords.HELP:
                self.db.show_commands()
            
            case TokenServiceWords.LIST:
                for table in self.db.list_tables():
                    print(table)
            
            case AlarmResponse.PARSE_ERROR:
                log.alarm(AlarmResponse.PARSE_ERROR.value)
            
            case TokensDML.SELECT:
                print(result)
            
            case TokensDML.INSERT:
                print(result)
            
            case _:
                ...