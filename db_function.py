"""
 Description: This file has some functions which
              are used to execute some data from DataBase.

       DataBase consists of some tables:

           users           -- user_id, user_name,
           info_users      -- user_id, group_name, schedule_switch
           list_groups     -- group_name
           schedule        -- group_name, day1, day2, day3, day4, day5, day6 ,day8, day9, day10, day11, day12, day13
           info_professor  -- group_name, position, name, subject
           info_global     -- week


 Authors: Mikhail Shikalovskyi

 version 1.0
"""
import SQL
from datetime import datetime


def reformat_list(data) -> list:
    """Function to convert executed data to list"""
    result = []
    for i in data:
        result.append(i[0])
    return result


def reformat_str(data) -> str:
    """Function to convert executed data to str"""
    result = ""
    if data[0][0] is None:
        return "None"
    else:
        for i in data:
            result += i[0]
    return result


def today_day() -> int:
    """Function to find out number of week and what day is today"""
    filter = f"SELECT week FROM info_global"
    if SQL.execute(filter) == 1:
        result = datetime.today().isoweekday()
    else:
        result = datetime.today().isoweekday() + 7
    return result


def users_by_group(group) -> list:
    """Function to execute all user_id by group"""
    filter = f"SELECT user_id FROM info_users WHERE group_name = '{group}'"
    result = reformat_list(SQL.execute(filter))
    return result


def all_groups() -> list:
    """Function to execute list of all groups from DataBase"""
    filter = f"SELECT group_name FROM list_groups"
    result = reformat_list(SQL.execute(filter))
    return result


def schedule_day_by_group(group, day) -> str:
    """Function to execute schedule for special day"""
    filter = f"SELECT day{day} FROM schedule WHERE group_name = '{group}'"
    result = reformat_str(SQL.execute(filter))
    return result

