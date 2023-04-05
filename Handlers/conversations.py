"""
    Description: Contains conversation handler.

    Author: Ivan Maruzhenko
    Version: 0.1
"""

from Services.registration_conversation import (
    GROUP,
    ROUTINE,
    INFO,
    start,
    group,
    routine,
    info,
    cancel,
    misunderstand,
    answers
)
from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    CommandHandler,
    filters
)

CONVERSATION_HANDLER = ConversationHandler(entry_points=[CommandHandler("start", start)],
                                           states={
                                               GROUP: [
                                                   MessageHandler(filters.Regex("[A-Za-z]{2}-[0-9]{2}"), group),
                                               ],

                                               ROUTINE: [
                                                   MessageHandler(
                                                       filters.Regex(
                                                           f"({answers.NO})|({answers.MORNING})|({answers.ALL})"),
                                                       routine)],

                                               INFO: [
                                                   MessageHandler(filters.Regex("(Зрозуміло)"), info)]},
                                           fallbacks=[
                                               CommandHandler("cancel", cancel),
                                               MessageHandler(filters.Regex("(Скасувати)"), cancel),
                                               MessageHandler(filters.TEXT, misunderstand)])
