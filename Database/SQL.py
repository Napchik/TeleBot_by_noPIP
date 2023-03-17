"""
    Description: This file has some functions which
                 are used to operate with SQL Database.

    Author: Mikhail Shikalovskyi
    Version: 1.5
"""

import sqlite3


def connector_base_cursor():
    """Makes connection to Database "Bot" """
    conn = sqlite3.connect("Database/Bot.db", check_same_thread=False)
    cursor = conn.cursor()
    # exception!!! Can't connect to Database
    return conn, cursor


def execute(filter) -> list:
    """Makes request to Database and returns values (list) using special 'filter' """
    conn, cursor = connector_base_cursor()
    cursor.execute(f"{filter}")  # Can be used to SELECT Values
    results = cursor.fetchall()
    # exception!!! Can't execute data from Database : {filter}
    conn.close()
    return results


def table_operate(filter):
    """Makes request to Database and changes it in a proper way using 'filter' """
    conn, cursor = connector_base_cursor()
    cursor.execute(f"{filter}")  # Can be used to DELETE, INSERT, UPDATE Values
    # exception!!! Can't operate data from Database : {filter}
    conn.commit()
    conn.close()


def exist_test_insert(filter, action1, action2):
    """Allows us to avoid problems with Database with fields that are UNIQUE """
    data = execute(f"{filter}")  # Checking for existing such Data is Database
    if bool(data) is False:
        table_operate(f"{action1}")  # If it's not exist --> Adding
        # exception!!! Can't add data to Database : {filter}
    else:
        table_operate(f"{action2}")  # Else --> Making another job (For example Updating Data)
        # exception!!! Can't operate data from Database : {filter}


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
        
        filter = "SELECT * FROM Schedule WHERE group_name = 'io-13'"
        action1  = "INSERT INTO {table} ({what}) VALUES ({val})"
        action2  = "UPDATE {table} SET {what} = {val} WHERE **"
        exist_test_insert(filter, action1, action2) 
"""
