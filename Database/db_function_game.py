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
import Database.SQL as SQL
import Database.reformattion_data as reformating_data


def user_check(user_id: int):
    filter = f"SELECT * FROM game WHERE user_id='{user_id}'"
    data = SQL.execute(f"{filter}")
    return bool(data)


def add_new_gamer(user_id: int, user_name: str):
    filter = f"INSERT INTO game (user_id, user_name_game) VALUES ('{user_id}','{user_name}')"
    SQL.table_operate(filter)


def score_by_gamer(user_id: int):
    filter = f"SELECT total_score FROM game WHERE user_id='{user_id}'"
    result = reformating_data.reformat_int(SQL.execute(filter))
    return result


def games_by_gamer(user_id: int):
    filter = f"SELECT total_games FROM game WHERE user_id='{user_id}'"
    result = reformating_data.reformat_int(SQL.execute(filter))
    return result


def update_score_by_user(user_id: int, new_score: int):
    filter = f"UPDATE game SET total_score = '{new_score}' WHERE user_id = '{user_id}'"
    SQL.table_operate(filter)


def update_games_by_user(user_id: int, new_games: int):
    filter = f"UPDATE game SET total_games = '{new_games}' WHERE user_id = '{user_id}'"
    SQL.table_operate(filter)


def top_gamers():
    filter = f"SELECT total_score, user_name_game, total_games FROM game ORDER BY total_score DESC limit(10)"
    result = reformating_data.reformat_list_3(SQL.execute(filter))
    return result
