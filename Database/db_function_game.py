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
    Version: 1.3
"""
import Database.SQL as SQL
import Database.reformattion_data as reformating_data


def user_check(user_id: int):
    """Function to check if user exists"""
    filter = f"SELECT * FROM game WHERE user_id='{user_id}'"
    data = SQL.execute(f"{filter}")
    return bool(data)


def add_new_gamer(user_id: int, user_name: str):
    """Function to add new gamer"""
    filter = f"INSERT INTO game (user_id, user_name_game) VALUES ('{user_id}','{user_name}')"
    SQL.table_operate(filter)


def score_by_gamer(user_id: int):
    """Function to execute score by gamer id"""
    filter = f"SELECT total_score FROM game WHERE user_id='{user_id}'"
    result = reformating_data.reformat_int(SQL.execute(filter))
    return result


def games_by_gamer(user_id: int):
    """Function to execute number of games by gamer id"""
    filter = f"SELECT total_games FROM game WHERE user_id='{user_id}'"
    result = reformating_data.reformat_int(SQL.execute(filter))
    return result


def name_by_gamer(user_id: int):
    """Function to execute name of gamer by id"""
    filter = f"SELECT user_name_game FROM game WHERE user_id='{user_id}'"
    result = reformating_data.reformat_str(SQL.execute(filter))
    return result


def change_name_gamer(user_id: int, new_name: str):
    filter = f"UPDATE game SET user_name_game = '{new_name}' WHERE user_id = '{user_id}'"
    SQL.table_operate(filter)


def update_score_by_user(user_id: int, new_score: int):
    """Function to update user score by gamer id"""
    filter = f"UPDATE game SET total_score = '{new_score}' WHERE user_id = '{user_id}'"
    SQL.table_operate(filter)


def update_games_by_user(user_id: int, new_games: int):
    """Function to update user number of games by gamer id"""
    filter = f"UPDATE game SET total_games = '{new_games}' WHERE user_id = '{user_id}'"
    SQL.table_operate(filter)


def top_gamers():
    """Function to execute top gamers"""
    filter = f"SELECT total_score, user_name_game, total_games FROM game ORDER BY total_score DESC limit(10)"
    result = reformating_data.reformat_list_3(SQL.execute(filter))
    return result
