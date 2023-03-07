
def inserter_schedule(week: str, group: str, data: list):
    """Function inserts or updates schedule for a group"""
    if week == "week1":
        counter = 1
    else:
        counter = 8
    for days in data[f"{week}"]:
        result = []
        print(result)
        for lessons in days:
            if lessons is not None:
                lesson = lessons[0].replace('\'', '`')
                type = lessons[2].replace('\'', '`')
                a = [lesson, type]
                result.append(a)
            else:
                a = []
                result.append(a)
        # result = result.replace('\'', '`')
        filter = f"SELECT * FROM schedule WHERE group_name = '{group}'"
        action1 = f"INSERT INTO schedule (group_name, day{counter}) VALUES ('{group}', '{result}')"
        action2 = f"UPDATE schedule SET day{counter} = '{str(result)}' WHERE group_name = '{group}'"
        SQL.exist_test_insert(filter, action1, action2)
        counter += 1



Есть запрос от юзера->
user_id

result = DataBase.db_function_game.user_check(user_id)
if result is False:
    print("Как тебя называть")
    ждем ответа
    получаем user_name
    DataBase.db_function_game.add_new_gamer(user_id,user_name)
    print("Гарної гри!")
    дальше ---->

else:
    print("Ты есть в базе")
    дальше ---->