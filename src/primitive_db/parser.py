from consts import *



class QueryParser:
    """
    Класс, отвечающий за парсинг страниц
    на вход текстовой запрос
    на выход словарь с запросом, типом запроса и дополнительными данными 
    в зависимости от типа на исполнение
    """
    def parse(self,query):
        """
        Входная команда, разделяет запросы на два типа -
        сервисные - не работают с таблицами напрямую или не имеют аргументов
        &
        управляющие - работают с бд и таблицами и имеют аргументы
        """
        if len(query.split()) == 1:
            if query in [word.value for word in TokenServiceWords]:
                return self.__class__.service_word_parse(query)
        return self.preprocessor({"text":query})
    @staticmethod
    def service_word_parse(query):
        """
        мэтчинг сервисных комманд
        """
        match query:
            case "help":
                return {"type":TokenServiceWords.HELP}
            case "exit":
                return {"type":TokenServiceWords.EXIT}
            case "list":
                return {"type":TokenServiceWords.LIST}
        return {'type': AlarmResponse.UNKNOWN_ERROR}

    def preprocessor(self, query: dict):
        """
        подготаваливает текст запроса для более удобного парсинга
        """
        processed = query["text"].strip()
        for char in list(TokenSymbols):
            processed = processed.replace(char.value, f' {char.value} ')
        query["text"] = processed
        
        return self.query_typing(query)
    def query_typing(self, query: dict):
        """
        типизирует команды
        """
        if TokensDML.SELECT.value in query["text"]:
            return self.__class__.selecting_parser({
                "text": query["text"],
                "type": TokensDML.SELECT
            })
        if TokensDML.DELETE.value in query["text"]:
            return self.__class__.deleting_parser({
                "text": query["text"],
                "type": TokensDML.DELETE
            })
            
        if TokensDML.INSERT.value in query["text"]:
            return self.__class__.inserting_parser({
                "text": query["text"],
                "type": TokensDML.INSERT
            })

        if TokensDDL.CREATE.value in query["text"]:
            return self.__class__.table_define_parser({
                "text": query["text"],
                "type": TokensDDL.CREATE
            })
        if TokensDML.UPDATE.value in query["text"]:
            return self.__class__.updating_parser({
                "text": query["text"],
                "type": TokensDML.UPDATE
            })            
            
        if TokensDDL.DROP.value in query["text"]:
            return self.__class__.droping_parser({
                "text": query["text"],
                "type": TokensDDL.DROP
            })
        if TokensDDL.INFO.value in query["text"]:
            return self.__class__.table_info({
                "text": query["text"],
                "type": TokensDDL.INFO
            })        
        return {"type":AlarmResponse.UNKNOWN_ERROR}

    @staticmethod
    def table_info(query:dict) -> dict:
        tokenized = query['text'].split()
        for i, token in enumerate(tokenized):
            if token == "info" and len(token) > i:
                table_name = tokenized[i+1]
                query['table_name'] = table_name
                break
        else:
            query['type'] = AlarmResponse.PARSE_ERROR
        return query
                

    @staticmethod
    def droping_parser(query:dict) -> dict:
        """
        обрабатывает дроп тэйбл запрос
        """
        tokenized = query["text"].split()
        table_name = ""
        
        for i, token in enumerate(tokenized):
            if token == "table" and len(token) > i:
                table_name = tokenized[i+1]
                break
            
        if table_name:
            query["table_name"] = table_name
        else:
            query["type"] = AlarmResponse.PARSE_ERROR
        return query
    
    @staticmethod
    def deleting_parser(query: dict) -> dict:
        tokenized = query['text'].split()
        table_name = ''
        condition = []
        flag = False
        for token in tokenized:
            if token == ')':
                flag = False
            if flag and len(condition) == 2:
                if token.isdigit():
                    condition.append(int(token))
                elif token in ['true','false']:
                    condition.append(True if token == 'true' else False)
                else:
                    condition.append(token[1:-1])

            if flag:
                condition.append(token)
            if token == '(':
                flag = True

        for i, token in enumerate(tokenized):
            if token == 'from' and len(tokenized) > i+1:
                table_name = tokenized[i+1]
                break
        try:
            query['condition'] = {'column_name': condition[0],'operation': condition[1], 'value':condition[2]}
            query['table_name'] = table_name 
        except:
            query['type'] = AlarmResponse.PARSE_ERROR
        return query
    
    @staticmethod
    def updating_parser(query: dict) -> dict:
        tokenized = query['text'].split()
        table_name = ''
        condition = []
        new_value = None
        updating_column = ''
        flag_equal = False
        flag = False
        for token in tokenized:
            if token == ')':
                flag = False
            if flag and len(condition) == 2:
                if token.isdigit():
                    condition.append(int(token))
                elif token in ['true','false']:
                    condition.append(True if token == 'true' else False)
                else:
                    condition.append(token[1:-1])

            if flag:
                condition.append(token)
            if token == '(':
                flag = True

        for i, token in enumerate(tokenized):
            if token == 'update' and len(tokenized) > i+1:
                table_name = tokenized[i+1]
                break
        for token in tokenized:
            if token == '}':
                flag = False
            if flag and token != '=' and not flag_equal:
                updating_column = token

            if flag and flag_equal:
                if token.isdigit():
                    new_value = int(token)
                elif token in ['true','false']:
                    new_value = True if token == 'true' else False
                else:
                    new_value = token[1:-1]

            if token == '=':
                flag_equal = True

            if token == '{':
                flag = True
        try:
            query['updating_column'] = updating_column
            query['new_value'] = new_value
            query['condition'] = {'column_name': condition[0],'operation': condition[1], 'value':condition[2]}
            query['table_name'] = table_name 
        except:
            query['type'] = AlarmResponse.PARSE_ERROR
        return query
    
    @staticmethod
    def selecting_parser(query: dict) -> dict:
        """
        обрабатывает запрос типа селект
        """
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

            if token == "(":
                condition_flag = True
            if tokenized[i-1] == "from":
                table_name = token

        if condition_list:
            query["condition"] = {"column_name":condition_list[0],"operation": condition_list[1], "value": condition_list[2]}
            value = query["condition"]['value']
            if "'" in value:
                query["condition"]['value'] = value[1:-1]
            elif value in ["true","false"]:
                if value == 'true':
                    query["condition"]['value'] = True
                else:
                    query["condition"]['value'] = False
            elif value.isdigit():
                query["condition"]['value'] = int(value)
            else:
                query["type"] = AlarmResponse.PARSE_ERROR
                return query
        if table_name and what:
            query["table_name"] = table_name
            query["what"] = what
        else: 
            query["type"] = AlarmResponse.PARSE_ERROR
        return query

    @staticmethod
    def inserting_parser(query: dict) -> dict:
        text = query.get("text")
        tokenized = text.split()

        table_name = ""
        fields_text = ""
    
        for i, token in enumerate(tokenized):
            if token == "into" and i + 1 < len(tokenized):
                table_name = tokenized[i + 1]
                break
        
        start = text.find('{')
        end = text.find('}')
        if start != -1 and end != -1:
            fields_text = text[start + 1:end].strip()
        
        fields_dict = {}
        for field_pair in fields_text.split(','):
            if ':' not in field_pair:
                query["type"] = AlarmResponse.PARSE_ERROR
                return query
                
            field_name, value = field_pair.split(':', 1)
            field_name = field_name.strip()
            value = value.strip()
            
            if value.startswith("'") and value.endswith("'"):
                fields_dict[field_name] = value[1:-1]
            elif value in ["true", "false"]:
                fields_dict[field_name] = value == "true"
            elif value.isdigit():
                fields_dict[field_name] = int(value)
            else:
                query["type"] = AlarmResponse.PARSE_ERROR
                return query

        query['table_name'] = table_name
        query['fields'] = fields_dict
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
