"""
    Description: This file makes upload parsing data to Database

    Author: Mikhail Shikalovskyi
    Version: 1.1
"""
import parsing
from Database import db_function, SQL
from datetime import datetime


def schedule_info_uploader():
    try:
        parser = parsing.Parser()
        list_group = db_function.all_groups()
        for groups in list_group:
            data = parser.parse(group=groups)
            for week in data:
                db_function.inserter_schedule(week, groups, data)
                db_function.inserter_professor(week, groups, data)
        filter = f"INSERT INTO log (parsing_time, status) VALUES ('{datetime.now()}', 'OK')"
        print(f"Parsing done \033[32mSuccessfully \033[36m{datetime.now()}")
    except:
        filter = f"INSERT INTO log (parsing_time, status) VALUES ('{datetime.now()}', 'FAIL')"
        print(f"Parsing \033[31mFAILED")
    SQL.table_operate(filter)
