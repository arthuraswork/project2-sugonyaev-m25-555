from consts import *
from logger import log
"""insert (name: "value", age: int)"""
"""select table list"""

class QueryParser:

    def parse(self, query):
        if len(query.split()) == 1:
            if query in [word.value for word in TokenServiceWords]:
                return {"type":query}

        return self.preprocessor({"text":query})
    
    def preprocessor(self, query: dict):
        processed = query["text"].lower().strip()
        for char in list(TokenSymbols):
            processed = processed.replace(char.value, f' {char.value} ')
        query["text"] = processed
        
        return self.query_typing(query)

    def query_typing(self, query: dict):
        if TokensDML.SELECT.value in query["text"]:
            log.info(TokensDDL.CREATE.value)
            return self.selecting_query_describing({
                "text": query["text"],
                "type": TokensDML.SELECT
            })
            
        if TokensDML.INSERT.value in query["text"]:
            log.info(TokensDDL.CREATE.value)
            return self.new_table_define({
                "text": query["text"],
                "type": TokensDML.INSERT
            })

        if TokensDDL.CREATE.value in query["text"]:
            log.info(TokensDDL.CREATE.value)
            return self.new_table_define({
                "text": query["text"],
                "type": TokensDDL.CREATE
            })


    def selecting_query_describing(self, query: dict):
        print(1)
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
            if token == "from" and i > len(tokenized)-1:
                table_name = tokenized[i+1]

        if condition_list:
            query["condition"] = {"column_name":condition_list[0],"operation": condition_list[1], "value": condition_list[2]}


        if table_name and what:
            query["table_name"] = table_name
            query["what"] = what
            return query
        return AlarmResponse.NO_FIELDS_SELECT


    def inserting_query_describing(self, query: dict):
        ...


    def new_table_define(self, query: dict):
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
        return AlarmResponse.NO_FIELDS
