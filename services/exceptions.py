
"""
    Description: File with custom exceptions.

    Author: Ivan Maruzhenko

    version 0.1
"""

import logging


class FailedToSend(Exception):
    logging.warning("Raised exception 'FailedToSend'.")
