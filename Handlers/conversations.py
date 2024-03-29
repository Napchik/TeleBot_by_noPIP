"""
    Description: Contains conversation handlers.

    Author: Ivan Maruzhenko
    Version: 1.0
"""

import re

from Services.registration_conversation import (
    GROUP,
    ROUTINE,
    REG_INFO,
    REG_EXIT,
    start_reg,
    group,
    set_routine,
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

from Services.weekly_schedule_conversation import (
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
    SEND_BUG,
    switch_schedule_mode,
    update_schedule_mode,
    switch_group_mode,
    update_group_mode,
    cancel_change,
    report_bug,
    send_bug_message
)

from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    CommandHandler,
    filters
)

from Services.daily_schedule_conversation import (
    today,
    today_links,
    tomorrow,
    tomorrow_links,
    TODAY_SCHEDULE,
    TOMORROW_SCHEDULE
)

from game import (
    DICE,
    ADD_PLAYER,
    CHANGE_NAME,
    game_start,
    dice_game,
    add_player,
    stop,
    top_players,
    change_name,
    update_name
)

from Services.controls_conversation import (
    choose_lesson_from_list,
    put_link,
    check_update_link,
    update_link_db,
    choose_user_from_list,
    check_update_role,
    update_role_db,
    CONTROLS_CHOOSE_LESSON,
    CONTROLS_UPDATE_LINK,
    CHECK_CORRECT,
    CHECK_ROLE_CORRECT,
    CONTROLS_CHOOSE_USER

)

from Services.start_conversation import (
    start_communication,
    cancel_communication,
    RUN_MAIN,
    RUN_REG
)

from Services.routine_conversation import (
    routine_today_links,
    routine_tomorrow_links,
    TODAY_LINKS,
    TOMORROW_LINKS
)

from Services.messages import RoutineChoice

answers = RoutineChoice.Answers
pattern_ua = re.compile(r"^[А-ЩЬЮЯЇІЄҐ]{2}-\d{2}$", re.IGNORECASE)

"""
    Routine Conversation
    Dedicated for daily schedule messages.
    
    States:
    TODAY_LINKS
    TOMORROW_LINKS
"""
ROUTINE_CONVERSATION = ConversationHandler(

    entry_points=[
        CallbackQueryHandler(routine_today_links, pattern=re.compile("^routine_today_links\d+$")),
        CallbackQueryHandler(routine_tomorrow_links, pattern=re.compile("^routine_tomorrow_links\d+$"))
    ],

    states={
        TODAY_LINKS: [
            CallbackQueryHandler(routine_today_links, pattern=re.compile("^routine_today_links\d+$"))
        ],

        TOMORROW_LINKS: [
            CallbackQueryHandler(routine_tomorrow_links, pattern=re.compile("^routine_tomorrow_links\d+$"))
        ]
    },

    fallbacks=[
        MessageHandler(filters.Regex(answers.BACK), back_to_main),
        MessageHandler(filters.TEXT, misunderstand)
    ]
)


"""
    Schedule Conversation
    Dedicated for schedule request handle.

    States:
    TODAY_SCHEDULE
    TOMORROW_SCHEDULE
    ALL_SCHEDULE
"""
SCHEDULE_CONVERSATION = ConversationHandler(

    entry_points=[
        MessageHandler(filters.Regex(answers.SCHEDULE_TODAY), today),
        MessageHandler(filters.Regex(answers.SCHEDULE_TOMORROW), tomorrow),
        MessageHandler(filters.Regex(answers.SCHEDULE_ALL), send_all_schedule),
        MessageHandler(filters.Regex(answers.SCHEDULE_WEEK), send_week_schedule)
    ],

    allow_reentry=True,

    conversation_timeout=60,

    states={
        TODAY_SCHEDULE: [
            CallbackQueryHandler(today_links, pattern=re.compile("^today_links\d+$"))
        ],

        TOMORROW_SCHEDULE: [
            CallbackQueryHandler(tomorrow_links, pattern=re.compile("^tomorrow_links\d+$"))
        ],


        WEEK_SCHEDULE: [
            CallbackQueryHandler(previous_day_in_week, pattern="previous_day"),
            CallbackQueryHandler(next_day_in_week, pattern="next_day"),
            CallbackQueryHandler(send_week_schedule_links, pattern=re.compile("^week_schedule_links\d+$"))
        ],

        ALL_SCHEDULE: [
            CallbackQueryHandler(previous_day, pattern="back"),
            CallbackQueryHandler(next_day, pattern="forward"),
            CallbackQueryHandler(send_all_schedule_links, pattern=re.compile("^all_schedule_links\d+$"))
        ]
    },

    fallbacks=[
        MessageHandler(filters.Regex(answers.BACK), back_to_main),
        MessageHandler(filters.TEXT, misunderstand)
    ]
)

