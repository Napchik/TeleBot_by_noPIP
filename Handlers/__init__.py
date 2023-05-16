"""
    Description: Initializes Handlers.

    Author: Ivan Maruzhenko
    Version: 0.51
"""

from .commands import help, today, tomorrow
from .queue import daily_schedule, schedule_for_tomorrow
from .conversations import REGISTRATION_CONVERSATION, MAIN_CONVERSATION, WEEK_SCHEDULE_CONVERSATION
