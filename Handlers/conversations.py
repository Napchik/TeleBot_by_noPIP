"""
    Description: Contains conversation handler.

    Author: Ivan Maruzhenko
    Version: 0.1
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
    SCHEDULE,
    GAME,
    SETTINGS,
    MAIN_INFO,
    CONTROLS,
    main,
    schedule,
    game,
    settings,
    main_info,
    controls
)

from Services.messages import RoutineChoice

from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    CommandHandler,
    filters
)

answers = RoutineChoice.Answers

REGISTRATION_CONVERSATION = ConversationHandler(entry_points=[CommandHandler("start", start)],
                                                states={
                                                    GROUP: [
                                                        MessageHandler(filters.Regex("[A-Za-z]{2}-[0-9]{2}"), group)],

                                                    ROUTINE: [
                                                        MessageHandler(
                                                            filters.Regex(
                                                                f"({answers.REG_NO})|({answers.REG_MORNING})|({answers.REG_ALL})"),
                                                            routine)],

                                                    REG_INFO: [
                                                        MessageHandler(filters.Regex("(Зрозуміло)"), info)]},
                                                fallbacks=[
                                                    CommandHandler("cancel", cancel),
                                                    MessageHandler(filters.Regex("(Скасувати)"), cancel),
                                                    MessageHandler(filters.TEXT, misunderstand)])

MAIN_CONVERSATION = ConversationHandler(entry_points=[CommandHandler("menu", main)],
                                        states={
                                            SCHEDULE: [
                                                MessageHandler(filters.Regex(f"{answers.MAIN_SCHEDULE}"), schedule)],

                                            GAME: [
                                                MessageHandler(filters.Regex(f"{answers.MAIN_GAME}"), game)],

                                            SETTINGS: [
                                                MessageHandler(filters.Regex(f"{answers.MAIN_SETTINGS}"), settings)],

                                            MAIN_INFO: [
                                                MessageHandler(filters.Regex(f"{answers.MAIN_INFO}"), main_info)],

                                            CONTROLS: [
                                                MessageHandler(filters.Regex(f"{answers.MAIN_CONTROLS}"), controls)]},

                                        fallbacks=[
                                            MessageHandler(filters.TEXT, misunderstand)])
