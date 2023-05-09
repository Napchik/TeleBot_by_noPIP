"""
    Description: Contains conversation handler.

    Author: Ivan Maruzhenko
    Version: 0.2
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
    MAIN_INFO,
    CONTROLS,
    start_main,
    schedule,
    game,
    settings,
    main_info,
    controls
)

from Services.schedule_update_conversation import (CHANGE_DAY, send_week_schedule, next_day, previous_day)

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

REGISTRATION_CONVERSATION = ConversationHandler(entry_points=[CommandHandler("start", start)],
                                                states={
                                                    GROUP: [
                                                        MessageHandler(filters.Regex("[A-Za-z]{2}-[0-9]{2}"), group)],

                                                    ROUTINE: [
                                                        MessageHandler(
                                                            filters.Regex(
                                                                f"({answers.REG_NO})|({answers.REG_MORNING})|"
                                                                f"({answers.REG_ALL})"),
                                                            routine)],

                                                    REG_INFO: [
                                                        MessageHandler(filters.Regex("(Зрозуміло)"), info)]},
                                                fallbacks=[
                                                    CommandHandler("cancel", cancel),
                                                    MessageHandler(filters.Regex("(Скасувати)"), cancel),
                                                    MessageHandler(filters.TEXT, misunderstand)])


SCHEDULE_UPDATE_CONVERSATION = ConversationHandler(entry_points=[CommandHandler("week", send_week_schedule)],
                                                   allow_reentry=True, conversation_timeout=60,

                                                   states={
                                                       CHANGE_DAY: [
                                                           CallbackQueryHandler(previous_day, pattern="back"),
                                                           CallbackQueryHandler(next_day, pattern="forward")]},

                                                   fallbacks=[MessageHandler(filters.TEXT, misunderstand)])


MAIN_CONVERSATION = ConversationHandler(entry_points=[CommandHandler("menu", start_main)], allow_reentry=True,
                                        states={

                                            MENU: [
                                                MessageHandler(filters.Regex(f"{answers.MAIN_SCHEDULE}"), schedule),
                                                MessageHandler(filters.Regex(f"{answers.MAIN_GAME}"), game),
                                                MessageHandler(filters.Regex(f"{answers.MAIN_SETTINGS}"), settings),
                                                MessageHandler(filters.Regex(f"{answers.MAIN_INFO}"), main_info),
                                                MessageHandler(filters.Regex(f"{answers.MAIN_CONTROLS}"), controls)],

                                            SCHEDULE: [MessageHandler(filters.Regex(f"{answers.SCHEDULE_TODAY}"),
                                                                      Handlers.today),
                                                       MessageHandler(filters.Regex(f"{answers.SCHEDULE_TOMORROW}"),
                                                                      Handlers.tomorrow)]},

                                        # GAME: [],
                                        #
                                        # SETTINGS: [],
                                        #
                                        # MAIN_INFO: [],
                                        #
                                        # CONTROLS: []},

                                        fallbacks=[
                                            MessageHandler(filters.Regex(f"{answers.BACK}"), start_main),
                                            MessageHandler(filters.TEXT, misunderstand)])
