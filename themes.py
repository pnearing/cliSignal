#!/usr/bin/env python3
from typing import TextIO, Optional
from enum import IntEnum
import curses
import json
import common


class ThemeColours(IntEnum):
    """
    Theme colour pair numbers.
    """
    MAIN_WIN = 1
    MAIN_WIN_BORDER = 2
    MAIN_WIN_FOCUS_BORDER = 3
    MAIN_WIN_TITLE = 4
    MAIN_WIN_FOCUS_TITLE = 5

    CONTACTS_WIN = 6
    CONTACT_WIN_BORDER = 7
    CONTACTS_WIN_FOCUS_BORDER = 8
    CONTACT_WIN_TITLE = 9
    CONTACTS_WIN_FOCUS_TITLE = 10

    MESSAGES_WIN = 11
    MESSAGES_WIN_BORDER = 12
    MESSAGES_WIN_FOCUS_BORDER = 13
    MESSAGES_WIN_TITLE = 14
    MESSAGES_WIN_FOCUS_TITLE = 15

    TYPING_WIN = 16
    TYPING_WIN_BORDER = 17
    TYPING_WIN_FOCUS_BORDER = 18
    TYPING_WIN_TITLE = 19
    TYPING_WIN_FOCUS_TITLE = 20

    MENU_BAR_EMPTY = 21
    STATUS_BAR_EMPTY = 22

    MENU_UNSEL = 23
    MENU_SEL = 24
    MENU_UNSEL_ACCEL = 25
    MENU_SEL_ACCEL = 26

    FILE_MENU_BORDER = 27
    FILE_MENU_SEL = 28
    FILE_MENU_SEL_ACCEL = 29
    FILE_MENU_UNSEL = 30
    FILE_MENU_UNSEL_ACCEL = 31

    ACCOUNTS_MENU_BORDER = 32
    ACCOUNTS_MENU_SEL = 33
    ACCOUNTS_MENU_SEL_ACCEL = 34
    ACCOUNTS_MENU_UNSEL = 35
    ACCOUNTS_MENU_UNSEL_ACCEL = 36

    HELP_MENU_BORDER = 37
    HELP_MENU_SEL = 48
    HELP_MENU_SEL_ACCEL = 39
    HELP_MENU_UNSEL = 40
    HELP_MENU_UNSEL_ACCEL = 41

    SETTINGS_WIN = 42
    SETTINGS_WIN_BORDER = 43
    SETTINGS_WIN_FOCUS_BORDER = 44
    SETTINGS_WIN_TITLE = 45
    SETTINGS_WIN_FOCUS_TITLE = 46

    QUIT_WIN = 47
    QUIT_WIN_BORDER = 48
    QUIT_WIN_FOCUS_BORDER = 49
    QUIT_WIN_TITLE = 50
    QUIT_WIN_FOCUS_TITLE = 51

    SWITCH_WIN = 52
    SWITCH_WIN_BORDER = 53
    SWITCH_WIN_FOCUS_BORDER = 54
    SWITCH_WIN_TITLE = 55
    SWITCH_WIN_FOCUS_TITLE = 56

    LINK_WIN = 57
    LINK_WIN_BORDER = 58
    LINK_WIN_FOCUS_BORDER = 59
    LINK_WIN_TITLE = 60
    LINK_WIN_FOCUS_TITLE = 61

    REGISTER_WIN = 62
    REGISTER_WIN_BORDER = 63
    REGISTER_WIN_FOCUS_BORDER = 64
    REGISTER_WIN_TITLE = 65
    REGISTER_WIN_FOCUS_TITLE = 66

    KEYS_WIN = 67
    KEYS_WIN_BORDER = 68
    KEYS_WIN_FOCUS_BORDER = 69
    KEYS_WIN_TITLE = 70
    KEYS_WIN_FOCUS_TITLE = 71

    ABOUT_WIN = 72
    ABOUT_WIN_BORDER = 73
    ABOUT_WIN_FOCUS_BORDER = 74
    ABOUT_WIN_TITLE = 75
    ABOUT_WIN_FOCUS_TITLE = 76

    VERSION_WIN = 77
    VERSION_WIN_BORDER = 78
    VERSION_WIN_FOCUS_BORDER = 79
    VERSION_WIN_TITLE = 80
    VERSION_FOCUS_TITLE = 81


