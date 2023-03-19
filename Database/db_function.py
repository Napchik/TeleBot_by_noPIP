"""
    Description: This file has some functions which
                 are used to execute/insert some data from/to Database.

          Database consists of some tables:
              log             -- id, parsing_time, status
              info_global     -- week
              info_professor  -- group_name, subject, name, type, link
              info_users      -- user_id, user_name, user_surname, nick_name
              list_groups     -- group_name
              schedule        -- group_name, day1, day2, day3, day4, day5, day6 ,day8, day9, day10, day11, day12, day13
              users           -- user_id, group_name, schedule_switch, status
              game            -- user_id, user_name_game, total_score, total_games

    Author: Mikhail Shikalovskyi
    Version: 1.4
"""
import Database.reformattion_data as reformation_data
import Database.SQL as SQL
from datetime import datetime


def today_day() -> int:
    """Function to find out number of week and what day is today"""
    filter = f"SELECT week FROM info_global"
    if SQL.execute(filter) == 1:
        result = datetime.today().isoweekday()
    else:
        result = datetime.today().isoweekday() + 7
    return result


def users_by_group(group: str) -> list:
    """Function to execute all user_id by group"""
    filter = f"SELECT user_id FROM info_users WHERE group_name = '{group}'"
    result = reformation_data.reformat_list(SQL.execute(filter))
    return result


def group_by_user(userid: int) -> str:
    """Function to execute all user_id by group"""
    filter = f"SELECT group_name FROM info_users WHERE user_id = '{userid}'"
    result = reformation_data.reformat_str(SQL.execute(filter))
    return result


def all_groups() -> list:
    """Function to execute list of all groups from Database"""
    filter = f"SELECT group_name FROM list_groups"
    result = reformation_data.reformat_list(SQL.execute(filter))
    return result


def schedule_day_by_group(group: str, day: int) -> str:
    """Function to execute schedule for special day"""
    if day == 7 or 14:
        return ''
    filter = f"SELECT day{day} FROM schedule WHERE group_name = '{group}'"
    result = reformation_data.reformat_str(SQL.execute(filter))
    return result


def professor_by_subject(group: str, subject: str) -> str:
    filter = f"SELECT name FROM info_professor WHERE group_name='{group}' AND subject = '{subject}'"
    result = reformation_data.reformat_str(SQL.execute(filter))
    return result


def link_by_subject(group: str, subject: str):
    filter = f"SELECT link FROM info_professor WHERE group_name='{group}' AND subject = '{subject}'"
    result = reformation_data.reformat_str(SQL.execute(filter))
    return result


def inserter_schedule(week: str, group: str, data: list):
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


def inserter_professor(week: str, group: str, data: list):
    """Function inserts or updates professors for a group"""
    for days in data[f"{week}"]:
        for lessons_professors in days:
            if lessons_professors is not None:
                subject = lessons_professors[0].replace('\'', '`') + " " + lessons_professors[2].replace('\'', '`')
                professor = lessons_professors[1].replace('\'', '`')
                position = lessons_professors[2].replace('\'', '`')
                filter = f"SELECT * FROM info_professor WHERE group_name = '{group}' AND subject = '{subject}'"
                action1 = f"INSERT INTO info_professor (group_name, subject, name, type) VALUES ('{group}', '{subject}', '{professor}', '{position}') "
                SQL.exist_test_insert(filter, action1, "")