"""
    Switch Time Conversation
    Dedicated for time switch option.

    States:
    CHANGE_TIME
"""
SWITCH_TIME_CONVERSATION = ConversationHandler(

    entry_points=[MessageHandler(filters.Regex(answers.SETTINGS_TIME), switch_schedule_mode)],

    allow_reentry=True,

    states={
        CHANGE_TIME: [
            MessageHandler(filters.Regex(f"({answers.SETTINGS_NO})|"
                                         f"({answers.SETTINGS_MORNING})|"
                                         f"({answers.SETTINGS_ALL})"),
                           update_schedule_mode)
        ]
    },

    fallbacks=[
        MessageHandler(filters.Regex(answers.BACK), back_to_main),
        MessageHandler(filters.TEXT, misunderstand)
    ]
)

"""
    Switch Group Conversation
    Dedicated for switch group option.

    States:
    CHANGE_GROUP
"""
SWITCH_GROUP_CONVERSATION = ConversationHandler(

    entry_points=[MessageHandler(filters.Regex(answers.SETTINGS_GROUP), switch_group_mode)],

    allow_reentry=True,

    states={
        CHANGE_GROUP: [
            MessageHandler(filters.Regex(pattern_ua), update_group_mode)
        ]
    },

    fallbacks=[
        CallbackQueryHandler(cancel_change, pattern="deny"),
        MessageHandler(filters.Regex(answers.BACK), back_to_main),
        MessageHandler(filters.TEXT, misunderstand)
    ]
)

"""
    Report Bug Conversation
    Dedicated for bug reporting.

    States:
    SEND_BUG
"""
REPORT_BUG_CONVERSATION = ConversationHandler(

    entry_points=[MessageHandler(filters.Regex(answers.SETTINGS_BUG), report_bug)],

    allow_reentry=True,

    states={
        SEND_BUG: [
            MessageHandler(filters.TEXT, send_bug_message)
        ],
    },

    fallbacks=[
        MessageHandler(filters.Regex(answers.BACK), back_to_main),
        MessageHandler(filters.TEXT, misunderstand)
    ]
)

"""
    Game Conversation
    Dedicated for playing game.

    States:
    DICE
    ADD_PLAYER
"""
GAME_CONVERSATION = ConversationHandler(

    entry_points=[MessageHandler(filters.Regex(answers.GAME_THROW), game_start)],

    allow_reentry=True,

    states={
        DICE: [
            CallbackQueryHandler(dice_game, pattern="game_start"),
            CallbackQueryHandler(stop, pattern="game_stop")
        ],

        ADD_PLAYER: [
            MessageHandler(filters.TEXT, add_player),
            CallbackQueryHandler(dice_game, pattern="game_start"),
            CallbackQueryHandler(stop, pattern="game_stop")
        ],
    },

    fallbacks=[
        CommandHandler('stop_game', stop),
        MessageHandler(filters.TEXT, misunderstand)
    ]
)

"""
    Game Name Change Conversation
    Dedicated for changing name in game.

    States:
    ADD_PLAYER
    CHANGE_NAME
"""
GAME_CHANGE_NAME_CONVERSATION = ConversationHandler(

    entry_points=[MessageHandler(filters.Regex(answers.GAME_CHANGE), change_name)],

    allow_reentry=True,

    states={
        ADD_PLAYER: [
            MessageHandler(filters.TEXT, add_player)
        ],

        CHANGE_NAME: [
            MessageHandler(filters.TEXT, update_name)
        ]
    },

    fallbacks=[
        CommandHandler('stop_game', stop),
        MessageHandler(filters.TEXT, misunderstand)
    ]
)

