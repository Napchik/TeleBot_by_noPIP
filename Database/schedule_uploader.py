"""
    Description: This file makes upload parsing data to Database

    Author: Mikhail Shikalovskyi
    Version: 1.3
"""
import parsing
from Database import db_function
from Database.db_function import add_log


def schedule_info_uploader():
    """ Function which triggers functions to collect and upload schedule data to database """
    try:
        parser = parsing.Parser()
        list_group = db_function.all_groups()
        for groups in list_group:
            data = parser.parse(group=groups)
            for week in data:
                db_function.inserter_schedule(week, groups, data)
                db_function.inserter_professor(week, groups, data)
        add_log("Parsing done Successfully")
    except:
        add_log("Parsing FAILED")
