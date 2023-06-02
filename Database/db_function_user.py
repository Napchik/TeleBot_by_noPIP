"""
    Description: This file has some functions which
                 are used to execute/insert some data from/to Database.

          Database consists of some tables:
              log             -- id, time, info
              info_global     -- week, time_lesson1, time_lesson2, time_lesson3, time_lesson4, time_lesson5,
                                    time_lesson6, day2, day3, day4, day5, day6, day1,
                                    day2, day3, day4, day5, day6, day7 ,day8, day9, day10, day11, day12, day13, day14
              info_professor  -- group_name, subject, name, type, link
              info_users      -- user_id, user_name, user_surname, nick_name
              list_groups     -- group_name
              schedule        -- group_name, day1, day2, day3, day4, day5, day6 ,day8, day9, day10, day11, day12, day13
              users           -- user_id, group_name, schedule_switch, status, is_blocked
              game            -- user_id, user_name_game, total_score, total_games

    Author: Mikhail Shikalovskyi
    Version: 1.3
"""
import Database.reformattion_data as reformation_data
import Database.SQL as SQL
import Database.db_function as db_function
from loger_config import logger


def check_group(group: str):
    """Function which checks if group exists in database"""
    filter = f"SELECT * FROM list_groups WHERE group_name = '{group}'"
    result = reformation_data.reformat_str(SQL.execute(filter))
    return bool(result)


def check_user(user_id: int):
    """Function which checks if user exists in database"""
    filter = f"SELECT * FROM users WHERE user_id = '{user_id}'"
    result = reformation_data.reformat_int(SQL.execute(filter))
    return bool(result)


def check_user_role(user_id: int):
    """Function which checks role of user in database"""
    filter = f"SELECT role FROM users WHERE user_id = '{user_id}'"
    result = reformation_data.reformat_str(SQL.execute(filter))
    return result


def choose_role(group_name: str):
    """Function which checks quantity of moderators in group and returns name on role chosen"""
    filter = f"SELECT user_id FROM users WHERE group_name = '{group_name}'"
    result = reformation_data.reformat_list(SQL.execute(filter))
    if len(result) < 3:
        return "moderator"
    else:
        return "user"


def check_user_group(user_id: int):
    """Function which returns name of group by user"""
    filter = f"SELECT group_name FROM users WHERE user_id = '{user_id}'"
    result = reformation_data.reformat_str(SQL.execute(filter))
    return result


def add_user(user_name: str, user_surname: str, user_nickname: str, user_id: int, user_group: str,
             user_schedule: int,
             user_role: str):
    """Function which adds new user and new group in list of groups or updates data which already exists"""
    if check_user(user_id) is False:
        filter = f"INSERT INTO users ('user_id', 'group_name', 'schedule_switch', 'role') VALUES ('{user_id}', '{user_group}', '{user_schedule}','{user_role}')"
        SQL.table_operate(filter)
        filter = f"INSERT INTO info_users ('user_id', 'user_name', 'user_surname', 'user_nickname') VALUES ('{user_id}', '{user_name}', '{user_surname}','{user_nickname}')"
        SQL.table_operate(filter)
        if check_group(user_group) is False:
            add_new_group(user_group)
    else:
        filter = f"UPDATE users SET group_name = '{user_group}', schedule_switch = '{user_schedule}', role = '{user_role}' WHERE user_id = '{user_id}'"
        SQL.table_operate(filter)
        filter = f"UPDATE info_users SET user_name = '{user_name}', user_surname = '{user_surname}', user_nickname = '{user_nickname}' WHERE user_id = '{user_id}'"
        SQL.table_operate(filter)
    logger.info(f"New user: {user_name}, {user_nickname} added.")
    db_function.add_log(f"New user: {user_name}, {user_nickname} added.")


def update_schedule_switch(user_id: int, schedule_switch: int):
    """Function to change schedule_switch by user_id 0 -> no schedule  1 -> only morning 2 -> morning and evening"""
    if check_user(user_id) is True:
        filter = f"UPDATE users SET schedule_switch = '{schedule_switch}' WHERE user_id = '{user_id}'"
        SQL.table_operate(filter)


def change_group(user_id: int, group_name: str):
    """Function to change user group"""
    if check_user(user_id) is True:
        filter = f"UPDATE users SET group_name = '{group_name}' WHERE user_id = '{user_id}'"
        SQL.table_operate(filter)


def list_lessons(group: str):
    """Function to execute list of lessons"""
    filter = f"SELECT subject FROM info_professor WHERE group_name = '{group}'"
    return reformation_data.reformat_list(SQL.execute(filter))


def add_new_group(group: str):
    """Function to add new group in list of groups"""
    filter = f"INSERT INTO list_groups ('group_name') VALUES ('{group}')"
    SQL.table_operate(filter)


def change_is_blocked(user_id: int):
    """Function to change user attribute 'is_blocked' to identify inactive users"""
    filter = f"UPDATE users SET is_blocked = 1 WHERE user_id = '{user_id}'"
    SQL.table_operate(filter)


def deleting_blocked_user():
    """Function to delete inactive users"""
    filter = "SELECT user_id FROM users WHERE is_blocked = 1"
    list_user_id = reformation_data.reformat_list(SQL.execute(filter))
    for user_id in list_user_id:
        filter = f"DELETE FROM users WHERE user_id = '{user_id}'"
        SQL.table_operate(filter)
        filter = f"DELETE FROM info_users WHERE user_id = '{user_id}'"
        SQL.table_operate(filter)
        db_function.add_log(f"User: {user_id} has been deleted")
    logger.info(f"Blocked users has been deleted.")
