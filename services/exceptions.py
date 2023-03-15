"""
    Description: File with custom exceptions.

    Author: Ivan Maruzhenko

    version 0.1
"""

import telegram.error


class FailedToSend(telegram.error.BadRequest):
    pass
