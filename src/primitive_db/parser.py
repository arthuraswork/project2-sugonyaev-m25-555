from consts import *
from logger import log
"""insert (name: "value", age: int)"""
"""select table list"""

class QueryParser:
    def parse(self,query):
        if len(query.split()) == 1:
            if query in [word.value for word in TokenServiceWords]:
                return self.__class__.service_word_parse(query)
        return self.preprocessor({"text":query})
    @staticmethod
    def service_word_parse(query):
        match query:
            case "help":
                return {"type":TokenServiceWords.HELP}
            case "exit":
                return {"type":TokenServiceWords.EXIT}

    def preprocessor(self, query: dict):
        processed = query["text"].lower().strip()
        for char in list(TokenSymbols):
            processed = processed.replace(char.value, f' {char.value} ')
        query["text"] = processed
        
        return self.query_typing(query)
    def query_typing(self, query: dict):
        if TokensDML.SELECT.value in query["text"]:
            log.info(TokensDDL.CREATE.value)
            return self.__class__.selecting_parser({
                "text": query["text"],
                "type": TokensDML.SELECT
            })
            
        if TokensDML.INSERT.value in query["text"]:
            log.info(TokensDDL.CREATE)
            return self.__class__.inserting_parser({
                "text": query["text"],
                "type": TokensDML.INSERT
            })

        if TokensDDL.CREATE.value in query["text"]:
            log.info(TokensDDL.CREATE)
            return self.__class__.table_define_parser({
                "text": query["text"],
                "type": TokensDDL.CREATE
            })

    @staticmethod
    def selecting_parser(query: dict) -> dict:
        tokenized = query["text"].split()
        condition_list = []
        condition_flag = False
        table_name = ""
        what = ""

        for i, token in enumerate(tokenized):

            if i > 0 and tokenized[i-1] == "select":
                what = token
                
            if token == ")" and condition_flag:
                condition_flag = False

            if condition_flag and token != "(":
                condition_list.append(token)


            if token == "if" and tokenized[i +1] == "(":
                condition_flag = True
            if tokenized[i-1] == "from":
                table_name = token

        if condition_list:
            query["condition"] = {"column_name":condition_list[0],"operation": condition_list[1], "value": condition_list[2]}

        print(what, table_name)
        if table_name and what:
            query["table_name"] = table_name
            query["what"] = what
            return query
        query["type"] = AlarmResponse.PARSE_ERROR
        return query

    @staticmethod
    def inserting_parser(query: dict) -> dict:
  
        fields_flag = False
        fields_not_parsed = ""
        tokenized = query.get("text").split()

        for char in query.get('text').split():

            if char == "}":
                break

            if fields_flag:
                fields_not_parsed += char

            if char == "{":
                fields_flag = True

        table_flag = False 
        table_name = ""

        for token in tokenized:
            if table_flag:
                table_name = token
                table_flag = False

            if token == "into":
                table_flag = True
                
        fields_tuples = []
        tokenized_fields = fields_not_parsed.split(',')
        
        for token in tokenized_fields:
            field_name, value = token.split(':')
            if "'" in value:
                fields_tuples.append((field_name,"string",value))
            elif value in ["true","false"]:
                fields_tuples.append((field_name,"logic",value))
            elif value.isdigit():
                fields_tuples.append((field_name,"int",value))
            else:
                query["type"] = AlarmResponse.PARSE_ERROR
                return query
        else:
            query['fields'] = fields_tuples
        query['table_name'] = table_name
        return query


    @staticmethod
    def table_define_parser(query: dict):
        
        new_field_type = ""
        fields = list()
        fields_flag = False
        table_name_flag = False
        tokenized = query.get("text").split()
        
        for token in tokenized:

            if table_name_flag:
                query["table_name"] = token
                table_name_flag = False

            if token == TokensDDL.TABLE.value:
                table_name_flag = True

            if token != TokenSymbols.COMMA.value:

                if token == TokenSymbols.BEGIN_BRACES.value:
                    fields_flag = True

                elif token == TokenSymbols.ENG_BRACES.value:
                    fields_flag = False

                if fields_flag:

                    if token in [datatype.value for datatype in TokenDatatype]:
                        if token == TokenDatatype.ID:
                            pass 
                        new_field_type = token

                    else:
                        if new_field_type != "":
                            fields.append((token,new_field_type))
                        new_field_type = ""
        if fields:
            query["fields"] = fields
            return query
        
        query["type"] = AlarmResponse.PARSE_ERROR
        return query
