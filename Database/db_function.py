"""
    Description: This file has some functions which
                 are used to execute/insert some data from/to Database.

          Database consists of some tables:
              log             -- id, time, info
              info_global     -- week, time_lesson1, time_lesson2, time_lesson3, time_lesson4, time_lesson5,
                                    time_lesson6, day2, day3, day4, day5, day6, day1,
                                    day2, day3, day4, day5, day6, day7 ,day8, day9, day10, day11, day12, day13, day14
              info_professor  -- group_name, subject, name, type, link
              info_users      -- user_id, user_name, user_surname, user_nickname
              list_groups     -- group_name
              schedule        -- group_name, day1, day2, day3, day4, day5, day6 ,day8, day9, day10, day11, day12, day13
              users           -- user_id, group_name, schedule_switch, status, is_blocked
              game            -- user_id, user_name_game, total_score, total_games


    Author: Mikhail Shikalovskyi
    Version: 1.0 (release)
"""
import Database.reformattion_data as reformation_data
import Database.SQL as SQL
from datetime import datetime
from loger_config import logger


def add_log(log: str):
    """
        Function to add logs into database

        :param log: text of log which must be inserted into table
    """
    filter = f"INSERT INTO log (time, info) VALUES ('{datetime.now()}', '{log}')"
    SQL.table_operate(filter)
    logger.info("Log has been inserted into database")


def today_day() -> int:
    """ Function to find out number of week and what day is today """
    filter = f"SELECT week FROM info_global"
    if SQL.execute(filter) == 1:
        result = datetime.today().isoweekday()
    else:
        result = datetime.today().isoweekday() + 7
    return result


def tomorrow_day() -> int:
    """ Function to find out number of day is tomorrow """
    if today_day() == 14:
        return 1
    return today_day() + 1


def get_week() -> int:
    """ Function to find out number of week 1 -> week1 2 -> week2 """
    filter = f"SELECT week FROM info_global"
    result = reformation_data.reformat_int(SQL.execute(filter))
    return result


def change_week():
    """ Function to change week on Mondays """
    if datetime.today().isoweekday() == 1:
        week = get_week()
        if week == 1:
            week = 2
        else:
            week = 1
        filter = f"UPDATE info_global SET week = {week}"
        SQL.table_operate(filter)
        add_log("Week changed successfully")


def users_by_group(group: str) -> list:
    """ Function to execute all user_id by group

        :param group: group name of user used in filter
    """
    filter = f"SELECT user_id FROM users WHERE group_name = '{group}'"
    result = reformation_data.reformat_list(SQL.execute(filter))
    return result


def all_groups() -> list:
    """ Function to execute list of all groups from Database """
    filter = f"SELECT group_name FROM list_groups"
    result = reformation_data.reformat_list(SQL.execute(filter))
    return result


def schedule_day_by_group(group: str, day: int) -> str:
    """
        Function to execute schedule for special day

        :param group: group name of user used in filter
        :param day: number of day for which schedule must be got
    """
    if day == 7 or day == 14:
        return ''
    filter = f"SELECT day{day} FROM schedule WHERE group_name = '{group}'"
    result = reformation_data.reformat_str(SQL.execute(filter))
    return result


def professor_by_subject(group: str, subject: str) -> str:
    """
        Function to execute name of professor by subject name

        :param group: group name of user used in filter
        :param subject: name of lesson for which professor must be got
    """
    filter = f"SELECT name FROM info_professor WHERE group_name='{group}' AND subject = '{subject}'"
    result = reformation_data.reformat_str(SQL.execute(filter))
    return result


def link_by_subject(group: str, subject: str):
    """
        Function to execute link for subject by subject name

        :param group: group name of user used in filter
        :param subject: name of lesson for which link must be got
    """
    filter = f"SELECT link FROM info_professor WHERE group_name='{group}' AND subject = '{subject}'"
    result = reformation_data.reformat_str(SQL.execute(filter))
    return result


def update_link_by_subject(group: str, subject: str, new_link: str):
    """
        Function to update link by group and subject name

        :param group: group name of user used in filter
        :param subject: name of lesson which is used in filter
        :param new_link: new link to update
    """
    filter = f"UPDATE info_professor SET link = '{new_link}' WHERE group_name='{group}' AND subject = '{subject}'"
    SQL.table_operate(filter)
    add_log(f"{group}: Link changed successfully")


def time_by_number(number: int) -> str:
    """
        Function to execute time of lesson given

        :param number: number of lesson which is used in filter
    """
    filter = f"SELECT time_lesson{number} FROM info_global"
    result = reformation_data.reformat_str(SQL.execute(filter))
    return result


def day_name(day: int) -> str:
    """
        Function to execute name of day by day number

        :param day: number of day which is used in filter
    """
    filter = f"SELECT day{day} FROM info_global"
    result = reformation_data.reformat_str(SQL.execute(filter))
    return result


def inserter_schedule(week: str, group: str, data: dict):
    """
        Function inserts or updates schedule for a group

        :param week: number of week which is inserting
        :param group: name of group which schedule is inserting
        :param data: all schedule in dict format
    """
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
    logger.info("Schedule has been inserted into database")


def inserter_professor(week: str, group: str, data: dict):
    """
        Function inserts or updates professors for a group

        :param week: number of week which is inserting
        :param group: name of group which professors is inserting
        :param data: all professors in dict format
    """
    for days in data[f"{week}"]:
        for lessons_professors in days:
            if lessons_professors is not None:
                subject = lessons_professors[0].replace('\'', '`') + " " + lessons_professors[2].replace('\'', '`')
                professor = lessons_professors[1].replace('\'', '`')
                position = lessons_professors[2].replace('\'', '`')
                filter = f"SELECT * FROM info_professor WHERE group_name = '{group}' AND subject = '{subject}'"
                action1 = f"INSERT INTO info_professor (group_name, subject, name, type) VALUES ('{group}', '{subject}', '{professor}', '{position}') "
                SQL.exist_test_insert(filter, action1, "")
    logger.info("Professors have been inserted into database")