_THEMES: dict[str, dict[str, dict[str, int | bool | str]]] = {
    # LIGHT THEME:
    'light': {
        # BORDER CHARACTERS:
        # Main window border characters:
        'mainBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                            'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        # Contacts window border characters:
        'contWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        # Messages window border characters:
        'msgsWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        # Typing window border characters:
        'typeWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        # File menu border characters:
        'fileMenuBorderChars': {'ts': '\u2500', 'bs': '\u2500', 'ls': '\u2502', 'rs': '\u2502',  # Sides
                                'tl': '\u250C', 'tr': '\u2510', 'bl': '\u2514', 'br': '\u2518'},  # Corners
        # Accounts menu border characters:
        'acctMenuBorderChars': {'ts': '\u2500', 'bs': '\u2500', 'ls': '\u2502', 'rs': '\u2502',  # Sides
                                'tl': '\u250C', 'tr': '\u2510', 'bl': '\u2514', 'br': '\u2518'},  # Corners
        # Help menu border characters:
        'helpMenuBorderChars': {'ts': '\u2500', 'bs': '\u2500', 'ls': '\u2502', 'rs': '\u2502',  # Sides
                                'tl': '\u250C', 'tr': '\u2510', 'bl': '\u2514', 'br': '\u2518'},  # Corners
        # Settings window border characters.
        'setWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                              'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        # Quit window border characters.
        'quitWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        # Switch account border characters:
        'switchWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                                 'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        # Keyboard shortcuts border characters:
        'keysWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        # About window border characters:
        'aboutWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                                'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        # Version window border characters:
        'verWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                              'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        # Link account window border characters:
        'linkWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        # Register account window border characters:
        'regWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                              'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners

        # TITLE CHARACTERS:
        # Main window Title start and end characters:
        'mainWinTitleChars': {'start': '\u2561', 'end': '\u255E'},
        # Contacts window title start and end characters:
        'contWinTitleChars': {'start': '\u2561', 'end': '\u255E'},
        # Messages window title start and end characters:
        'msgsWinTitleChars': {'start': '\u2561', 'end': '\u255E'},
        # Typing window title start and end characters: NOTE: NOT USED.
        'typeWinTitleChars': {'start': '\u2561', 'end': '\u255E'},
        # Link window title start and end characters:
        'linkWinTitleChars': {'start': '\u2561', 'end': '\u255E'},
        # Register window title start and end characters:
        'regWinTitleChars': {'start': '\u2561', 'end': '\u255E'},

        # MENU SELECTION INDICATOR CHARACTERS:
        # Menu bar selection indicator characters:
        'menuSelChars': {'leadSel': '\u2192', 'leadUnsel': ' ', 'tailSel': '\u2190', 'tailUnsel': ' '},
        # File menu selection indicator characters:
        'fileMenuSelChars': {'leadSel': '\u2192', 'leadUnsel': ' ', 'tailSel': '\u2190', 'tailUnsel': ' '},
        # Accounts menu selection indicator characters:
        'acctMenuSelChars': {'leadSel': '\u2192', 'leadUnsel': ' ', 'tailSel': '\u2190', 'tailUnsel': ' '},
        # Help menu selection indicator characters:
        'helpMenuSelChars': {'leadSel': '\u2192', 'leadUnsel': ' ', 'tailSel': '\u2190', 'tailUnsel': ' '},

        # MAIN WINDOW COLOUR ATTRIBUTES:
        # Main window centre:
        'mainWin': {'fg': 7, 'bg': 18, 'bold': False, 'underline': False, 'reverse': False},
        # Main window border:
        'mainWinBorder': {'fg': 15, 'bg': 18, 'bold': True, 'underline': False, 'reverse': False},
        # Main window focused border NOTE: NOT USED
        'mainWinFBorder': {'fg': 15, 'bg': 18, 'bold': True, 'underline': False, 'reverse': True},
        # Main window title:
        'mainWinTitle': {'fg': 15, 'bg': 18, 'bold': True, 'underline': True, 'reverse': False},
        # Main window focused title:
        'mainWinFTitle': {'fg': 15, 'bg': 19, 'bold': True, 'underline': True, 'reverse': True},

        # CONTACTS WINDOW COLOUR ATTRIBUTES:
        # Contacts window centre:
        'contWin': {'fg': 7, 'bg': 19, 'bold': False, 'underline': False, 'reverse': False},
        # Contacts window border:
        'contWinBorder': {'fg': 15, 'bg': 19, 'bold': True, 'underline': False, 'reverse': False},
        # Contacts window focused border:
        'contWinFBorder': {'fg': 15, 'bg': 19, 'bold': True, 'underline': False, 'reverse': True},
        # Contacts' window title:
        'contWinTitle': {'fg': 15, 'bg': 19, 'bold': True, 'underline': True, 'reverse': False},
        # Contacts window focused title:
        'contWinFTitle': {'fg': 15, 'bg': 19, 'bold': True, 'underline': True, 'reverse': True},

        # MESSAGES WINDOW COLOUR ATTRIBUTES:
        # Messages window centre:
        'msgsWin': {'fg': 7, 'bg': 20, 'bold': False, 'underline': False, 'reverse': False},
        # Messages window border:
        'msgsWinBorder': {'fg': 15, 'bg': 20, 'bold': True, 'underline': False, 'reverse': False},
        # Messages window focused border:
        'msgsWinFBorder': {'fg': 15, 'bg': 20, 'bold': True, 'underline': False, 'reverse': True},
        # Messages window Title:
        'msgsWinTitle': {'fg': 15, 'bg': 20, 'bold': True, 'underline': True, 'reverse': False},
        # Messages window focused title:
        'msgsWinFTitle': {'fg': 15, 'bg': 20, 'bold': True, 'underline': True, 'reverse': True},

        # TYPING WINDOW COLOUR ATTRIBUTES:
        # The typing window centre:
        'typeWin': {'fg': 7, 'bg': 21, 'bold': False, 'underline': False, 'reverse': False},
        # The Typing window border:
        'typeWinBorder': {'fg': 15, 'bg': 21, 'bold': True, 'underline': False, 'reverse': False},
        # The typing window focused border:
        'typeWinFBorder': {'fg': 15, 'bg': 21, 'bold': True, 'underline': False, 'reverse': True},
        # Typing window title:
        'typeWinTitle': {'fg': 15, 'bg': 21, 'bold': True, 'underline': True, 'reverse': False},
        # Typing window focused title:
        'typeWinFTitle': {'fg': 15, 'bg': 21, 'bold': True, 'underline': True, 'reverse': True},

        # SETTINGS WINDOW COLOUR ATTRIBUTES:
        # The settings window centre:
        'setWin': {'fg': 7, 'bg': 21, 'bold': False, 'underline': False, 'reverse': False},
        # The settings window border:
        'setWinBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': False},
        # The settings window focused border:
        'setWinFBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': True},
        # The settings window title:
        'setWinTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': False},
        # The settings window focused title:
        'setWinFTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': True},

        # THE QUIT WINDOW COLOUR ATTRIBUTES:
        # The quit window centre:
        'quitWin': {'fg': 7, 'bg': 21, 'bold': False, 'underline': False, 'reverse': False},
        # The quit window border:
        'quitWinBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': False},
        # The quit window focused border:
        'quitWinFBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': True},
        # The quit window title:
        'quitWinTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': False},
        # The quit window focused title:
        'quitWinFTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': True},

        # THE SWITCH ACCOUNT WINDOW COLOUR ATTRIBUTES:
        # The switch window centre:
        'switchWin': {'fg': 7, 'bg': 21, 'bold': False, 'underline': False, 'reverse': False},
        # The switch window border:
        'switchWinBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': False},
        # The switch window focused border:
        'switchWinFBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': True},
        # The switch window title:
        'switchWinTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': False},
        # The switch window focused title:
        'switchWinFTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': True},

        # THE LINK ACCOUNT WINDOW COLOUR ATTRIBUTES:
        # The link window centre:
        'linkWin': {'fg': 7, 'bg': 21, 'bold': False, 'underline': False, 'reverse': False},
        # The link window border:
        'linkWinBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': False},
        # The link window focused border:
        'linkWinFBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': True},
        # The link window title:
        'linkWinTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': False},
        # The link window focused title:
        'linkWinFTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': True},

        # THE REGISTER NEW ACCOUNT WINDOW COLOUR ATTRIBUTES:
        # The register window centre:
        'regWin': {'fg': 7, 'bg': 21, 'bold': False, 'underline': False, 'reverse': False},
        # The register window border:
        'regWinBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': False},
        # The register window focused border:
        'regWinFBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': True},
        # The register window title:
        'regWinTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': False},
        # The register window focused title:
        'regWinFTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': True},

        # THE SHORTCUT KEYS HELP WINDOW COLOUR ATTRIBUTES:
        # The keys window centre:
        'keysWin': {'fg': 7, 'bg': 21, 'bold': False, 'underline': False, 'reverse': False},
        # The keys window border:
        'keysWinBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': False},
        # The keys window focused border:
        'keysWinFBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': True},
        # The keys window title:
        'keysWinTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': False},
        # The keys window focused title:
        'keysWinFTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': True},

        # THE ABOUT WINDOW COLOUR ATTRIBUTES:
        # The about window centre:
        'aboutWin': {'fg': 7, 'bg': 21, 'bold': False, 'underline': False, 'reverse': False},
        # The about window border:
        'aboutWinBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': False},
        # The about window focused border:
        'aboutWinFBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': True},
        # The about window title:
        'aboutWinTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': False},
        # The about window focused title:
        'aboutWinFTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': True},

        # THE VERSION WINDOW COLOUR ATTRIBUTES:
        # The version window centre:
        'verWin': {'fg': 7, 'bg': 21, 'bold': False, 'underline': False, 'reverse': False},
        # The version window border:
        'verWinBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': False},
        # The version window focused border:
        'verWinFBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': True},
        # The version window title:
        'verWinTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': False},
        # The version window focused title:
        'verWinFTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': True},

        # MENU BAR COLOUR ATTRIBUTES:
        # Menu bar background spaces:
        'menuBG': {'fg': 15, 'bg': 18, 'bold': False, 'underline': False, 'reverse': False},
        # Menu bar item selected:
        'menuSel': {'fg': 15, 'bg': 18, 'bold': True, 'underline': False, 'reverse': False},
        # Menu bar accelerator indicator when selected:
        'menuSelAccel': {'fg': 15, 'bg': 18, 'bold': True, 'underline': True, 'reverse': False},
        # Menu bar item unselected:
        'menuUnsel': {'fg': 15, 'bg': 18, 'bold': False, 'underline': False, 'reverse': False},
        # Menu bar item accelerator indicator when unselected.
        'menuUnselAccel': {'fg': 15, 'bg': 18, 'bold': False, 'underline': True, 'reverse': False},

        # STATUS BAR COLOUR ATTRIBUTES:
        # Status bar background spaces:
        'statusBG': {'fg': 15, 'bg': 18, 'bold': False, 'underline': False, 'reverse': False},

        # FILE MENU COLOUR ATTRIBUTES:
        # File menu border:
        'fileMenuBorder': {'fg': 7, 'bg': 20, 'bold': False, 'underline': False, 'reverse': False},
        # FIle menu selected item:
        'fileMenuSel': {'fg': 7, 'bg': 20, 'bold': False, 'underline': False, 'reverse': True},
        # File menu unselected item:
        'fileMenuUnsel': {'fg': 7, 'bg': 20, 'bold': False, 'underline': False, 'reverse': False},
        # File menu selected accelerator:
        'fileMenuSelAccel': {'fg': 7, 'bg': 20, 'bold': False, 'underline': True, 'reverse': True},
        # File menu unselected accelerator:
        'fileMenuUnselAccel': {'fg': 7, 'bg': 20, 'bold': False, 'underline': True, 'reverse': False},

        # ACCOUNTS MENU COLOUR ATTRIBUTES:
        # Accounts menu border:
        'acctMenuBorder': {'fg': 7, 'bg': 20, 'bold': False, 'underline': False, 'reverse': False},
        # Accounts menu selected item.
        'acctMenuSel': {'fg': 7, 'bg': 20, 'bold': False, 'underline': False, 'reverse': True},
        # Accounts menu unselected item.
        'acctMenuUnsel': {'fg': 7, 'bg': 20, 'bold': False, 'underline': False, 'reverse': False},
        # Accounts menu selected accelerator:
        'acctMenuSelAccel': {'fg': 7, 'bg': 20, 'bold': False, 'underline': True, 'reverse': True},
        # Accounts menu unselected accelerator:
        'acctMenuUnselAccel': {'fg': 7, 'bg': 20, 'bold': False, 'underline': True, 'reverse': False},

        # HELP MENU COLOUR ATTRIBUTES:
        # Help menu border:
        'helpMenuBorder': {'fg': 7, 'bg': 20, 'bold': False, 'underline': False, 'reverse': False},
        # Help menu selected item:
        'helpMenuSel': {'fg': 7, 'bg': 20, 'bold': False, 'underline': False, 'reverse': True},
        # Help menu unselected item:
        'helpMenuUnsel': {'fg': 7, 'bg': 20, 'bold': False, 'underline': False, 'reverse': False},
        # Help menu selected accelerator:
        'helpMenuSelAccel': {'fg': 7, 'bg': 20, 'bold': False, 'underline': True, 'reverse': True},
        # Help menu unselected accelerator:
        'helpMenuUnselAccel': {'fg': 7, 'bg': 20, 'bold': False, 'underline': True, 'reverse': False},
    },
    # DARK THEME:
    'dark': {
        'titles': {'main': 'cliSignal', 'messages': 'Messages', 'contacts': 'Contacts & Groups', 'typing': None},
        'mainBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                            'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'contWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'msgsWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'typeWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'setWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                              'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'quitWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'linkWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'regWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                              'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'switchWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                                 'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'keysWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'aboutWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                                'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'verWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                              'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners

        'fileMenuBorderChars': {'ts': '\u2500', 'bs': '\u2500', 'ls': '\u2502', 'rs': '\u2502',  # Sides
                                'tl': '\u250C', 'tr': '\u2510', 'bl': '\u2514', 'br': '\u2518'},  # Corners
        'acctMenuBorderChars': {'ts': '\u2500', 'bs': '\u2500', 'ls': '\u2502', 'rs': '\u2502',  # Sides
                                'tl': '\u250C', 'tr': '\u2510', 'bl': '\u2514', 'br': '\u2518'},  # Corners
        'helpMenuBorderChars': {'ts': '\u2500', 'bs': '\u2500', 'ls': '\u2502', 'rs': '\u2502',  # Sides
                                'tl': '\u250C', 'tr': '\u2510', 'bl': '\u2514', 'br': '\u2518'},  # Corners
        'mainWinTitleChars': {'start': '\u2561', 'end': '\u255E'},
        'contWinTitleChars': {'start': '\u2561', 'end': '\u255E'},
        'msgsWinTitleChars': {'start': '\u2561', 'end': '\u255E'},
        'typeWinTitleChars': {'start': '\u2561', 'end': '\u255E'},
        'setWinTitleChars': {'start': '\u2561', 'end': '\u255E'},
        'quitWinTitleChars': {'start': '\u2561', 'end': '\u255E'},
        'keysWinTitleChars': {'start': '\u2561', 'end': '\u255E'},
        'aboutWinTitleChars': {'start': '\u2561', 'end': '\u255E'},
        'verWinTitleChars': {'start': '\u2561', 'end': '\u255E'},
        'switchWinTitleChars': {'start': '\u2561', 'end': '\u255E'},
        'linkWinTitleChars': {'start': '\u2561', 'end': '\u255E'},
        'regWinTitleChars': {'start': '\u2561', 'end': '\u255E'},
        'menuSelChars': {'leadSel': '\u2192', 'leadUnsel': ' ', 'tailSel': '\u2190', 'tailUnsel': ' '},
        'fileMenuSelChars': {'leadSel': '\u2192', 'leadUnsel': ' ', 'tailSel': '\u2190', 'tailUnsel': ' '},
        'acctMenuSelChars': {'leadSel': '\u2192', 'leadUnsel': ' ', 'tailSel': '\u2190', 'tailUnsel': ' '},
        'helpMenuSelChars': {'leadSel': '\u2192', 'leadUnsel': ' ', 'tailSel': '\u2190', 'tailUnsel': ' '},
        'mainWin': {'fg': 7, 'bg': 237, 'bold': False, 'underline': False, 'reverse': False},
        'mainWinBorder': {'fg': 7, 'bg': 237, 'bold': True, 'underline': False, 'reverse': False},
        'mainWinFBorder': {'fg': 7, 'bg': 237, 'bold': True, 'underline': False, 'reverse': True},
        'mainWinTitle': {'fg': 7, 'bg': 237, 'bold': True, 'underline': True, 'reverse': False},
        'mainWinFTitle': {'fg': 7, 'bg': 237, 'bold': True, 'underline': True, 'reverse': True},
        'contWin': {'fg': 7, 'bg': 238, 'bold': False, 'underline': False, 'reverse': False},
        'contWinBorder': {'fg': 7, 'bg': 238, 'bold': True, 'underline': False, 'reverse': False},
        'contWinFBorder': {'fg': 7, 'bg': 238, 'bold': True, 'underline': False, 'reverse': True},
        'contWinTitle': {'fg': 7, 'bg': 238, 'bold': True, 'underline': True, 'reverse': False},
        'contWinFTitle': {'fg': 7, 'bg': 238, 'bold': True, 'underline': True, 'reverse': True},
        'contNameUnsel': {'fg': 7, 'bg': 238, 'bold': False, 'underline': False, 'reverse': False},
        'contNameSel': {'fg': 7, 'bg': 238, 'bold': False, 'underline': True, 'reverse': True},
        'msgsWin': {'fg': 7, 'bg': 239, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinBorder': {'fg': 7, 'bg': 239, 'bold': True, 'underline': False, 'reverse': False},
        'msgsWinFBorder': {'fg': 7, 'bg': 239, 'bold': True, 'underline': False, 'reverse': True},
        'msgsWinTitle': {'fg': 7, 'bg': 239, 'bold': True, 'underline': True, 'reverse': False},
        'msgsWinFTitle': {'fg': 7, 'bg': 239, 'bold': True, 'underline': True, 'reverse': True},
        'typeWin': {'fg': 7, 'bg': 240, 'bold': False, 'underline': False, 'reverse': False},
        'typeWinBorder': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': False},
        'typeWinFBorder': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': True},
        'typeWinTitle': {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': False},
        'typeWinFTitle': {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': True},
        'setWin': {'fg': 7, 'bg': 240, 'bold': False, 'underline': False, 'reverse': False},
        'setWinBorder': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': False},
        'setWinFBorder': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': True},
        'setWinTitle': {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': False},
        'setWinFTitle': {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': True},
        'quitWin': {'fg': 7, 'bg': 240, 'bold': False, 'underline': False, 'reverse': False},
        'quitWinBorder': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': False},
        'quitWinFBorder': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': True},
        'quitWinTitle': {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': False},
        'quitWinFTitle': {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': True},
        'switchWin': {'fg': 7, 'bg': 240, 'bold': False, 'underline': False, 'reverse': False},
        'switchWinBorder': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': False},
        'switchWinFBorder': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': True},
        'switchWinTitle': {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': False},
        'switchWinFTitle': {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': True},
        'linkWin': {'fg': 7, 'bg': 240, 'bold': False, 'underline': False, 'reverse': False},
        'linkWinBorder': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': False},
        'linkWinFBorder': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': True},
        'linkWinTitle': {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': False},
        'linkWinFTitle': {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': True},
        'regWin': {'fg': 7, 'bg': 240, 'bold': False, 'underline': False, 'reverse': False},
        'regWinBorder': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': False},
        'regWinFBorder': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': True},
        'regWinTitle': {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': False},
        'regWinFTitle': {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': True},
        'keysWin': {'fg': 7, 'bg': 240, 'bold': False, 'underline': False, 'reverse': False},
        'keysWinBorder': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': False},
        'keysWinFBorder': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': True},
        'keysWinTitle': {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': False},
        'keysWinFTitle': {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': True},
        'aboutWin': {'fg': 7, 'bg': 240, 'bold': False, 'underline': False, 'reverse': False},
        'aboutWinBorder': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': False},
        'aboutWinFBorder': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': True},
        'aboutWinTitle': {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': False},
        'aboutWinFTitle': {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': True},
        'verWin': {'fg': 7, 'bg': 240, 'bold': False, 'underline': False, 'reverse': False},
        'verWinBorder': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': False},
        'verWinFBorder': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': True},
        'verWinTitle': {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': False},
        'verWinFTitle': {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': True},
        'menuBG': {'fg': 7, 'bg': 236, 'bold': False, 'underline': False, 'reverse': False},
        'menuSel': {'fg': 7, 'bg': 0, 'bold': True, 'underline': False, 'reverse': True},
        'menuSelAccel': {'fg': 7, 'bg': 0, 'bold': True, 'underline': True, 'reverse': True},
        'menuUnsel': {'fg': 7, 'bg': 0, 'bold': False, 'underline': False, 'reverse': False},
        'menuUnselAccel': {'fg': 7, 'bg': 0, 'bold': False, 'underline': True, 'reverse': False},
        'statusBG': {'fg': 7, 'bg': 0, 'bold': False, 'underline': False, 'reverse': False},
        'fileMenuBorder': {'fg': 7, 'bg': 237, 'bold': False, 'underline': False, 'reverse': False},
        'fileMenuSel': {'fg': 7, 'bg': 237, 'bold': True, 'underline': False, 'reverse': True},
        'fileMenuUnsel': {'fg': 7, 'bg': 237, 'bold': False, 'underline': False, 'reverse': False},
        'fileMenuSelAccel': {'fg': 7, 'bg': 237, 'bold': False, 'underline': True, 'reverse': True},
        'fileMenuUnselAccel': {'fg': 7, 'bg': 237, 'bold': False, 'underline': True, 'reverse': False},
        'acctMenuBorder': {'fg': 7, 'bg': 237, 'bold': False, 'underline': False, 'reverse': False},
        'acctMenuSel': {'fg': 7, 'bg': 237, 'bold': False, 'underline': False, 'reverse': True},
        'acctMenuUnsel': {'fg': 7, 'bg': 237, 'bold': False, 'underline': False, 'reverse': False},
        'acctMenuSelAccel': {'fg': 7, 'bg': 237, 'bold': False, 'underline': True, 'reverse': True},
        'acctMenuUnselAccel': {'fg': 7, 'bg': 237, 'bold': False, 'underline': True, 'reverse': False},
        'helpMenuBorder': {'fg': 7, 'bg': 237, 'bold': False, 'underline': False, 'reverse': False},
        'helpMenuSel': {'fg': 7, 'bg': 237, 'bold': False, 'underline': False, 'reverse': True},
        'helpMenuUnsel': {'fg': 7, 'bg': 237, 'bold': False, 'underline': False, 'reverse': False},
        'helpMenuSelAccel': {'fg': 7, 'bg': 237, 'bold': False, 'underline': True, 'reverse': True},
        'helpMenuUnselAccel': {'fg': 7, 'bg': 237, 'bold': False, 'underline': True, 'reverse': False},
    }
}
"""Light and dark theme definitions."""

# Primary Keys:
_ATTRIBUTE_PRIMARY_KEYS: list[str] = ['mainWin', 'mainWinBorder', 'mainWinTitle', 'contWin', 'contWinBorder',
                                      'contWinTitle', 'msgsWin', 'msgsWinBorder', 'msgsWinTitle', 'typeWin',
                                      'typeWinBorder', 'typeWinTitle', 'contNameUnsel', 'contNameSel',
                                      'mainWinFBorder', 'msgsWinFBorder', 'contWinFBorder', 'typeWinFBorder',
                                      'mainWinFTitle', 'contWinFTitle', 'msgsWinFTitle', 'typeWinFTitle',
                                      'menuBG', 'statusBG', 'menuSel', 'menuSelAccel', 'menuUnsel', 'menuUnselAccel',
                                      'fileMenuBorder', 'acctMenuBorder', 'helpMenuBorder', 'setWin', 'setWinBorder',
                                      'setWinFBorder', 'setWinTitle', 'setWinFTitle', 'quitWin', 'quitWinBorder',
                                      'quitWinFBorder', 'quitWinTitle', 'quitWinFTitle', 'switchWin', 'switchWinBorder',
                                      'switchWinFBorder', 'switchWinTitle', 'switchWinFTitle', 'linkWin',
                                      'linkWinBorder', 'linkWinFBorder', 'linkWinTitle', 'linkWinFTitle', 'regWin',
                                      'regWinBorder', 'regWinFBorder', 'regWinTitle', 'regWinFTitle', 'keysWin',
                                      'keysWinBorder', 'keysWinFBorder', 'keysWinTitle', 'keysWinTitle', 'aboutWin',
                                      'aboutWinBorder', 'aboutWinFBorder', 'aboutWinTitle', 'aboutWinFTitle', 'verWin',
                                      'verWinBorder', 'verWinFBorder', 'verWinTitle', 'verWinFTitle',
                                      ]
"""Primary attribute theme keys."""
# 'keysWin': {'fg': 7, 'bg': 240, 'bold': False, 'underline': False, 'reverse': False},
# 'keysWinBorder': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': False},
# 'keysWinFBorder': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': True},
# 'keysWinTitle': {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': False},
# 'keysWinFTitle': {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': True},
# 'aboutWin': {'fg': 7, 'bg': 240, 'bold': False, 'underline': False, 'reverse': False},
# 'aboutWinBorder': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': False},
# 'aboutWinFBorder': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': True},
# 'aboutWinTitle': {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': False},
# 'aboutWinFTitle': {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': True},
# 'verWin': {'fg': 7, 'bg': 240, 'bold': False, 'underline': False, 'reverse': False},
# 'verWinBorder': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': False},
# 'verWinFBorder': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': True},
# 'verWinTitle': {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': False},
# 'verWinFTitle': {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': True},

_TITLE_CHAR_PRIMARY_KEYS: list[str] = ['mainWinTitleChars', 'contWinTitleChars', 'msgsWinTitleChars',
                                       'typeWinTitleChars', 'setWinTitleChars', 'quitWinTitleChars',
                                       'keysWinTitleChars', 'aboutWinTitleChars', 'verWinTitleChars',
                                       'switchWinTitleChars', 'linkWinTitleChars', 'regWinTitleChars',
                                       ]
"""Title characters primary keys."""
_MENU_SEL_PRIMARY_KEYS: list[str] = ['menuSelChars', 'fileMenuSelChars', 'acctMenuSelChars', 'helpMenuSelChars']
"""Menu selection primary keys."""

_BORDER_PRIMARY_KEYS: list[str] = ['mainBorderChars', 'contWinBorderChars', 'msgsWinBorderChars', 'typeWinBorderChars',
                                   'fileMenuBorderChars', 'acctMenuBorderChars', 'helpMenuBorderChars',
                                   'setWinBorderChars', 'quitWinBorderChars', 'switchWinBorderChars',
                                   'keysWinBorderChars', 'verWinBorderChars', 'linkWinBorderChars', 'regWinBorderChars',
                                   ]
"""Keys with border strings."""

# Sub keys:
_ATTR_KEYS: list[str] = ['fg', 'bg', 'bold', 'underline', 'reverse']
"""Attribute keys."""
_BORDER_CHAR_KEYS: list[str] = ['ts', 'bs', 'ls', 'rs', 'tl', 'tr', 'bl', 'br']
"""Border character keys."""
_TITLE_CHAR_KEYS: list[str] = ['start', 'end']
"""Title character keys."""
_MENU_SEL_CHAR_KEYS: list[str] = ['leadSel', 'leadUnsel', 'tailSel', 'tailUnsel']
"""Menu selection indicator character keys."""


def verify_theme(theme: dict[str, dict[str, int | bool | str]]) -> tuple[bool, str]:
    """
    Verify a theme dict is correct, has the right keys, and values.
    :param theme: The theme to check.
    :return: bool: True if this theme passes the test, False if not.
    """
    # Colour / font attribute keys:
    for main_key in _ATTRIBUTE_PRIMARY_KEYS:
        if main_key not in theme.keys():
            return False, "Primary key '%s' doesn't exist." % main_key
        for attr_key in _ATTR_KEYS:
            if attr_key not in theme[main_key].keys():
                return False, "Key '%s' missing from '%s'." % (attr_key, main_key)
            elif attr_key in ('fg', 'bg'):
                if theme[main_key][attr_key] < 0 or theme[main_key][attr_key] >= curses.COLORS:
                    return False, "Value at ['%s']['%s'] out of range 0 -> %i." % (main_key, attr_key, curses.COLORS)

    # Border character keys:
    for border_key in _BORDER_PRIMARY_KEYS:
        if border_key not in theme.keys():
            return False, "Primary key '%s' doesn't exist." % border_key
        for border_char_key in _BORDER_CHAR_KEYS:
            if border_char_key not in theme[border_key].keys():
                return False, "Key '%s' missing from '%s'." % (border_char_key, border_key)

    # Menu selection character keys:
    for menu_sel_primary_key in _MENU_SEL_PRIMARY_KEYS:
        if menu_sel_primary_key not in theme.keys():
            return False, "Primary key '%s' doesn't exist." % menu_sel_primary_key
        for menu_sel_key in _MENU_SEL_CHAR_KEYS:
            if menu_sel_key not in theme[menu_sel_primary_key].keys():
                return False, "Key '%s' missing from '%s'." % (menu_sel_key, menu_sel_primary_key)

    # Title character keys:
    for title_char_primary_key in _TITLE_CHAR_PRIMARY_KEYS:
        if title_char_primary_key not in theme.keys():
            return False, "Primary key '%s' doesn't exist." % title_char_primary_key
        for title_char_key in _TITLE_CHAR_KEYS:
            if title_char_key not in theme[title_char_primary_key].keys():
                return False, "Key '%s' missing from '%s'." % (title_char_key, title_char_primary_key)

    # Everything is good:
    return True, 'PASS'


def load_theme() -> dict[str, dict[str, int | bool | str]]:
    """
    Load the current theme.
    :return: dict[str, dict[str, int | bool]]:
    """
    theme: dict[str, dict[str, int | bool | str]]
    if common.SETTINGS['theme'] == 'light':
        theme = _THEMES['light']
    elif common.SETTINGS['theme'] == 'dark':
        theme = _THEMES['dark']
    elif common.SETTINGS['theme'] == 'custom':
        try:
            file_handle: TextIO = open(common.SETTINGS['themePath'], 'r')
            theme = json.loads(file_handle.read())
            file_handle.close()
        except (OSError, FileNotFoundError, PermissionError) as e:
            raise RuntimeError("Failed to open '%s' for reading: %s" % (common.SETTINGS['themePath'], str(e.args)))
        except json.JSONDecodeError as e:
            raise RuntimeError("Failed to load JSON from '%s': %s" % (common.SETTINGS['themePath'], e.msg))
    else:
        raise RuntimeError("Invalid theme: '%s' is not 'light', 'dark', or 'custom'.")
    # Verify the theme:
    result, message = verify_theme(theme)
    if result:
        return theme
    raise RuntimeError("Invalid theme: %s." % message)


def init_colours(theme: dict[str, dict[str, int | bool | Optional[str]]]) -> None:
    """
    Initialize the colour pairs:
    :param theme: The colour theme dict.
    :return: None
    """
    curses.init_pair(ThemeColours.MAIN_WIN, theme['mainWin']['fg'], theme['mainWin']['bg'])
    curses.init_pair(ThemeColours.MAIN_WIN_BORDER, theme['mainWinBorder']['fg'], theme['mainWinBorder']['bg'])
    curses.init_pair(ThemeColours.MAIN_WIN_TITLE, theme['mainWinTitle']['fg'], theme['mainWinTitle']['bg'])
    curses.init_pair(ThemeColours.CONTACTS_WIN, theme['contWin']['fg'], theme['contWin']['bg'])
    curses.init_pair(ThemeColours.CONTACT_WIN_BORDER, theme['contWinBorder']['fg'], theme['contWinBorder']['bg'])
    curses.init_pair(ThemeColours.CONTACT_WIN_TITLE, theme['contWinTitle']['fg'], theme['contWinTitle']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN, theme['msgsWin']['fg'], theme['msgsWin']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_BORDER, theme['msgsWinBorder']['fg'], theme['msgsWinBorder']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_TITLE, theme['msgsWinTitle']['fg'], theme['msgsWinTitle']['bg'])
    curses.init_pair(ThemeColours.TYPING_WIN, theme['typeWin']['fg'], theme['typeWin']['bg'])
    curses.init_pair(ThemeColours.TYPING_WIN_BORDER, theme['typeWinBorder']['fg'], theme['typeWinBorder']['bg'])
    curses.init_pair(ThemeColours.TYPING_WIN_TITLE, theme['typeWinTitle']['fg'], theme['typeWinTitle']['bg'])
    curses.init_pair(ThemeColours.MAIN_WIN_FOCUS_BORDER, theme['mainWinFBorder']['fg'],
                     theme['mainWinFBorder']['bg'])
    curses.init_pair(ThemeColours.CONTACTS_WIN_FOCUS_BORDER, theme['contWinFBorder']['fg'],
                     theme['contWinFBorder']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_FOCUS_BORDER, theme['msgsWinFBorder']['fg'],
                     theme['msgsWinFBorder']['bg'])
    curses.init_pair(ThemeColours.TYPING_WIN_FOCUS_BORDER, theme['typeWinFBorder']['fg'],
                     theme['typeWinFBorder']['bg'])
    curses.init_pair(ThemeColours.MAIN_WIN_FOCUS_TITLE, theme['mainWinFTitle']['fg'],
                     theme['mainWinFTitle']['bg'])
    curses.init_pair(ThemeColours.CONTACTS_WIN_FOCUS_TITLE, theme['contWinFTitle']['fg'],
                     theme['contWinFTitle']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_FOCUS_TITLE, theme['msgsWinFTitle']['fg'],
                     theme['msgsWinFTitle']['bg'])
    curses.init_pair(ThemeColours.TYPING_WIN_FOCUS_TITLE, theme['typeWinFTitle']['fg'],
                     theme['typeWinFTitle']['bg'])
    curses.init_pair(ThemeColours.MENU_BAR_EMPTY, theme['menuBG']['fg'], theme['menuBG']['bg'])
    curses.init_pair(ThemeColours.STATUS_BAR_EMPTY, theme['statusBG']['fg'], theme['statusBG']['bg'])
    curses.init_pair(ThemeColours.MENU_SEL, theme['menuSel']['fg'], theme['menuSel']['bg'])
    curses.init_pair(ThemeColours.MENU_SEL_ACCEL, theme['menuSelAccel']['fg'], theme['menuSelAccel']['bg'])
    curses.init_pair(ThemeColours.MENU_UNSEL, theme['menuUnsel']['fg'], theme['menuUnsel']['bg'])
    curses.init_pair(ThemeColours.MENU_UNSEL_ACCEL, theme['menuUnselAccel']['fg'], theme['menuUnselAccel']['bg'])
    curses.init_pair(ThemeColours.FILE_MENU_BORDER, theme['fileMenuBorder']['fg'], theme['fileMenuBorder']['bg'])
    curses.init_pair(ThemeColours.FILE_MENU_SEL, theme['fileMenuSel']['fg'], theme['fileMenuSel']['bg'])
    curses.init_pair(ThemeColours.FILE_MENU_UNSEL, theme['fileMenuUnsel']['fg'], theme['fileMenuUnsel']['bg'])
    curses.init_pair(ThemeColours.ACCOUNTS_MENU_BORDER, theme['acctMenuBorder']['fg'], theme['acctMenuBorder']['bg'])
    curses.init_pair(ThemeColours.ACCOUNTS_MENU_SEL, theme['acctMenuSel']['fg'], theme['acctMenuSel']['bg'])
    curses.init_pair(ThemeColours.ACCOUNTS_MENU_UNSEL, theme['acctMenuUnsel']['fg'], theme['acctMenuUnsel']['bg'])
    curses.init_pair(ThemeColours.HELP_MENU_BORDER, theme['helpMenuBorder']['fg'], theme['helpMenuBorder']['bg'])
    curses.init_pair(ThemeColours.HELP_MENU_SEL, theme['helpMenuSel']['fg'], theme['helpMenuUnsel']['bg'])
    curses.init_pair(ThemeColours.HELP_MENU_UNSEL, theme['helpMenuUnsel']['fg'], theme['helpMenuUnsel']['bg'])
    curses.init_pair(ThemeColours.FILE_MENU_SEL_ACCEL, theme['fileMenuSelAccel']['fg'], theme['fileMenuSelAccel']['bg'])
    curses.init_pair(ThemeColours.FILE_MENU_UNSEL_ACCEL, theme['fileMenuUnselAccel']['fg'],
                     theme['fileMenuUnselAccel']['bg'])
    curses.init_pair(ThemeColours.ACCOUNTS_MENU_SEL_ACCEL, theme['acctMenuSelAccel']['fg'],
                     theme['acctMenuSelAccel']['bg'])
    curses.init_pair(ThemeColours.ACCOUNTS_MENU_UNSEL_ACCEL, theme['acctMenuUnselAccel']['fg'],
                     theme['acctMenuUnselAccel']['bg'])
    curses.init_pair(ThemeColours.HELP_MENU_SEL_ACCEL, theme['helpMenuSelAccel']['fg'], theme['helpMenuSelAccel']['bg'])
    curses.init_pair(ThemeColours.HELP_MENU_UNSEL_ACCEL, theme['helpMenuUnselAccel']['fg'],
                     theme['helpMenuUnselAccel']['bg'])
    curses.init_pair(ThemeColours.SETTINGS_WIN, theme['setWin']['fg'], theme['setWin']['bg'])
    curses.init_pair(ThemeColours.SETTINGS_WIN_BORDER, theme['setWinBorder']['fg'], theme['setWinBorder']['bg'])
    curses.init_pair(ThemeColours.SETTINGS_WIN_FOCUS_BORDER, theme['setWinFBorder']['fg'], theme['setWinFBorder']['bg'])
    curses.init_pair(ThemeColours.SETTINGS_WIN_TITLE, theme['setWinTitle']['fg'], theme['setWinTitle']['bg'])
    curses.init_pair(ThemeColours.SETTINGS_WIN_FOCUS_TITLE, theme['setWinFTitle']['fg'], theme['setWinFTitle']['bg'])
    curses.init_pair(ThemeColours.QUIT_WIN, theme['quitWin']['fg'], theme['quitWin']['bg'])
    curses.init_pair(ThemeColours.QUIT_WIN_BORDER, theme['quitWinBorder']['fg'], theme['quitWinBorder']['bg'])
    curses.init_pair(ThemeColours.QUIT_WIN_FOCUS_BORDER, theme['quitWinFBorder']['fg'], theme['quitWinFBorder']['bg'])
    curses.init_pair(ThemeColours.QUIT_WIN_TITLE, theme['quitWinTitle']['fg'], theme['quitWinTitle']['bg'])
    curses.init_pair(ThemeColours.QUIT_WIN_FOCUS_TITLE, theme['quitWinFTitle']['fg'], theme['quitWinFTitle']['bg'])
    curses.init_pair(ThemeColours.SWITCH_WIN, theme['switchWin']['fg'], theme['switchWin']['bg'])
    curses.init_pair(ThemeColours.SWITCH_WIN_BORDER, theme['switchWinBorder']['fg'], theme['switchWinBorder']['bg'])
    curses.init_pair(ThemeColours.SWITCH_WIN_FOCUS_BORDER, theme['switchWinFBorder']['fg'],
                     theme['switchWinFBorder']['bg'])
    curses.init_pair(ThemeColours.SWITCH_WIN_TITLE, theme['switchWinTitle']['fg'], theme['switchWinTitle']['bg'])
    curses.init_pair(ThemeColours.SWITCH_WIN_FOCUS_TITLE, theme['switchWinFTitle']['fg'],
                     theme['switchWinFTitle']['bg'])
    curses.init_pair(ThemeColours.LINK_WIN, theme['linkWin']['fg'], theme['linkWin']['bg'])
    curses.init_pair(ThemeColours.LINK_WIN_BORDER, theme['linkWinBorder']['fg'], theme['linkWin']['bg'])
    curses.init_pair(ThemeColours.LINK_WIN_FOCUS_BORDER, theme['linkWinFBorder']['fg'], theme['linkWinFBorder']['bg'])
    curses.init_pair(ThemeColours.LINK_WIN_TITLE, theme['linkWinTitle']['fg'], theme['linkWinTitle']['bg'])
    curses.init_pair(ThemeColours.LINK_WIN_FOCUS_TITLE, theme['linkWinFTitle']['fg'], theme['linkWinFTitle']['bg'])
    curses.init_pair(ThemeColours.REGISTER_WIN, theme['regWin']['fg'], theme['regWin']['bg'])
    curses.init_pair(ThemeColours.REGISTER_WIN_BORDER, theme['regWinBorder']['fg'], theme['regWinBorder']['bg'])
    curses.init_pair(ThemeColours.REGISTER_WIN_FOCUS_BORDER, theme['regWinFBorder']['fg'], theme['regWinFBorder']['bg'])
    curses.init_pair(ThemeColours.REGISTER_WIN_TITLE, theme['regWinTitle']['fg'], theme['regWinTitle']['bg'])
    curses.init_pair(ThemeColours.REGISTER_WIN_FOCUS_TITLE, theme['regWinFTitle']['fg'], theme['regWinFTitle']['bg'])
    curses.init_pair(ThemeColours.KEYS_WIN, theme['keysWin']['fg'], theme['keysWin']['bg'])
    curses.init_pair(ThemeColours.KEYS_WIN_BORDER, theme['keysWinBorder']['fg'], theme['keysWinBorder']['bg'])
    curses.init_pair(ThemeColours.KEYS_WIN_FOCUS_BORDER, theme['keysWinFBorder']['fg'], theme['keysWinFBorder']['bg'])
    curses.init_pair(ThemeColours.KEYS_WIN_TITLE, theme['keysWinTitle']['fg'], theme['keysWinTitle']['bg'])
    curses.init_pair(ThemeColours.KEYS_WIN_FOCUS_TITLE, theme['keysWinFTitle']['fg'], theme['keysWinFTitle']['bg'])
    curses.init_pair(ThemeColours.ABOUT_WIN, theme['aboutWin']['fg'], theme['aboutWin']['bg'])
    curses.init_pair(ThemeColours.ABOUT_WIN_BORDER, theme['aboutWinBorder']['fg'], theme['aboutWinBorder']['bg'])
    curses.init_pair(ThemeColours.ABOUT_WIN_FOCUS_BORDER, theme['aboutWinFBorder']['fg'],
                     theme['aboutWinFBorder']['bg'])
    curses.init_pair(ThemeColours.ABOUT_WIN_TITLE, theme['aboutWinTitle']['fg'], theme['aboutWinTitle']['bg'])
    curses.init_pair(ThemeColours.ABOUT_WIN_FOCUS_TITLE, theme['aboutWinFTitle']['fg'], theme['aboutWinFTitle']['bg'])
    curses.init_pair(ThemeColours.VERSION_WIN, theme['verWin']['fg'], theme['verWin']['bg'])
    curses.init_pair(ThemeColours.VERSION_WIN_BORDER, theme['verWinBorder']['fg'], theme['verWinBorder']['bg'])
    curses.init_pair(ThemeColours.VERSION_WIN_TITLE, theme['verWinTitle']['fg'], theme['verWinTitle']['bg'])
    curses.init_pair(ThemeColours.VERSION_FOCUS_TITLE, theme['verWinFTitle']['fg'], theme['verWinFTitle']['bg'])
    return

