"""
 Description: This file uses to activate daily functions

 Authors: Mikhail Shikalovskyi

 version 1.0
"""
from DataBase.schedule_uploader import *
import schedule
import time

# schedule.every().day.at("01:00").do(schedule_info_uploader())
schedule.every(10).seconds.do(schedule_info_uploader)

while True:
    schedule.run_pending()
    time.sleep(1)
