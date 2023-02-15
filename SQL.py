#
# Description: some decr
#
# Authors: Mikhail Shikalovskyi
#
# version 0.0
import sqlite3


def execute(what, table, special, condition):
    conn = sqlite3.connect("Bot.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute(f"SELECT {what} FROM {table} {special} {condition}")
    results = cursor.fetchall()
    conn.close()
    return results


def table_operate(operator, what, from_into, table, special, condition, values):
    conn = sqlite3.connect("Bot.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute(f"{operator} {what} {from_into} {table} {special} {condition} {values}")
    conn.commit()
    conn.close()
