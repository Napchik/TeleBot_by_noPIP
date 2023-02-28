"""
 Description: This file uses to activate daily functions

 Authors: Mikhail Shikalovskyi

 version 1.0
"""

import Parsing
import db_function
import SQL
import schedule
from datetime import datetime
import time


def schedule_info_uploader():
    try:
        parser = Parsing.Parser()
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


schedule.every().day.at("01:00").do(schedule_info_uploader)

while True:
    schedule.run_pending()
    time.sleep(1)