"""
    Controls Link Conversation
    Dedicated for modifying links of subjects (moderators).

    States:
    CONTROLS_CHOOSE_LESSON
    CONTROLS_UPDATE_LINK
    CHECK_CORRECT
"""
CONTROLS_LINK_CONVERSATION = ConversationHandler(

    entry_points=[MessageHandler(filters.Regex(answers.CONTROLS_LINKS), choose_lesson_from_list)],

    allow_reentry=True,

    states={
        CONTROLS_CHOOSE_LESSON: [
            MessageHandler(filters.Regex(r'[0-9]'), put_link)
        ],

        CONTROLS_UPDATE_LINK: [
            MessageHandler(filters.Entity("url"), check_update_link)
        ],

        CHECK_CORRECT: [
            CallbackQueryHandler(update_link_db, pattern="confirm"),
            CallbackQueryHandler(cancel_change, pattern="cancel_change")
        ]
    },

    fallbacks=[
        MessageHandler(filters.Regex(answers.BACK), back_to_main),
        MessageHandler(filters.TEXT, misunderstand)
    ]
)

"""
    Controls Role Conversation
    Dedicated for role transfer (moderators).

    States:
    CONTROLS_CHOOSE_USER
    CHECK_ROLE_CORRECT
"""
CONTROLS_ROLE_CONVERSATION = ConversationHandler(

    entry_points=[MessageHandler(filters.Regex(answers.CONTROLS_ROLE), choose_user_from_list)],

    allow_reentry=True,

    states={
        CONTROLS_CHOOSE_USER: [
            MessageHandler(filters.Regex(r'[0-9]'), check_update_role)
        ],

        CHECK_ROLE_CORRECT: [
            CallbackQueryHandler(update_role_db, pattern="confirm"),
            CallbackQueryHandler(cancel_change, pattern="cancel_change")
        ],
    },

    fallbacks=[
        MessageHandler(filters.Regex(answers.GOT_IT), back_to_main),
        MessageHandler(filters.Regex(answers.BACK), back_to_main),
        MessageHandler(filters.TEXT, misunderstand)
    ]
)

"""
    Main Conversation
    Dedicated for handling main menu.

    States:
    MENU
    GAME
    SCHEDULE
    SETTINGS
    CONTROLS
"""
MAIN_CONVERSATION = ConversationHandler(

    entry_points=[
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

        GAME: [
            GAME_CONVERSATION,
            MessageHandler(filters.Regex(answers.GAME_TOP), top_players),
            GAME_CHANGE_NAME_CONVERSATION
        ],

        SCHEDULE: [
            SCHEDULE_CONVERSATION
        ],

        SETTINGS: [
            SWITCH_TIME_CONVERSATION,
            SWITCH_GROUP_CONVERSATION,
            REPORT_BUG_CONVERSATION
        ],

        CONTROLS: [
            CONTROLS_LINK_CONVERSATION,
            CONTROLS_ROLE_CONVERSATION
        ]
    },

    fallbacks=[
        MessageHandler(filters.Regex(answers.BACK), start_main),
        MessageHandler(filters.TEXT, misunderstand)
    ]
)

"""
    Registration Conversation
    Dedicated for user registration.

    States:
    GROUP
    ROUTINE
    REG_INFO
    REG_EXIT
"""
REGISTRATION_CONVERSATION = ConversationHandler(

    entry_points=[
        CommandHandler("reg", start_reg),
        MessageHandler(filters.Regex(answers.REG_START), start_reg)
    ],

    allow_reentry=True,

    states={
        GROUP: [
            MessageHandler(filters.Regex(pattern_ua), group)
        ],

        ROUTINE: [
            MessageHandler(filters.Regex(f"({answers.REG_NO})|"
                                         f"({answers.REG_MORNING})|"
                                         f"({answers.REG_ALL})"),
                           set_routine)
        ],

        REG_INFO: [
            MessageHandler(filters.Regex(answers.GOT_IT), info),
        ],

        REG_EXIT: [
            MAIN_CONVERSATION
        ]
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
        MessageHandler(filters.Regex(answers.CANCEL), cancel),
        MessageHandler(filters.TEXT, misunderstand)
    ]
)

"""
    Start Conversation
    Dedicated for handling /start command.

    States:
    RUN_MAIN
    RUN_REG
"""
START_CONVERSATION = ConversationHandler(
    entry_points=[CommandHandler("start", start_communication)],

    allow_reentry=True,

    states={
        RUN_MAIN: [
            MessageHandler(filters.Regex(answers.CANCEL), cancel_communication),
            MAIN_CONVERSATION
        ],

        RUN_REG: [
            MessageHandler(filters.Regex(answers.CANCEL), cancel_communication),
            REGISTRATION_CONVERSATION
        ]
    },

    fallbacks=[
        MessageHandler(filters.TEXT, misunderstand)
    ]
)
