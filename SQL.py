"""
 Description: This file has some functions which
              are used to operate with SQL DataBase.

       DataBase consists of some tables:

           users           -- user_id, user_name,
           info_users      -- user_id, user_group, schedule_switch
           list_groups     -- grup
           schedule        -- grup, day1, day2, day3, day4, day5, day6 ,day8, day9, day10, day11, day12, day13
           info_professor  -- subject, position, name, grup
           info_global     -- week


 Authors: Mikhail Shikalovskyi

 version 1.0
"""
import sqlite3


def connector_base_cursor():
    """Makes connection to DataBase "Bot" """
    conn = sqlite3.connect("Bot.db", check_same_thread=False)
    cursor = conn.cursor()
    return conn, cursor


def execute(filter) -> list:
    """Makes request to DataBase and returns values (list) using special 'filter' """
    conn, cursor = connector_base_cursor()
    cursor.execute(f"{filter}")
    results = cursor.fetchall()
    conn.close()
    return results


def table_operate(filter):
    """Makes request to DataBase and changes it in a proper way using 'filter' """
    conn, cursor = connector_base_cursor()
    cursor.execute(f"{filter}")  # Can be used to DELETE, INSERT, UPDATE Values
    conn.commit()
    conn.close()


def exist_test_insert(filter, action1, action2):
    """Allows us to avoid problems with DataBase with fields that are UNIQUE """
    data = execute(f"{filter}")  # Checking for existing such Data is DataBase
    if bool(data) is False:
        table_operate(f"{action1}")  # If it's not exist --> Adding
    else:
        table_operate(f"{action2}")  # Else --> Making another job (For example Updating Data)


"""
It's possible to use  ""  filter and action --> Returns nothing
Examples:

    1. SELECTING

        filter = "SELECT * FROM table"
        results = execute(filter)
        
    2. DELETING
        
        filter = "DELETE * FROM table WHERE **"
        table_operate(filter)
        
    3. UPDATING
    
        filter = "UPDATE {table} SET {what} = {val} WHERE **"
        table_operate(filter)
        
    4. INSERTING
    
        filter = "INSERT INTO {table} ({what}) VALUES ({val})"
        table_operate(filter)
        
    5. INSERTING (UNIQUE) with UPDATING if EXISTS
        
        filter = "SELECT * FROM Schedule WHERE grup = 'io-13'"
        action1  = "INSERT INTO {table} ({what}}) VALUES ({val})"
        action2  = "UPDATE {table} SET {what} = {val} WHERE **"
        exist_test_insert(filter, action1, action2) 
"""
