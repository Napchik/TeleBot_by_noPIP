"""
 Description: This file has some functions which
              are used to execute/insert some data from/to DataBase.

       DataBase consists of some tables:
           log             -- id, parsing_time, status
           info_global     -- week
           info_professor  -- group_name, subject, name, link
           info_users      -- user_id, group_name, schedule_switch
           list_groups     -- group_name
           schedule        -- group_name, day1, day2, day3, day4, day5, day6 ,day8, day9, day10, day11, day12, day13
           users           -- user_id, user_name,

 Authors: Mikhail Shikalovskyi

 version 1.2
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


def inserter_schedule(week, group, data):
    """Function inserts or updates schedule for a group"""
    if week == "week1":
        counter = 1
    else:
        counter = 8
    for days in data[f"{week}"]:
        result = ""
        for lessons in days:
            if lessons is not None:
                result += f"{lessons[0]} {lessons[2]}; "
            else:
                result += "; "
        result = result.replace('\'', '`')
        filter = f"SELECT * FROM schedule WHERE group_name = '{group}'"
        action1 = f"INSERT INTO schedule (group_name, day{counter}) VALUES ('{group}', '{result}')"
        action2 = f"UPDATE schedule SET day{counter} = '{result}' WHERE group_name = '{group}'"
        SQL.exist_test_insert(filter, action1, action2)
        counter += 1


def inserter_professor(week, group, data):
    """Function inserts or updates professors for a group"""
    for days in data[f"{week}"]:
        for lessons_professors in days:
            if lessons_professors is not None:
                subject = lessons_professors[0].replace('\'', '`') + " " + lessons_professors[2].replace('\'', '`')
                professor = lessons_professors[1].replace('\'', '`')
                list_subjects = subject.split(", ")
                list_professors = professor.split(", ")
                for i in range(len(list_subjects)):
                    filter = f"SELECT '{list_subjects[i]}' FROM info_professor WHERE group_name = '{group}' AND name = '{list_professors[i]}'"
                    action1 = f"INSERT INTO info_professor (group_name, subject, name) VALUES ('{group}', '{list_subjects[i]}', '{list_professors[i]}')"
                    action2 = f"UPDATE info_professor SET name = '{list_professors[i]}' WHERE group_name = '{group}' AND subject = '{list_subjects[i]}'"
                    SQL.exist_test_insert(filter, action1, action2)
