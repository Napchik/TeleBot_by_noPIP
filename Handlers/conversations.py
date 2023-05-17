"""
    Description: Contains conversation handlers.

    Author: Ivan Maruzhenko
    Version: 0.3
"""

from Services.registration_conversation import (
    GROUP,
    ROUTINE,
    REG_INFO,
    start,
    group,
    routine,
    info,
    cancel,
    misunderstand
)

from Services.main_conversation import (
    MENU,
    SCHEDULE,
    GAME,
    SETTINGS,
    CONTROLS,
    start_main,
    schedule,
    game,
    settings,
    controls,
    back_to_main
)

from Services.week_schedule_conversation import (
    CHANGE_DAY_IN_WEEK,
    send_week_schedule, next_day_in_week,
    previous_day_in_week
)

from Services.all_schedule_conversation import CHANGE_DAY, send_all_schedule, next_day, previous_day

from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    CommandHandler,
    filters
)

from Services.messages import RoutineChoice

import Handlers

answers = RoutineChoice.Answers


REGISTRATION_CONVERSATION = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        GROUP: [
            MessageHandler(filters.Regex("[A-Za-z]{2}-[0-9]{2}"), group)],  # TODO Зробити універсальний REGEX

        ROUTINE: [
            MessageHandler(
                filters.Regex(
                    f"({answers.REG_NO})|"
                    f"({answers.REG_MORNING})|"
                    f"({answers.REG_ALL})"),
                routine)],

        REG_INFO: [
            MessageHandler(filters.Regex("(Зрозуміло)"), info)]},
    fallbacks=[
        CommandHandler("cancel", cancel),
        MessageHandler(filters.Regex("(Скасувати)"), cancel),
        MessageHandler(filters.TEXT, misunderstand)])


ALL_SCHEDULE_CONVERSATION = ConversationHandler(

    entry_points=[MessageHandler(filters.Regex(answers.SCHEDULE_ALL), send_all_schedule)],

    allow_reentry=True,

    conversation_timeout=60,

    states={

        CHANGE_DAY: [
            CallbackQueryHandler(previous_day, pattern="back"),
            CallbackQueryHandler(next_day, pattern="forward")]},

    fallbacks=[

        MessageHandler(filters.Regex(answers.BACK), back_to_main),
        MessageHandler(filters.TEXT, misunderstand)

    ])


WEEK_SCHEDULE_CONVERSATION = ConversationHandler(

    entry_points=[MessageHandler(filters.Regex(answers.SCHEDULE_WEEK), send_week_schedule)],

    allow_reentry=True,

    conversation_timeout=60,

    states={

        CHANGE_DAY_IN_WEEK: [
            CallbackQueryHandler(previous_day_in_week, pattern="previous_day"),
            CallbackQueryHandler(next_day_in_week, pattern="next_day")]},

    fallbacks=[

        ALL_SCHEDULE_CONVERSATION,
        MessageHandler(filters.Regex(answers.BACK), back_to_main),
        MessageHandler(filters.TEXT, misunderstand)
    ])


MAIN_CONVERSATION = ConversationHandler(

    entry_points=[

        CommandHandler("menu", start_main),
        MessageHandler(filters.Regex(answers.BACK), start_main)
    ],

    allow_reentry=True,

    states={

        MENU: [

            MessageHandler(filters.Regex(answers.MAIN_SCHEDULE), schedule),
            MessageHandler(filters.Regex(answers.MAIN_GAME), game),
            MessageHandler(filters.Regex(answers.MAIN_SETTINGS), settings),
            MessageHandler(filters.Regex(answers.MAIN_CONTROLS), controls)

        ],

        SCHEDULE: [

            MessageHandler(filters.Regex(answers.SCHEDULE_TODAY), Handlers.today),
            MessageHandler(filters.Regex(answers.SCHEDULE_TOMORROW), Handlers.tomorrow),
            WEEK_SCHEDULE_CONVERSATION,
            ALL_SCHEDULE_CONVERSATION

        ]},

    # GAME: [],
    #
    # SETTINGS: [],
    #
    # CONTROLS: []},

    fallbacks=[

        MessageHandler(filters.Regex(answers.BACK), start_main),
        MessageHandler(filters.TEXT, misunderstand)

    ])
