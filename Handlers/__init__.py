"""
    Description: Initializes Handlers.

    Author: Ivan Maruzhenko
    Version: 0.51
"""

from .commands import help
from .queue import daily_schedule, schedule_for_tomorrow, daily_routine
from .conversations import REGISTRATION_CONVERSATION, MAIN_CONVERSATION
