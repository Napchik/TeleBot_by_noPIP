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
    Version: 1.1
"""
import Database.reformattion_data as reformation_data
import Database.SQL as SQL


def check_user(user_id: int):
    filter = f"SELECT * FROM users WHERE user_id = '{user_id}'"
    result = reformation_data.reformat_str(SQL.execute(filter))
    if bool(result) is False:
        return False
    else:
        return True


def update_schedule_switch(user_id: int, schedule_switch: int):
    if check_user(user_id) is True:
        filter = f"UPDATE users SET schedule_switch = '{schedule_switch}' WHERE user_id = '{user_id}'"
        SQL.table_operate(filter)
