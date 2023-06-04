"""
    Description: This file contains all conversation states.

    Author: Ivan Skorobagatko
    Version: 1.0
"""

(
    # Start
    RUN_REG,
    RUN_MAIN,

    # Registration
    GROUP,
    ROUTINE,
    REG_INFO,
    REG_EXIT,

    # Main
    MENU,
    SCHEDULE,
    GAME,
    SETTINGS,
    CONTROLS,

    # Game
    ADD_PLAYER,
    CHANGE_NAME,
    DICE,

    # Schedule Daily
    TODAY_SCHEDULE,
    TOMORROW_SCHEDULE,

    # Schedule Weekly
    WEEK_SCHEDULE,
    ALL_SCHEDULE,

    # Settings
    CHANGE_TIME,
    CHANGE_GROUP,
    SEND_BUG,

    # Controls
    CONTROLS_CHOOSE_LESSON,
    CONTROLS_UPDATE_LINK,
    CHECK_CORRECT,
    CONTROLS_CHOOSE_USER,
    CHECK_ROLE_CORRECT,

    # Routine
    TODAY_LINKS,
    TOMORROW_LINKS

) = map(chr, range(0, 28))
