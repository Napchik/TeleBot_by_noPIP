"""
    Description: Contains conversation handlers.

    Author: Ivan Maruzhenko
    Version: 0.5
"""

from Services.registration_conversation import (
    GROUP,
    ROUTINE,
    REG_INFO,
    REG_EXIT,
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
    WEEK_SCHEDULE,
    ALL_SCHEDULE,
    send_week_schedule,
    next_day_in_week,
    previous_day_in_week,
    send_all_schedule,
    next_day,
    previous_day,
    send_week_schedule_links,
    send_all_schedule_links
)

from Services.settings_conversation import (
    CHANGE_TIME,
    CHANGE_GROUP,
    switch_schedule_mode,
    update_schedule_mode,
    switch_group_mode,
    update_group_mode, cancel_change,
    report_bug
)

# from Services.all_schedule_conversation import CHANGE_DAY, send_all_schedule, next_day, previous_day

from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    CommandHandler,
    filters
)

from Services.one_day_schedule_conversation import (
    today,
    today_links,
    tomorrow,
    tomorrow_links,
    GET_TODAY_LINKS,
    GET_TOMORROW_LINKS
)
from Services.messages import RoutineChoice

import re

answers = RoutineChoice.Answers
pattern_ua = re.compile(r"^[А-ЩЬЮЯЇІЄҐ]{2}-\d{2}$", re.IGNORECASE)

ALL_SCHEDULE_CONVERSATION = ConversationHandler(

    entry_points=

    [
        MessageHandler(filters.Regex(answers.SCHEDULE_ALL), send_all_schedule),
        MessageHandler(filters.Regex(answers.SCHEDULE_WEEK), send_week_schedule)
    ],

    allow_reentry=True,

    conversation_timeout=60,

    states={

        ALL_SCHEDULE:

            [
                CallbackQueryHandler(previous_day, pattern="back"),
                CallbackQueryHandler(next_day, pattern="forward"),

                CallbackQueryHandler(send_all_schedule_links, pattern="all_schedule_links")

            ],

        WEEK_SCHEDULE:
            [
                CallbackQueryHandler(previous_day_in_week, pattern="previous_day"),
                CallbackQueryHandler(next_day_in_week, pattern="next_day"),

                CallbackQueryHandler(send_week_schedule_links, pattern="week_schedule_links")
            ]},

    fallbacks=[

        MessageHandler(filters.Regex(answers.BACK), back_to_main),
        MessageHandler(filters.TEXT, misunderstand)

    ])

# WEEK_SCHEDULE_CONVERSATION = ConversationHandler(
#
#     entry_points=[MessageHandler(filters.Regex(answers.SCHEDULE_WEEK), send_week_schedule)],
#
#     allow_reentry=True,
#
#     conversation_timeout=60,
#
#     states={
#
#         CHANGE_DAY_IN_WEEK: [
#             CallbackQueryHandler(previous_day_in_week, pattern="previous_day"),
#             CallbackQueryHandler(next_day_in_week, pattern="next_day"),
#             ALL_SCHEDULE_CONVERSATION,
#         ]},
#
#     fallbacks=[
#
#         MessageHandler(filters.Regex(answers.BACK), back_to_main),
#         MessageHandler(filters.TEXT, misunderstand)
#     ])

ONE_DAY_SCHEDULE_CONVERSATION = ConversationHandler(

    entry_points=

    [
        MessageHandler(filters.Regex(answers.SCHEDULE_TODAY), today),
        MessageHandler(filters.Regex(answers.SCHEDULE_TOMORROW), tomorrow)
    ],

    allow_reentry=True,

    conversation_timeout=60,

    states={
        GET_TODAY_LINKS:
            [
                CallbackQueryHandler(today_links, pattern="today_links"),
            ],
        GET_TOMORROW_LINKS:
            [
                CallbackQueryHandler(tomorrow_links, pattern="tomorrow_links")
            ]
    },

    fallbacks=

    [
        ALL_SCHEDULE_CONVERSATION,
        MessageHandler(filters.Regex(answers.BACK), back_to_main),
        MessageHandler(filters.TEXT, misunderstand)
    ]
)

SWITCH_TIME_CONVERSATION = ConversationHandler(

    entry_points=[MessageHandler(filters.Regex(answers.SETTINGS_TIME), switch_schedule_mode)],

    allow_reentry=True,

    conversation_timeout=60,

    states={

        CHANGE_TIME: [
            MessageHandler(filters.Regex(f"({answers.SETTINGS_NO})|"
                                         f"({answers.SETTINGS_MORNING})|"
                                         f"({answers.SETTINGS_ALL})"),
                           update_schedule_mode)
        ]},

    fallbacks=[

        MessageHandler(filters.Regex(answers.BACK), back_to_main),
        MessageHandler(filters.TEXT, misunderstand)
    ])

SWITCH_GROUP_CONVERSATION = ConversationHandler(

    entry_points=[MessageHandler(filters.Regex(answers.SETTINGS_GROUP), switch_group_mode)],

    allow_reentry=True,

    conversation_timeout=60,

    states={

        CHANGE_GROUP: [
            MessageHandler(filters.Regex(pattern_ua), update_group_mode)
        ]},

    fallbacks=[

        MessageHandler(filters.Regex(answers.SETTINGS_DENY), cancel_change),
        MessageHandler(filters.Regex(answers.BACK), back_to_main),
        MessageHandler(filters.TEXT, misunderstand)
    ])

MAIN_CONVERSATION = ConversationHandler(

    entry_points=[

        CommandHandler("menu", start_main),
        MessageHandler(filters.Regex(answers.BACK), start_main),
        MessageHandler(filters.Regex(answers.GOT_IT), start_main),
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

            ONE_DAY_SCHEDULE_CONVERSATION,
            ALL_SCHEDULE_CONVERSATION

        ],

        SETTINGS: [

            SWITCH_TIME_CONVERSATION,
            SWITCH_GROUP_CONVERSATION,
            MessageHandler(filters.Regex(answers.SETTINGS_BUG), report_bug),

        ]
    },

    # GAME: [],
    #
    # CONTROLS: []},

    fallbacks=[

        MessageHandler(filters.Regex(answers.BACK), start_main),
        MessageHandler(filters.TEXT, misunderstand)

    ])

REGISTRATION_CONVERSATION = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    allow_reentry=True,
    states={
        GROUP:
            [
                MessageHandler(filters.Regex(pattern_ua), group)
            ],

        ROUTINE:
            [
                MessageHandler(
                    filters.Regex(
                        f"({answers.REG_NO})|"
                        f"({answers.REG_MORNING})|"
                        f"({answers.REG_ALL})"),
                    routine)
            ],

        REG_INFO:
            [
                MessageHandler(filters.Regex(answers.GOT_IT), info),
            ],

        REG_EXIT:
            [
                MAIN_CONVERSATION
            ]
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
        MessageHandler(filters.Regex(answers.CANCEL), cancel),
        MessageHandler(filters.TEXT, misunderstand)])
