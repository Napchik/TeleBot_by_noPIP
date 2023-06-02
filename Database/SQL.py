"""
    Description: This file has some functions which
                 are used to operate with SQL Database.

    Author: Mikhail Shikalovskyi
    Version: 2.0
"""
import sqlite3
import os
from loger_config import logger


def connector_base_cursor():
    """Makes connection to Database "Bot" """
    try:
        folder = os.path.abspath(os.curdir).split("\\")
        if "Database" in folder or "Handlers" in folder or "Services" in folder:
            del folder[-1]
            a = "\\".join(folder)
            conn = sqlite3.connect(f"{a}\Bot.db", check_same_thread=False)
        else:
            conn = sqlite3.connect("Bot.db", check_same_thread=False)
        cursor = conn.cursor()
        return conn, cursor
    except:
        logger.critical("Can't connect to Database")


def execute(filter) -> list:
    """Makes request to Database and returns values (list) using special 'filter' """
    try:
        conn, cursor = connector_base_cursor()
        cursor.execute(f"{filter}")  # Can be used to SELECT Values
        results = cursor.fetchall()
        conn.close()
        return results
    except:
        logger.critical(f"Can't execute data from Database : {filter}")


def table_operate(filter):
    """Makes request to Database and changes it in a proper way using 'filter' """
    try:
        conn, cursor = connector_base_cursor()
        cursor.execute(f"{filter}")  # Can be used to DELETE, INSERT, UPDATE Values
        conn.commit()
        conn.close()
    except:
        logger.info(f"Can't operate data from Database : {filter}")


def exist_test_insert(filter, action1, action2):
    """Allows us to avoid problems with Database with fields that are UNIQUE """
    data = execute(f"{filter}")  # Checking for existing such Data is Database
    if bool(data) is False:
        try:
            table_operate(f"{action1}")  # If it's not exist --> Adding
        except:
            logger.info(f"Can't add data to Database : {filter}")
    else:
        try:
            table_operate(f"{action2}")  # Else --> Making another job (For example Updating Data)
        except:
            logger.info(f"Can't operate data from Database : {filter}")


"""
It's possible to use  ""  filter and action --> Returns nothing
Examples:

    1. SELECTING

        filter = "SELECT * FROM table"
        results = execute(filter)
        
    2. DELETING
        
        filter = "DELETE FROM table WHERE **"
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
