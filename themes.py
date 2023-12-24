#!/usr/bin/env python3
"""
File: themes.py
-> Store theme information and functions.
"""
from typing import TextIO, Optional
from enum import IntEnum, auto
import curses
import json
import common


class ThemeColours(IntEnum):
    """
    Theme colour pair numbers.
    """
    # TODO: Clean up unused colours.
    # Main window:
    MAIN_WIN = auto()
    """Main window text / background."""
    MAIN_WIN_BORDER = auto()
    """Main window unfocused border."""
    MAIN_WIN_FOCUS_BORDER = auto()
    """Main window focused border."""
    MAIN_WIN_TITLE = auto()
    """Main window title."""
    MAIN_WIN_FOCUS_TITLE = auto()
    """Main window focused title."""
    MAIN_WIN_ERROR_TEXT = auto()
    """Main window error message text."""

    CONTACTS_WIN = auto()
    """Contacts window background."""
    CONTACT_WIN_BORDER = auto()
    """Contacts window border."""
    CONTACTS_WIN_FOCUS_BORDER = auto()
    """Contact window focused border."""
    CONTACT_WIN_TITLE = auto()
    """Contacts window title."""
    CONTACTS_WIN_FOCUS_TITLE = auto()
    """Contact window focused title."""
    CONTACTS_WIN_CONT_BORDER = auto()
    """Contacts window contacts sub window border."""
    CONTACTS_WIN_CONT_F_BORDER = auto()
    """Contact window, contact sub window focused border."""
    CONTACTS_WIN_CONT_TITLE = auto()
    """Contacts window contacts sub window title."""
    CONTACTS_WIN_CONT_F_TITLE = auto()
    """Contact window contacts sub window focused title."""
    CONTACTS_WIN_GRPS_BORDER = auto()
    """Contacts window groups sub window border."""
    CONTACTS_WIN_GRPS_F_BORDER = auto()
    """Contact window groups sub window focused border."""
    CONTACTS_WIN_GRPS_TITLE = auto()
    """Contacts window groups sub window title."""
    CONTACTS_WIN_GRPS_F_TITLE = auto()
    """Contacts window groups sub window focused title."""
    CONTACTS_WIN_SEL_CONT = auto()
    """Contacts window, selected contact."""
    CONTACTS_WIN_UNSEL_CONT = auto()
    """Contacts window, unselected contact."""
    CONTACTS_WIN_SEL_GRP = auto()
    """Contacts window, selected group."""
    CONTACTS_WIN_UNSEL_GRP = auto()
    """Contacts window unselected group."""

    MESSAGES_WIN = auto()
    """Messages window background."""
    MESSAGES_WIN_BORDER = auto()
    """Messages window border."""
    MESSAGES_WIN_FOCUS_BORDER = auto()
    """Messages window focused border."""
    MESSAGES_WIN_TITLE = auto()
    """Messages window title."""
    MESSAGES_WIN_FOCUS_TITLE = auto()
    """Messages window focused title."""

    MESSAGES_WIN_SENT_MSG_BG = auto()
    MESSAGES_WIN_SENT_SEL_MSG_BG = auto()
    MESSAGES_WIN_RECV_MSG_BG = auto()
    MESSAGES_WIN_RECV_SEL_MGS_BG = auto()

    MESSAGES_WIN_SENT_TEXT = auto()
    """Messages window, sent message text"""
    MESSAGES_WIN_SENT_SEL_TEXT = auto()
    """Messages window sent message selected text"""
    MESSAGES_WIN_RECV_TEXT = auto()
    """Messages window, received message unselected text."""
    MESSAGES_WIN_RECV_SEL_TEXT = auto()
    """Messages window, received message selected text."""
    MESSAGES_WIN_SENT_BORDER = auto()
    """Messages window, sent message border."""
    MESSAGES_WIN_SENT_SEL_BORDER = auto()
    """Messages window, sent message selected border."""
    MESSAGES_WIN_RECV_BORDER = auto()
    """Messages window, received message border."""
    MESSAGES_WIN_RECV_SEL_BORDER = auto()
    """Messages window, received message selected border."""
    MESSAGES_WIN_SENT_TIME = auto()
    """Messages window, sent time and date."""
    MESSAGES_WIN_SENT_SEL_TIME = auto()
    """Messages window, sent selected time and date."""
    MESSAGES_WIN_RECV_TIME = auto()
    """Messages window, received time and date."""
    MESSAGES_WIN_RECV_SEL_TIME = auto()
    """Messages window, received selected time and date."""
    MESSAGES_WIN_SENT_INDICATOR = auto()
    """Messages window, sent unselected indicator."""
    MESSAGES_WIN_SENT_SEL_INDICATOR = auto()
    """Messages window, sent selected indicator."""
    MESSAGES_WIN_RECV_INDICATOR = auto()
    """Messages window, received unselected indicator."""
    MESSAGES_WIN_RECV_SEL_INDICATOR = auto()
    """Messages window, received selected indicator."""

    MESSAGES_WIN_SENT_STICKER_LABEL = auto()
    MESSAGES_WIN_SENT_SEL_STICKER_LABEL = auto()
    MESSAGES_WIN_RECV_STICKER_LABEL = auto()
    MESSAGES_WIN_RECV_SEL_STICKER_LABEL = auto()

    MESSAGES_WIN_SENT_STICKER_VALUE = auto()
    MESSAGES_WIN_SENT_SEL_STICKER_VALUE = auto()
    MESSAGES_WIN_RECV_STICKER_VALUE = auto()
    MESSAGES_WIN_RECV_SEL_STICKER_VALUE = auto()

    MESSAGES_WIN_SENT_ATTACH_LABEL = auto()
    MESSAGES_WIN_SENT_SEL_ATTACH_LABEL = auto()
    MESSAGES_WIN_RECV_ATTACH_LABEL = auto()
    MESSAGES_WIN_RECV_SEL_ATTACH_LABEL = auto()

    MESSAGES_WIN_SENT_ATTACH_VALUE = auto()
    MESSAGES_WIN_SENT_SEL_ATTACH_VALUE = auto()
    MESSAGES_WIN_RECV_ATTACH_VALUE = auto()
    MESSAGES_WIN_RECV_SEL_ATTACH_VALUE = auto()

    MESSAGES_WIN_SENT_PREVIEW_LABEL = auto()
    MESSAGES_WIN_SENT_SEL_PREVIEW_LABEL = auto()
    MESSAGES_WIN_RECV_PREVIEW_LABEL = auto()
    MESSAGES_WIN_RECV_SEL_PREVIEW_LABEL = auto()

    MESSAGES_WIN_SENT_PREVIEW_TITLE = auto()
    MESSAGES_WIN_SENT_SEL_PREVIEW_TITLE = auto()
    MESSAGES_WIN_RECV_PREVIEW_TITLE = auto()
    MESSAGES_WIN_RECV_SEL_PREVIEW_TITLE = auto()

    MESSAGES_WIN_SENT_PREVIEW_DESC = auto()
    MESSAGES_WIN_SENT_SEL_PREVIEW_DESC = auto()
    MESSAGES_WIN_RECV_PREVIEW_DESC = auto()
    MESSAGES_WIN_RECV_SEL_PREVIEW_DESC = auto()

    MESSAGES_WIN_SENT_THUMB_LABEL = auto()
    MESSAGES_WIN_SENT_SEL_THUMB_LABEL = auto()
    MESSAGES_WIN_RECV_THUMB_LABEL = auto()
    MESSAGES_WIN_RECV_SEL_THUMB_LABEL = auto()

    MESSAGES_WIN_SENT_THUMB_VALUE = auto()
    MESSAGES_WIN_SENT_SEL_THUMB_VALUE = auto()
    MESSAGES_WIN_RECV_THUMB_VALUE = auto()
    MESSAGES_WIN_RECV_SEL_THUMB_VALUE = auto()

    MESSAGES_WIN_SENT_QUOTE_LABEL = auto()
    MESSAGES_WIN_SENT_SEL_QUOTE_LABEL = auto()
    MESSAGES_WIN_RECV_QUOTE_LABEL = auto()
    MESSAGES_WIN_RECV_SEL_QUOTE_LABEL = auto()

    MESSAGES_WIN_SENT_QUOTE_THUMB_LABEL = auto()
    MESSAGES_WIN_SENT_SEL_QUOTE_THUMB_LABEL = auto()
    MESSAGES_WIN_RECV_QUOTE_THUMB_LABEL = auto()
    MESSAGES_WIN_RECV_SEL_QUOTE_THUMB_LABEL = auto()

    MESSAGES_WIN_SENT_QUOTE_THUMB_VALUE = auto()
    MESSAGES_WIN_SENT_SEL_QUOTE_THUMB_VALUE = auto()
    MESSAGES_WIN_RECV_QUOTE_THUMB_VALUE = auto()
    MESSAGES_WIN_RECV_SEL_QUOTE_THUMB_VALUE = auto()

    MESSAGES_WIN_SENT_QUOTE_ATTACH_LABEL = auto()
    MESSAGES_WIN_SENT_SEL_QUOTE_ATTACH_LABEL = auto()
    MESSAGES_WIN_RECV_QUOTE_ATTACH_LABEL = auto()
    MESSAGES_WIN_RECV_SEL_QUOTE_ATTACH_LABEL = auto()

    MESSAGES_WIN_SENT_QUOTE_ATTACH_VALUE = auto()
    MESSAGES_WIN_SENT_SEL_QUOTE_ATTACH_VALUE = auto()
    MESSAGES_WIN_RECV_QUOTE_ATTACH_VALUE = auto()
    MESSAGES_WIN_RECV_SEL_QUOTE_ATTACH_VALUE = auto()

    MESSAGES_WIN_SENT_QUOTE_TEXT = auto()
    MESSAGES_WIN_SENT_SEL_QUOTE_TEXT = auto()
    MESSAGES_WIN_RECV_QUOTE_TEXT = auto()
    MESSAGES_WIN_RECV_SEL_QUOTE_TEXT = auto()

    MESSAGES_WIN_SENT_QUOTE_AUTHOR = auto()
    MESSAGES_WIN_SENT_SEL_QUOTE_AUTHOR = auto()
    MESSAGES_WIN_RECV_QUOTE_AUTHOR = auto()
    MESSAGES_WIN_RECV_SEL_QUOTE_AUTHOR = auto()

    TYPING_WIN = auto()
    """Typing window background."""
    TYPING_WIN_BORDER = auto()
    """Typing window unfocused border"""
    TYPING_WIN_FOCUS_BORDER = auto()
    """Typing window focused border."""
    TYPING_WIN_TITLE = auto()
    """Typing window unfocused title."""
    TYPING_WIN_FOCUS_TITLE = auto()
    """Typing window focused title."""

    MENU_BAR_EMPTY = auto()
    """Menu bar empty spaces"""
    MENU_BAR_UNSEL = auto()
    """Menu bar unselected item attrs."""
    MENU_BAR_SEL = auto()
    """Menu bar selected item attrs."""
    MENU_BAR_UNSEL_ACCEL = auto()
    """Menu bar unselected accelerator attrs."""
    MENU_BAR_SEL_ACCEL = auto()
    """Menu bar selected accelerator attrs."""

    STATUS_BAR_EMPTY = auto()
    """Status bar empty characters."""
    STATUS_BAR_CHAR = auto()
    """Status bar character code."""
    STATUS_BAR_MOUSE = auto()
    """Status bar mouse position."""
    STATUS_RECEIVE = auto()
    """Status bar receive status indicator."""

    MENU_BORDER = auto()
    """Menu border."""
    MENU_SEL = auto()
    """Menu selected item text."""
    MENU_SEL_ACCEL = auto()
    """Menu selected item accelerator text."""
    MENU_UNSEL = auto()
    """Menu unselected text."""
    MENU_UNSEL_ACCEL = auto()
    """Menu unselected accelerator text."""
    MENU_ACCT_LABEL = auto()
    """Menu bar account indicator label text."""
    MENU_ACCT_TEXT = auto()
    """Menu bar account indicator value text."""

    SETTINGS_WIN = auto()
    SETTINGS_WIN_BORDER = auto()
    SETTINGS_WIN_FOCUS_BORDER = auto()
    SETTINGS_WIN_TITLE = auto()
    SETTINGS_WIN_FOCUS_TITLE = auto()

    QUIT_WIN = auto()
    """Quit window background."""
    QUIT_WIN_BORDER = auto()
    """Quit window unfocused border."""
    QUIT_WIN_FOCUS_BORDER = auto()
    """Quit window focused border."""
    QUIT_WIN_TITLE = auto()
    """Quit window unfocused title."""
    QUIT_WIN_FOCUS_TITLE = auto()
    """Quit window focused title."""
    QUIT_WIN_TEXT = auto()
    """Quit window message text."""
    QUIT_WIN_SEL_TEXT = auto()
    """Quit window selected button text."""
    QUIT_WIN_SEL_ACCEL_TEXT = auto()
    """Quit window selected button accelerator text."""
    QUIT_WIN_UNSEL_TEXT = auto()
    """Quit window unselected button text."""
    QUIT_WIN_UNSEL_ACCEL_TEXT = auto()
    """Quit window unselected accelerator text."""

    SWITCH_WIN = auto()
    SWITCH_WIN_BORDER = auto()
    SWITCH_WIN_FOCUS_BORDER = auto()
    SWITCH_WIN_TITLE = auto()
    SWITCH_WIN_FOCUS_TITLE = auto()

    LINK_WIN = auto()
    """Link window background."""
    LINK_WIN_BORDER = auto()
    """Link window unfocused border."""
    LINK_WIN_FOCUS_BORDER = auto()
    """Link window focused border."""
    LINK_WIN_TITLE = auto()
    """Link window unfocused title."""
    LINK_WIN_FOCUS_TITLE = auto()
    """Link window focused title."""
    LINK_WIN_TEXT = auto()
    """Link window message text."""

    REGISTER_WIN = auto()
    REGISTER_WIN_BORDER = auto()
    REGISTER_WIN_FOCUS_BORDER = auto()
    REGISTER_WIN_TITLE = auto()
    REGISTER_WIN_FOCUS_TITLE = auto()

    KEYS_WIN = auto()
    KEYS_WIN_BORDER = auto()
    KEYS_WIN_FOCUS_BORDER = auto()
    KEYS_WIN_TITLE = auto()
    KEYS_WIN_FOCUS_TITLE = auto()

    ABOUT_WIN = auto()
    ABOUT_WIN_BORDER = auto()
    ABOUT_WIN_FOCUS_BORDER = auto()
    ABOUT_WIN_TITLE = auto()
    ABOUT_WIN_FOCUS_TITLE = auto()

    VERSION_WIN = auto()
    """Version window background."""
    VERSION_WIN_BORDER = auto()
    """Version window unfocused border."""
    VERSION_WIN_FOCUS_BORDER = auto()
    """Version window focused border."""
    VERSION_WIN_TITLE = auto()
    """Version window unfocused title."""
    VERSION_WIN_FOCUS_TITLE = auto()
    """Version window focused title."""
    VERSION_TEXT = auto()
    """Version window message text."""

    GEN_MESSAGE_WIN = auto()
    GEN_MESSAGE_WIN_BORDER = auto()
    GEN_MESSAGE_WIN_FOCUS_BORDER = auto()
    GEN_MESSAGE_WIN_TITLE = auto()
    GEN_MESSAGE_WIN_FOCUS_TITLE = auto()

    QRCODE_WIN = auto()
    """Qr-code window background."""
    QRCODE_WIN_BORDER = auto()
    """Qr-code window unfocused border."""
    QRCODE_WIN_FOCUS_BORDER = auto()
    """Qr-code window focused border."""
    QRCODE_WIN_TITLE = auto()
    """Qr-code window unfocused title."""
    QRCODE_WIN_FOCUS_TITLE = auto()
    """Qr-code window focused title."""
    QRCODE_TEXT = auto()
    """Qr-code window qr-code text."""

    BUTTON_SEL = auto()
    """General button selected text."""
    BUTTON_SEL_ACCEL = auto()
    """General button selected accelerator text."""
    BUTTON_UNSEL = auto()
    """General button unselected text."""
    BUTTON_UNSEL_ACCEL = auto()
    """General button unselected accelerator text."""

    SCROLL_ENA_BG = auto()
    """Scroll bar enabled background."""
    SCROLL_DIS_BG = auto()
    """Scroll bar disabled background."""
    SCROLL_ENA_BTN = auto()
    """Scroll bar enabled button."""
    SCROLL_DIS_BTN = auto()
    """Scroll bar disabled button."""
    SCROLL_ENA_HAND = auto()
    """Scroll bar enabled handle."""
    SCROLL_DIS_HAND = auto()
    """Scroll bar disabled handle."""


###########################
# Theme definitions: If you're looking to make your own theme, this is where you want to look.
###########################
_THEMES: dict[str, dict[str, dict[str, int | bool | str]]] = {
    # LIGHT THEME:
    'light': {
        # BACKGROUND CHARACTERS, USUALLY SPACE:
        'backgroundChars': {'menuItem': ' ', 'mainWin': ' ', 'contactsWin': ' ', 'linkWin': ' ', 'messagesWin': ' ',
                            'qrcodeWin': ' ', 'quitWin': ' ', 'typingWin': ' ', 'menuBar': ' ', 'statusBar': ' ',
                            'versionWin': ' ',
                            },
        # MESSAGES WINDOW CHARS:
        'messages': {
            'undelivered': '\u2026', 'delivered': '\u2020', 'read': '\u2021', 'expires': '\u23F2', 'noExpire': ' ',
            'expired': '\U0001F6AB', 'headLead': '\u2524', 'headTail': '\u251C', 'footLead': '\u2524',
            'footTail': '\u251C', 'seperator': '\u250A', 'barLead': '\u251C', 'barMid': '\u254C', 'barTail': '\u2524',
            'barTitleLead': '\u2524', 'barTitleTail': '\u251C', 'msgBarLead': '\u251C', 'msgBarTail': '\u2524',
            'msgBarMid': '\u2500'
        },

        # CONTACTS / GROUPS SUB WINDOWS:
        # Contacts chars:
        'contactSubWinChars': {
            'collapsed': '\u25B6', 'expanded': '\u25BC', 'selected': '\U0001F846 ', 'unselected': '  ',
            'typing': ' \U0001F5AE ', 'notTyping': '   ', 'expandLine': '\u2506',
        },
        # Groups chars:
        'groupSubWinChars': {
            'collapsed': '\u25B6', 'expanded': '\u25BC', 'selected': '\U0001F846 ', 'unselected': '  ',
            'typing': ' \U0001F5AE ', 'notTyping': '   ', 'expandLine': '\u2506',
        },
        # SCROLL BAR CHARACTERS:
        'scrollBarChars': {
            'up': '\u2191', 'pgUp': '\u21C8', 'down': '\u2193', 'pgDown': '\u21CA',
            'left': '\u2190', 'pgLeft': '\u21C7', 'right': '\u2192', 'pgRight': '\u21C9',
            'vHandle': '\u21C5', 'hHandle': '\u21C6', 'bg': '\u2592'
        },
        # BORDER CHARACTERS:
        # Main window border characters:
        'mainBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                            'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'mainFBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                             'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        # Contacts window border characters:
        'contWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'contWinFBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                                'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        # Messages window border characters:
        'msgsWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'msgsWinFBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                                'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        # Typing window border characters:
        'typeWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'typeWinFBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                                'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        # Menu border chars:
        'menuBorderChars': {'ts': '\u2500', 'bs': '\u2500', 'ls': '\u2502', 'rs': '\u2502',  # Sides
                            'tl': '\u250C', 'tr': '\u2510', 'bl': '\u2514', 'br': '\u2518'},  # Corners
        # Settings window border characters.
        'setWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                              'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'setWinFBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners

        # Quit window border characters.
        'quitWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'quitWinFBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                                'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        # Switch account border characters:
        'switchWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                                 'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'switchWinFBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                                  'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        # Keyboard shortcuts border characters:
        'keysWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'keysWinFBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                                'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        # About window border characters:
        'aboutWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                                'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'aboutWinFBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                                 'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        # Version window border characters:
        'verWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                              'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'verWinFBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        # Link account window border characters:
        'linkWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'linkWinFBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                                'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        # Register account window border characters:
        'regWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                              'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'regWinFBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        # QRCode window border characters:
        'qrcodeWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                                 'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'qrcodeWinFBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                                  'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        # The Contacts window: 'contacts' sub-window border chars:
        'contactsBorderChars': {'ts': '\u2500', 'bs': '\u2500', 'ls': '\u2502', 'rs': '\u2502',  # Sides
                                'tl': '\u250C', 'tr': '\u2510', 'bl': '\u2514', 'br': '\u2518'},  # Corners
        'contactsFBorderChars': {'ts': '\u2500', 'bs': '\u2500', 'ls': '\u2502', 'rs': '\u2502',  # Sides
                                 'tl': '\u250C', 'tr': '\u2510', 'bl': '\u2514', 'br': '\u2518'},  # Corners
        # The Contacts window: 'groups' sub-window border chars:
        'groupsBorderChars': {'ts': '\u2500', 'bs': '\u2500', 'ls': '\u2502', 'rs': '\u2502',  # Sides
                              'tl': '\u250C', 'tr': '\u2510', 'bl': '\u2514', 'br': '\u2518'},  # Corners
        'groupsFBorderChars': {'ts': '\u2500', 'bs': '\u2500', 'ls': '\u2502', 'rs': '\u2502',  # Sides
                               'tl': '\u250C', 'tr': '\u2510', 'bl': '\u2514', 'br': '\u2518'},  # Corners

        # The border chars for a single message:
        'messageBorderUnselChars': {'ts': '\u2500', 'bs': '\u2500', 'ls': '\u2502', 'rs': '\u2502',  # Sides
                                    'tl': '\u256D', 'tr': '\u256E', 'bl': '\u2570', 'br': '\u256F'},  # Corners
        'messageBorderSelChars': {'ts': '\u2500', 'bs': '\u2500', 'ls': '\u2502', 'rs': '\u2502',  # Sides
                                  'tl': '\u256D', 'tr': '\u256E', 'bl': '\u2570', 'br': '\u256F'},  # Corners

        # TITLE CHARACTERS:
        # Main window Title start and end characters:
        'mainWinTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'mainWinFTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        # Contacts window title start and end characters:
        'contWinTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'contWinFTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        # Messages window title start and end characters:
        'msgsWinTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'msgsWinFTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        # Typing window title start and end characters: NOTE: NOT USED.
        'typeWinTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'typeWinFTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        # Settings window title start and end characters:
        'setWinTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'setWinFTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        # Quit window title start and end characters:
        'quitWinTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'quitWinFTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        # Switch account window title start and end characters:
        'switchWinTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'switchWinFTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        # Link account window title start and end characters:
        'linkWinTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'linkWinFTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        # Register a new account window title start and end characters:
        'regWinTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'regWinFTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        # Keyboard shortcuts window title start and end characters:
        'keysWinTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'keysWinFTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        # About window title start and end characters:
        'aboutWinTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'aboutWinFTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        # Version window title start and end characters:
        'verWinTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'verWinFTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        # QR Code window title start and end characters:
        'qrcodeWinTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'qrcodeWinFTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        # 'Contacts' sub window title chars:
        'contactsTitleChars': {'lead': '\u2524', 'tail': '\u251C'},
        'contactsFTitleChars': {'lead': '\u2524', 'tail': '\u251C'},
        # 'Groups' sub window title chars:
        'groupsTitleChars': {'lead': '\u2524', 'tail': '\u251C'},
        'groupsFTitleChars': {'lead': '\u2524', 'tail': '\u251C'},


        # BUTTON CHARACTERS:
        # Link window button start and end chars:
        'linkWinBtnBorderChars': {'lead': '\u2561', 'tail': '\u255E'},

        # STATUS BAR CHARACTERS:
        # Receive state:
        'receiveStateChars': {'stopped': '\u2716', 'started': '\u2714'},


        # SELECTION INDICATOR CHARACTERS:
        # Menu bar selection indicator characters:
        'menuBarSelChars': {'leadSel': '\u2192', 'leadUnsel': ' ', 'tailSel': '\u2190', 'tailUnsel': ' '},
        # Menu item selection indicator characters:
        'menuSelChars': {'leadSel': '\u2192', 'leadUnsel': ' ', 'tailSel': '\u2190', 'tailUnsel': ' '},
        # Button selection indicator characters.
        'buttonSelChars': {'leadSel': '\u2192', 'leadUnsel': ' ', 'tailSel': '\u2190', 'tailUnsel': ' '},

        # SCROLL BAR ATTRIBUTES:
        # Enabled background attributes:
        'scrollBarEnaBg': {'fg': 7, 'bg': 18, 'bold': False, 'underline': False, 'reverse': False},
        # Disabled background attributes:
        'scrollBarDisBg': {'fg': 8, 'bg': 18, 'bold': False, 'underline': False, 'reverse': False},
        # Enabled button attributes:
        'scrollBarEnaBtn': {'fg': 7, 'bg': 18, 'bold': False, 'underline': False, 'reverse': False},
        # Disabled button attributes:
        'scrollBarDisBtn': {'fg': 8, 'bg': 18, 'bold': False, 'underline': False, 'reverse': False},
        # Enabled Handle attributes:
        'scrollBarEnaHand': {'fg': 7, 'bg': 18, 'bold': False, 'underline': False, 'reverse': False},
        # Disabled Handle attributes:
        'scrollBarDisHand': {'fg': 8, 'bg': 18, 'bold': False, 'underline': False, 'reverse': False},

        # BUTTON COLOUR ATTRIBUTES:
        # Button selected text:
        'buttonSel': {'fg': 7, 'bg': 18, 'bold': True, 'underline': False, 'reverse': False},
        # Button unselected text:
        'buttonUnsel': {'fg': 7, 'bg': 18, 'bold': False, 'underline': False, 'reverse': False},
        # Button selected accelerator text:
        'buttonSelAccel': {'fg': 7, 'bg': 18, 'bold': True, 'underline': True, 'reverse': False},
        # Button unselected accelerator text:
        'buttonUnselAccel': {'fg': 7, 'bg': 18, 'bold': False, 'underline': True, 'reverse': False},

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
        # Main window Error text:
        'mainWinErrorText': {'fg': 15, 'bg': 1, 'bold': True, 'underline': False, 'reverse': False},

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
        # Contacts window 'contact' border attributes:
        'contWinContBorder': {'fg': 15, 'bg': 19, 'bold': False, 'underline': False, 'reverse': False},
        # Contacts window 'contacts' focused border attributes:
        'contWinContFBorder': {'fg': 15, 'bg': 19, 'bold': True, 'underline': False, 'reverse': False},
        # Contact window 'contacts' sub window title attributes:
        'contWinContTitle': {'fg': 15, 'bg': 19, 'bold': False, 'underline': True, 'reverse': False},
        # Contact window 'contacts' sub window focus title attributes:
        'contWinContFTitle': {'fg': 15, 'bg': 19, 'bold': True, 'underline': True, 'reverse': True},
        # Contacts window 'groups' border attributes:
        'contWinGrpsBorder': {'fg': 15, 'bg': 19, 'bold': False, 'underline': False, 'reverse': False},
        # Contacts window 'groups' focused border attributes:
        'contWinGrpsFBorder': {'fg': 15, 'bg': 19, 'bold': True, 'underline': False, 'reverse': False},
        # Contact window 'groups' sub window title attributes:
        'contWinGrpsTitle': {'fg': 15, 'bg': 19, 'bold': True, 'underline': True, 'reverse': False},
        # Contacts window 'groups sub window focused title attributes:
        'contWinGrpsFTitle': {'fg': 15, 'bg': 19, 'bold': True, 'underline': True, 'reverse': True},

        'contWinSelCont': {'fg': 15, 'bg': 19, 'bold': False, 'underline': False, 'reverse': True},
        'contWinUnselCont': {'fg': 15, 'bg': 19, 'bold': False, 'underline': False, 'reverse': False},
        'contWinSelGrp': {'fg': 15, 'bg': 19, 'bold': False, 'underline': False, 'reverse': True},
        'contWinUnselGrp': {'fg': 15, 'bg': 19, 'bold': False, 'underline': False, 'reverse': False},

        # MESSAGES WINDOW COLOUR ATTRIBUTES:
        # Messages window centre:
        'msgsWin': {'fg': 7, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        # Messages window border:
        'msgsWinBorder': {'fg': 15, 'bg': 17, 'bold': True, 'underline': False, 'reverse': False},
        # Messages window focused border:
        'msgsWinFBorder': {'fg': 15, 'bg': 17, 'bold': True, 'underline': False, 'reverse': True},
        # Messages window Title:
        'msgsWinTitle': {'fg': 15, 'bg': 17, 'bold': True, 'underline': True, 'reverse': False},
        # Messages window focused title:
        'msgsWinFTitle': {'fg': 15, 'bg': 17, 'bold': True, 'underline': True, 'reverse': True},
        # Messages window, message background:
        'msgsWinSentMsgBG': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelMsgBG': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvMsgBG': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelMsgBG': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        # Messages window, message border:
        'msgsWinSentBorder': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelBorder': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvBorder': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelBorder': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        # Messages window, indicator:
        'msgsWinSentIndicator': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelIndicator': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvIndicator': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelIndicator': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        # Messages window, message text:
        'msgsWinSentText': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelText': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvText': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelText': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        # Messages window, date time:
        'msgsWinSentTime': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelTime': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvTime': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelTime': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        # Messages window, sticker label:
        'msgsWinSentStickerLabel': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': True},
        'msgsWinSentSelStickerLabel': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': True},
        'msgsWinRecvStickerLabel': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': True},
        'msgsWinRecvSelStickerLabel': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': True},
        # Messages window sticker value:
        'msgsWinSentStickerValue': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': True},
        'msgsWinSentSelStickerValue': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': True},
        'msgsWinRecvStickerValue': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': True},
        'msgsWinRecvSelStickerValue': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        # Messages window attachment label:
        'msgsWinSentAttachLabel': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelAttachLabel': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvAttachLabel': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelAttachLabel': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        # Messages window attachment value:
        'msgsWinSentAttachValue': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelAttachValue': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvAttachValue': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelAttachValue': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        # Messages window preview label:
        'msgsWinSentPreviewLabel': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelPreviewLabel': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvPreviewLabel': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelPreviewLabel': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        # Messages window preview title:
        'msgsWinSentPreviewTitle': {'fg': 8, 'bg': 17, 'bold': False, 'underline': True, 'reverse': False},
        'msgsWinSentSelPreviewTitle': {'fg': 15, 'bg': 17, 'bold': False, 'underline': True, 'reverse': False},
        'msgsWinRecvPreviewTitle': {'fg': 8, 'bg': 17, 'bold': False, 'underline': True, 'reverse': False},
        'msgsWinRecvSelPreviewTitle': {'fg': 15, 'bg': 17, 'bold': False, 'underline': True, 'reverse': False},
        # Messages window preview description:
        'msgsWinSentPreviewDesc': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelPreviewDesc': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvPreviewDesc': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelPreviewDesc': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        # Messages window thumbnail label:
        'msgsWinSentThumbLabel': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelThumbLabel': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvThumbLabel': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelThumbLabel': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        # Messages window thumbnail value:
        'msgsWinSentThumbValue': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelThumbValue': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvThumbValue': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelThumbValue': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        # Messages window quote label:
        'msgsWinSentQuoteLabel': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelQuoteLabel': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvQuoteLabel': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelQuoteLabel': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        # Messages window quote thumbnail label:
        'msgsWinSentQuoteThumbLabel': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelQuoteThumbLabel': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvQuoteThumbLabel': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelQuoteThumbLabel': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        # Messages window quote thumbnail value:
        'msgsWinSentQuoteThumbValue': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelQuoteThumbValue': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvQuoteThumbValue': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelQuoteThumbValue': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        # Messages window quote attachment label:
        'msgsWinSentQuoteAttachLabel': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelQuoteAttachLabel': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvQuoteAttachLabel': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelQuoteAttachLabel': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        # Messages window quote attachment value:
        'msgsWinSentQuoteAttachValue': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelQuoteAttachValue': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvQuoteAttachValue': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelQuoteAttachValue': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        # Messages window quote text:
        'msgsWinSentQuoteText': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelQuoteText': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvQuoteText': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelQuoteText': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        # Messages window quote sender name:
        'msgsWinSentQuoteAuthor': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelQuoteAuthor': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvQuoteAuthor': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelQuoteAuthor': {'fg': 15, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},

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
        # The settings window border: NOTE: Not used.
        'setWinBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': False},
        # The settings window focused border:
        'setWinFBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': True},
        # The settings window title: NOTE: Not used.
        'setWinTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': False},
        # The settings window focused title:
        'setWinFTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': True},

        # THE QUIT WINDOW COLOUR ATTRIBUTES:
        # The quit window centre:
        'quitWin': {'fg': 7, 'bg': 21, 'bold': False, 'underline': False, 'reverse': False},
        # The quit window border: NOTE: Not used.
        'quitWinBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': False},
        # The quit window focused border:
        'quitWinFBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': True},
        # The quit window title: NOTE: Not used.
        'quitWinTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': False},
        # The quit window focused title:
        'quitWinFTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': True},
        # The quit window text:
        'quitWinText': {'fg': 7, 'bg': 21, 'bold': False, 'underline': False, 'reverse': False},
        # The quit window selected text:
        'quitWinSelText': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': True},
        # The quit window selected accelerator text:
        'quitWinSelAccelText': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': True},
        # The quit window unselected text:
        'quitWinUnselText': {'fg': 7, 'bg': 21, 'bold': False, 'underline': False, 'reverse': False},
        # The quit window unselected accelerator text:
        'quitWinUnselAccelText': {'fg': 7, 'bg': 21, 'bold': False, 'underline': True, 'reverse': False},

        # THE SWITCH ACCOUNT WINDOW COLOUR ATTRIBUTES:
        # The switch window centre:
        'switchWin': {'fg': 7, 'bg': 21, 'bold': False, 'underline': False, 'reverse': False},
        # The switch window border: NOTE: Not used.
        'switchWinBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': False},
        # The switch window focused border:
        'switchWinFBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': True},
        # The switch window title: NOTE: Not used.
        'switchWinTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': False},
        # The switch window focused title:
        'switchWinFTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': True},

        # THE LINK ACCOUNT WINDOW COLOUR ATTRIBUTES:
        # The link window centre:
        'linkWin': {'fg': 7, 'bg': 21, 'bold': False, 'underline': False, 'reverse': False},
        # The link window border: NOTE: Not used.
        'linkWinBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': False},
        # The link window focused border:
        'linkWinFBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': True},
        # The link window title: NOTE: Not used.
        'linkWinTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': False},
        # The link window focused title:
        'linkWinFTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': True},
        # The link window text:
        'linkWinText': {'fg': 7, 'bg': 21, 'bold': False, 'underline': False, 'reverse': False},

        # THE REGISTER NEW ACCOUNT WINDOW COLOUR ATTRIBUTES:
        # The register window centre:
        'regWin': {'fg': 7, 'bg': 21, 'bold': False, 'underline': False, 'reverse': False},
        # The register window border: NOTE: Not used.
        'regWinBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': False},
        # The register window focused border:
        'regWinFBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': True},
        # The register window title: NOTE: Not used.
        'regWinTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': False},
        # The register window focused title:
        'regWinFTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': True},

        # THE SHORTCUT KEYS HELP WINDOW COLOUR ATTRIBUTES:
        # The keys window centre:
        'keysWin': {'fg': 7, 'bg': 21, 'bold': False, 'underline': False, 'reverse': False},
        # The keys window border: NOTE: Not used.
        'keysWinBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': False},
        # The keys window focused border:
        'keysWinFBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': True},
        # The keys window title: NOTE: Not used.
        'keysWinTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': False},
        # The keys window focused title:
        'keysWinFTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': True},

        # THE ABOUT WINDOW COLOUR ATTRIBUTES:
        # The about window centre:
        'aboutWin': {'fg': 7, 'bg': 21, 'bold': False, 'underline': False, 'reverse': False},
        # The about window border: NOTE: Not used.
        'aboutWinBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': False},
        # The about window focused border:
        'aboutWinFBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': True},
        # The about window title: NOTE: Not used.
        'aboutWinTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': False},
        # The about window focused title:
        'aboutWinFTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': True},

        # THE VERSION WINDOW COLOUR ATTRIBUTES:
        # The version window centre:
        'verWin': {'fg': 7, 'bg': 21, 'bold': False, 'underline': False, 'reverse': False},
        # The version window border: NOTE: Not used.
        'verWinBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': False},
        # The version window focused border:
        'verWinFBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': True},
        # The version window title: NOTE: Not used.
        'verWinTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': False},
        # The version window focused title:
        'verWinFTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': True},
        # The version window centre text:
        'verWinText': {'fg': 7, 'bg': 21, 'bold': False, 'underline': False, 'reverse': False},
        # GENERAL MESSAGE WINDOW:
        # General message background window attributes:
        'genMsgWin': {'fg': 7, 'bg': 21, 'bold': False, 'underline': False, 'reverse': False},
        # General message border attributes: NOTE: Not used.
        'genMsgWinBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': False},
        # General message focused border attributes:
        'genMsgWinFBorder': {'fg': 7, 'bg': 21, 'bold': True, 'underline': False, 'reverse': True},
        # General message window title attributes: NOTE: Not used.
        'genMsgWinTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': False},
        # General message window focused title attributes:
        'genMsgWinFTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': True},

        # QR-CODE WINDOW:
        # QR Code window background:
        'qrcodeWin': {'fg': 7, 'bg': 21, 'bold': False, 'underline': False, 'reverse': False},
        # QR Code border: NOTE: Not used.
        'qrcodeWinBorder': {'fg': 7, 'bg': 21, 'bold': False, 'underline': False, 'reverse': False},
        # QR Code focused border:
        'qrcodeWinFBorder': {'fg': 7, 'bg': 21, 'bold': False, 'underline': False, 'reverse': True},
        # QR Code title: NOTE: Not used.
        'qrcodeWinTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': False},
        # QR COde focused title:
        'qrcodeWinFTitle': {'fg': 7, 'bg': 21, 'bold': True, 'underline': True, 'reverse': True},
        # QRCODE text:
        'qrcodeText': {'fg': 15, 'bg': 16, 'bold': False, 'underline': False, 'reverse': False},

        # MENU BAR COLOUR ATTRIBUTES:
        # Menu bar background spaces:
        'menuBarBG': {'fg': 15, 'bg': 18, 'bold': False, 'underline': False, 'reverse': False},
        # Menu bar item selected:
        'menuBarSel': {'fg': 15, 'bg': 18, 'bold': True, 'underline': False, 'reverse': False},
        # Menu bar accelerator indicator when selected:
        'menuBarSelAccel': {'fg': 15, 'bg': 18, 'bold': True, 'underline': True, 'reverse': False},
        # Menu bar item unselected:
        'menuBarUnsel': {'fg': 15, 'bg': 18, 'bold': False, 'underline': False, 'reverse': False},
        # Menu bar item accelerator indicator when unselected.
        'menuBarUnselAccel': {'fg': 15, 'bg': 18, 'bold': False, 'underline': True, 'reverse': False},
        # Menu bar account label:
        'menuBarAccountLabel': {'fg': 15, 'bg': 18, 'bold': True, 'underline': False, 'reverse': False},
        # Menu bar account text:
        'menuBarAccountText': {'fg': 7, 'bg': 18, 'bold': False, 'underline': False, 'reverse': False},
        # STATUS BAR COLOUR ATTRIBUTES:
        # Status bar background spaces:
        'statusBG': {'fg': 15, 'bg': 18, 'bold': False, 'underline': False, 'reverse': False},
        # Status bar character code:
        'statusCC': {'fg': 16, 'bg': 220, 'bold': False, 'underline': False, 'reverse': False},
        # Status bar mouse info:
        'statusMouse': {'fg': 16, 'bg': 196, 'bold': False, 'underline': False, 'reverse': False},
        # Status bar receive state:
        'statusReceive': {'fg': 16, 'bg': 70, 'bold': False, 'underline': False, 'reverse': False},

        # GENERAL MENU COLOUR ATTRIBUTES:
        # Menu border:
        'menuBorder': {'fg': 7, 'bg': 20, 'bold': False, 'underline': False, 'reverse': False},
        # Selected item:
        'menuSel': {'fg': 7, 'bg': 20, 'bold': False, 'underline': False, 'reverse': True},
        # Unselected item:
        'menuUnsel': {'fg': 7, 'bg': 20, 'bold': False, 'underline': False, 'reverse': False},
        # Selected item accelerator:
        'menuSelAccel': {'fg': 7, 'bg': 20, 'bold': False, 'underline': True, 'reverse': False},
        # Unselected item accelerator:
        'menuUnselAccel': {'fg': 7, 'bg': 20, 'bold': False, 'underline': True, 'reverse': False},

    },
    # DARK THEME:
    'dark': {
        'backgroundChars': {'menuItem': ' ', 'mainWin': ' ', 'contactsWin': ' ', 'linkWin': ' ', 'messagesWin': ' ',
                            'qrcodeWin': ' ', 'quitWin': ' ', 'typingWin': ' ', 'menuBar': ' ', 'statusBar': ' ',
                            'versionWin': ' ',
                            },

        'messages': {
            'undelivered': '\u2026', 'delivered': '\u2020', 'read': '\u2021', 'expires': '\u23F2', 'noExpire': ' ',
            'expired': '\U0001F6AB', 'headLead': '\u2524', 'headTail': '\u251C', 'footLead': '\u2524',
            'footTail': '\u251C', 'seperator': '\u250A', 'barLead': '\u251C', 'barMid': '\u254C', 'barTail': '\u2524',
            'barTitleLead': '\u2524', 'barTitleTail': '\u251C', 'msgBarLead': '\u251C', 'msgBarTail': '\u2524',
            'msgBarMid': '\u2500'
        },

        'scrollBarChars': {
            'up': '\u2191', 'pgUp': '\u21C8', 'down': '\u2193', 'pgDown': '\u21CA',
            'left': '\u2190', 'pgLeft': '\u21C7', 'right': '\u2192', 'pgRight': '\u21C9',
            'vHandle': '\u21C5', 'hHandle': '\u21C6', 'bg': '\u2592'
        },

        'contactSubWinChars': {
            'collapsed': '\u2B9A', 'expanded': '\u2B9B', 'selected': '\U0001F846 ', 'unselected': '  ',
            'typing': ' \u270D ', 'notTyping': '   ', 'expandLine': '\u2506',
        },
        'groupSubWinChars': {
            'collapsed': '\u2B9A', 'expanded': '\u2B9B', 'selected': '\U0001F846 ', 'unselected': '  ',
            'typing': ' \u270D ', 'notTyping': '   ', 'expandLine': '\u2506',
        },

        'mainBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                            'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'mainFBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                             'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners

        'contWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'contWinFBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                                'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners

        'msgsWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'msgsWinFBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                                'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners

        'typeWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'typeWinFBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                                'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners

        'setWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                              'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'setWinFBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners

        'quitWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'quitWinFBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                                'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners

        'linkWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'linkWinFBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                                'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners

        'regWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                              'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'regWinFBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners

        'switchWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                                 'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'switchWinFBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                                  'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners

        'keysWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'keysWinFBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                                'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners

        'aboutWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                                'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'aboutWinFBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                                 'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners

        'verWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                              'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'verWinFBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners

        'qrcodeWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                                 'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'qrcodeWinFBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                                  'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners

        'menuBorderChars': {'ts': '\u2500', 'bs': '\u2500', 'ls': '\u2502', 'rs': '\u2502',  # Sides
                            'tl': '\u250C', 'tr': '\u2510', 'bl': '\u2514', 'br': '\u2518'},  # Corners

        'contactsBorderChars': {'ts': '\u2500', 'bs': '\u2500', 'ls': '\u2502', 'rs': '\u2502',  # Sides
                                'tl': '\u250C', 'tr': '\u2510', 'bl': '\u2514', 'br': '\u2518'},  # Corners
        'contactsFBorderChars': {'ts': '\u2501', 'bs': '\u2501', 'ls': '\u2503', 'rs': '\u2503',  # Sides
                                 'tl': '\u250F', 'tr': '\u2513', 'bl': '\u2517', 'br': '\u251B'},  # Corners

        'groupsBorderChars': {'ts': '\u2500', 'bs': '\u2500', 'ls': '\u2502', 'rs': '\u2502',  # Sides
                              'tl': '\u250C', 'tr': '\u2510', 'bl': '\u2514', 'br': '\u2518'},  # Corners
        'groupsFBorderChars': {'ts': '\u2501', 'bs': '\u2501', 'ls': '\u2503', 'rs': '\u2503',  # Sides
                               'tl': '\u250F', 'tr': '\u2513', 'bl': '\u2517', 'br': '\u251B'},  # Corners

        'messageBorderUnselChars': {'ts': '\u2500', 'bs': '\u2500', 'ls': '\u2502', 'rs': '\u2502',  # Sides
                                    'tl': '\u256D', 'tr': '\u256E', 'bl': '\u2570', 'br': '\u256F'},  # Corners
        'messageBorderSelChars': {'ts': '\u2500', 'bs': '\u2500', 'ls': '\u2502', 'rs': '\u2502',  # Sides
                                  'tl': '\u256D', 'tr': '\u256E', 'bl': '\u2570', 'br': '\u256F'},  # Corners

        'mainWinTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'mainWinFTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'contWinTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'contWinFTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'msgsWinTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'msgsWinFTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'typeWinTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'typeWinFTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'setWinTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'setWinFTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'quitWinTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'quitWinFTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'keysWinTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'keysWinFTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'aboutWinTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'aboutWinFTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'verWinTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'verWinFTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'switchWinTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'switchWinFTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'linkWinTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'linkWinFTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'regWinTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'regWinFTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'qrcodeWinTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'qrcodeWinFTitleChars': {'lead': '\u2561', 'tail': '\u255E'},
        'contactsTitleChars': {'lead': '\u2524', 'tail': '\u251C'},
        'contactsFTitleChars': {'lead': '\u252B', 'tail': '\u2523'},
        'groupsTitleChars': {'lead': '\u2524', 'tail': '\u251C'},
        'groupsFTitleChars': {'lead': '\u252B', 'tail': '\u2523'},

        'linkWinBtnBorderChars': {'lead': '\u2561', 'tail': '\u255E'},

        'receiveStateChars': {'stopped': '\u23F8', 'started': '\u25B6'},

        'menuBarSelChars': {'leadSel': '\u2192', 'leadUnsel': ' ', 'tailSel': '\u2190', 'tailUnsel': ' '},
        'menuSelChars': {'leadSel': '\u2192', 'leadUnsel': ' ', 'tailSel': '\u2190', 'tailUnsel': ' '},
        'buttonSelChars': {'leadSel': '\u2192', 'leadUnsel': ' ', 'tailSel': '\u2190', 'tailUnsel': ' '},

        'scrollBarEnaBg': {'fg': 7, 'bg': 245, 'bold': False, 'underline': False, 'reverse': False},
        'scrollBarDisBg': {'fg': 8, 'bg': 237, 'bold': False, 'underline': False, 'reverse': False},
        'scrollBarEnaBtn': {'fg': 7, 'bg': 237, 'bold': False, 'underline': False, 'reverse': False},
        'scrollBarDisBtn': {'fg': 8, 'bg': 237, 'bold': False, 'underline': False, 'reverse': False},
        'scrollBarEnaHand': {'fg': 7, 'bg': 237, 'bold': False, 'underline': False, 'reverse': False},
        'scrollBarDisHand': {'fg': 8, 'bg': 237, 'bold': False, 'underline': False, 'reverse': False},

        'buttonSel': {'fg': 7, 'bg': 237, 'bold': True, 'underline': False, 'reverse': False},
        'buttonUnsel': {'fg': 7, 'bg': 237, 'bold': False, 'underline': False, 'reverse': False},
        'buttonSelAccel': {'fg': 7, 'bg': 237, 'bold': True, 'underline': True, 'reverse': False},
        'buttonUnselAccel': {'fg': 7, 'bg': 237, 'bold': False, 'underline': True, 'reverse': False},

        'mainWin': {'fg': 7, 'bg': 237, 'bold': False, 'underline': False, 'reverse': False},
        'mainWinBorder': {'fg': 7, 'bg': 237, 'bold': True, 'underline': False, 'reverse': False},
        'mainWinFBorder': {'fg': 7, 'bg': 237, 'bold': True, 'underline': False, 'reverse': True},
        'mainWinTitle': {'fg': 7, 'bg': 237, 'bold': True, 'underline': True, 'reverse': False},
        'mainWinFTitle': {'fg': 7, 'bg': 237, 'bold': True, 'underline': True, 'reverse': True},
        'mainWinErrorText': {'fg': 15, 'bg': 1, 'bold': True, 'underline': False, 'reverse': False},

        'contWin': {'fg': 7, 'bg': 238, 'bold': False, 'underline': False, 'reverse': False},
        'contWinBorder': {'fg': 7, 'bg': 238, 'bold': True, 'underline': False, 'reverse': False},
        'contWinFBorder': {'fg': 7, 'bg': 238, 'bold': True, 'underline': False, 'reverse': True},
        'contWinTitle': {'fg': 7, 'bg': 238, 'bold': True, 'underline': True, 'reverse': False},
        'contWinFTitle': {'fg': 7, 'bg': 238, 'bold': True, 'underline': True, 'reverse': True},
        'contWinContBorder': {'fg': 8, 'bg': 235, 'bold': False, 'underline': False, 'reverse': False},
        'contWinContFBorder': {'fg': 7, 'bg': 235, 'bold': True, 'underline': False, 'reverse': False},
        'contWinContTitle': {'fg': 8, 'bg': 235, 'bold': False, 'underline': True, 'reverse': False},
        'contWinContFTitle': {'fg': 7, 'bg': 235, 'bold': True, 'underline': True, 'reverse': False},
        'contWinGrpsBorder': {'fg': 8, 'bg': 235, 'bold': False, 'underline': False, 'reverse': False},
        'contWinGrpsFBorder': {'fg': 7, 'bg': 235, 'bold': True, 'underline': False, 'reverse': False},
        'contWinGrpsTitle': {'fg': 8, 'bg': 235, 'bold': False, 'underline': True, 'reverse': False},
        'contWinGrpsFTitle': {'fg': 7, 'bg': 235, 'bold': True, 'underline': True, 'reverse': False},
        'contWinSelCont': {'fg': 7, 'bg': 235, 'bold': True, 'underline': False, 'reverse': False},
        'contWinUnselCont': {'fg': 8, 'bg': 235, 'bold': False, 'underline': False, 'reverse': False},
        'contWinSelGrp': {'fg': 7, 'bg': 235, 'bold': True, 'underline': False, 'reverse': False},
        'contWinUnselGrp': {'fg': 8, 'bg': 235, 'bold': False, 'underline': False, 'reverse': False},

        'msgsWin': {'fg': 7, 'bg': 235, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinBorder': {'fg': 7, 'bg': 235, 'bold': True, 'underline': False, 'reverse': False},
        'msgsWinFBorder': {'fg': 7, 'bg': 235, 'bold': True, 'underline': False, 'reverse': True},
        'msgsWinTitle': {'fg': 7, 'bg': 235, 'bold': True, 'underline': True, 'reverse': False},
        'msgsWinFTitle': {'fg': 7, 'bg': 235, 'bold': True, 'underline': True, 'reverse': True},
        'msgsWinSentMsgBG': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelMsgBG': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvMsgBG': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelMsgBG': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentBorder': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelBorder': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvBorder': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelBorder': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentIndicator': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelIndicator': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvIndicator': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelIndicator': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentText': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelText': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvText': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelText': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentTime': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelTime': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvTime': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelTime': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentStickerLabel': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': True},
        'msgsWinSentSelStickerLabel': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': True},
        'msgsWinRecvStickerLabel': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': True},
        'msgsWinRecvSelStickerLabel': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': True},
        'msgsWinSentStickerValue': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': True},
        'msgsWinSentSelStickerValue': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': True},
        'msgsWinRecvStickerValue': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': True},
        'msgsWinRecvSelStickerValue': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentAttachLabel': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelAttachLabel': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvAttachLabel': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelAttachLabel': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentAttachValue': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelAttachValue': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvAttachValue': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelAttachValue': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentPreviewLabel': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelPreviewLabel': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvPreviewLabel': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelPreviewLabel': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentPreviewTitle': {'fg': 8, 'bg': 234, 'bold': False, 'underline': True, 'reverse': False},
        'msgsWinSentSelPreviewTitle': {'fg': 15, 'bg': 234, 'bold': False, 'underline': True, 'reverse': False},
        'msgsWinRecvPreviewTitle': {'fg': 8, 'bg': 234, 'bold': False, 'underline': True, 'reverse': False},
        'msgsWinRecvSelPreviewTitle': {'fg': 15, 'bg': 234, 'bold': False, 'underline': True, 'reverse': False},
        'msgsWinSentPreviewDesc': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelPreviewDesc': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvPreviewDesc': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelPreviewDesc': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentThumbLabel': {'fg': 8, 'bg': 225, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelThumbLabel': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvThumbLabel': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelThumbLabel': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentThumbValue': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelThumbValue': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvThumbValue': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelThumbValue': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentQuoteLabel': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelQuoteLabel': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvQuoteLabel': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelQuoteLabel': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentQuoteThumbLabel': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelQuoteThumbLabel': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvQuoteThumbLabel': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelQuoteThumbLabel': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentQuoteThumbValue': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelQuoteThumbValue': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvQuoteThumbValue': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelQuoteThumbValue': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentQuoteAttachLabel': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelQuoteAttachLabel': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvQuoteAttachLabel': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelQuoteAttachLabel': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentQuoteAttachValue': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelQuoteAttachValue': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvQuoteAttachValue': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelQuoteAttachValue': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentQuoteText': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelQuoteText': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvQuoteText': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelQuoteText': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentQuoteAuthor': {'fg': 8, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinSentSelQuoteAuthor': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvQuoteAuthor': {'fg': 8, 'bg': 17, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinRecvSelQuoteAuthor': {'fg': 15, 'bg': 234, 'bold': False, 'underline': False, 'reverse': False},

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
        'quitWinText': {'fg': 7, 'bg': 240, 'bold': False, 'underline': False, 'reverse': False},
        'quitWinSelText': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': True},
        'quitWinSelAccelText': {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': True},
        'quitWinUnselText': {'fg': 7, 'bg': 240, 'bold': False, 'underline': False, 'reverse': False},
        'quitWinUnselAccelText': {'fg': 7, 'bg': 240, 'bold': False, 'underline': True, 'reverse': False},

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
        'linkWinText': {'fg': 7, 'bg': 240, 'bold': False, 'underline': False, 'reverse': False},

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
        'verWinText': {'fg': 7, 'bg': 240, 'bold': False, 'underline': False, 'reverse': False},

        'genMsgWin': {'fg': 7, 'bg': 240, 'bold': False, 'underline': False, 'reverse': False},
        'genMsgWinBorder': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': False},
        'genMsgWinFBorder': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': True},
        'genMsgWinTitle': {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': False},
        'genMsgWinFTitle': {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': True},

        'qrcodeWin': {'fg': 7, 'bg': 240, 'bold': False, 'underline': False, 'reverse': False},
        'qrcodeWinBorder': {'fg': 7, 'bg': 232, 'bold': False, 'underline': False, 'reverse': False},
        'qrcodeWinFBorder': {'fg': 7, 'bg': 232, 'bold': False, 'underline': False, 'reverse': True},
        'qrcodeWinTitle': {'fg': 7, 'bg': 232, 'bold': True, 'underline': True, 'reverse': False},
        'qrcodeWinFTitle': {'fg': 7, 'bg': 232, 'bold': True, 'underline': True, 'reverse': True},
        'qrcodeText': {'fg': 15, 'bg': 16, 'bold': False, 'underline': False, 'reverse': False},

        'menuBarBG': {'fg': 7, 'bg': 236, 'bold': False, 'underline': False, 'reverse': False},
        'menuBarSel': {'fg': 7, 'bg': 16, 'bold': True, 'underline': False, 'reverse': True},
        'menuBarSelAccel': {'fg': 7, 'bg': 16, 'bold': True, 'underline': True, 'reverse': True},
        'menuBarUnsel': {'fg': 7, 'bg': 16, 'bold': False, 'underline': False, 'reverse': False},
        'menuBarUnselAccel': {'fg': 7, 'bg': 16, 'bold': False, 'underline': True, 'reverse': False},
        'menuBarAccountLabel': {'fg': 7, 'bg': 16, 'bold': True, 'underline': True, 'reverse': False},
        'menuBarAccountText': {'fg': 7, 'bg': 16, 'bold': False, 'underline': False, 'reverse': False},

        'statusBG': {'fg': 7, 'bg': 16, 'bold': False, 'underline': False, 'reverse': False},
        'statusCC': {'fg': 16, 'bg': 220, 'bold': False, 'underline': False, 'reverse': False},
        'statusMouse': {'fg': 16, 'bg': 196, 'bold': False, 'underline': True, 'reverse': False},
        'statusReceive': {'fg': 16, 'bg': 70, 'bold': False, 'underline': False, 'reverse': False},

        'menuBorder': {'fg': 7, 'bg': 16, 'bold': False, 'underline': False, 'reverse': False},
        'menuSel': {'fg': 7, 'bg': 16, 'bold': True, 'underline': False, 'reverse': True},
        'menuSelAccel': {'fg': 7, 'bg': 16, 'bold': True, 'underline': True, 'reverse': True},
        'menuUnsel': {'fg': 7, 'bg': 16, 'bold': False, 'underline': False, 'reverse': False},
        'menuUnselAccel': {'fg': 7, 'bg': 16, 'bold': False, 'underline': True, 'reverse': False},

    }
}
"""Light and dark theme definitions."""

# Primary Keys:
_ATTRIBUTE_PRIMARY_KEYS: list[str] = [
    'mainWin', 'mainWinBorder', 'mainWinTitle', 'contWin', 'contWinBorder', 'contWinTitle', 'msgsWin', 'msgsWinBorder',
    'msgsWinTitle', 'typeWin', 'typeWinBorder', 'typeWinTitle', 'mainWinFBorder', 'msgsWinFBorder', 'contWinFBorder',
    'typeWinFBorder', 'mainWinFTitle', 'contWinFTitle', 'msgsWinFTitle', 'typeWinFTitle', 'menuBarBG', 'statusBG',
    'menuBarSel', 'menuBarSelAccel', 'menuBarUnsel', 'menuBarUnselAccel', 'setWin', 'setWinBorder', 'setWinFBorder',
    'setWinTitle', 'setWinFTitle', 'quitWin', 'quitWinBorder', 'quitWinFBorder', 'quitWinTitle', 'quitWinFTitle',
    'switchWin', 'switchWinBorder', 'switchWinFBorder', 'switchWinTitle', 'switchWinFTitle', 'linkWin', 'linkWinBorder',
    'linkWinFBorder', 'linkWinTitle', 'linkWinFTitle', 'regWin', 'regWinBorder', 'regWinFBorder', 'regWinTitle',
    'regWinFTitle', 'keysWin', 'keysWinBorder', 'keysWinFBorder', 'keysWinTitle', 'keysWinTitle', 'aboutWin',
    'aboutWinBorder', 'aboutWinFBorder', 'aboutWinTitle', 'aboutWinFTitle', 'verWin', 'verWinBorder', 'verWinFBorder',
    'verWinTitle', 'verWinFTitle', 'quitWinText', 'quitWinSelText', 'quitWinSelAccelText', 'quitWinUnselText',
    'quitWinUnselAccelText', 'mainWinErrorText', 'genMsgWin', 'genMsgWinBorder', 'genMsgWinFBorder', 'genMsgWinTitle',
    'genMsgWinFTitle', 'qrcodeWin', 'qrcodeWinBorder', 'qrcodeWinFBorder', 'qrcodeWinTitle', 'qrcodeWinFTitle',
    'linkWinText', 'qrcodeText', 'statusCC', 'statusMouse', 'statusReceive', 'menuBarAccountLabel',
    'menuBarAccountText', 'contWinContBorder', 'contWinGrpsBorder', 'contWinContFBorder', 'contWinGrpsFBorder',
    'scrollBarEnaBg', 'scrollBarDisBg', 'scrollBarEnaBtn', 'scrollBarDisBtn', 'scrollBarEnaHand', 'scrollBarDisHand',
    'contWinSelCont', 'contWinUnselCont', 'contWinSelGrp', 'contWinUnselGrp', 'msgsWinSentSelText',
    'msgsWinRecvSelText', 'msgsWinSentSelTime', 'msgsWinRecvSelTime', 'msgsWinSentStickerLabel',
    'msgsWinSentSelStickerLabel', 'msgsWinRecvStickerLabel', 'msgsWinRecvSelStickerLabel', 'msgsWinSentStickerValue',
    'msgsWinSentSelStickerValue', 'msgsWinRecvStickerValue', 'msgsWinRecvSelStickerValue', 'msgsWinSentAttachLabel',
    'msgsWinSentSelAttachLabel', 'msgsWinRecvAttachLabel', 'msgsWinRecvSelAttachLabel', 'msgsWinSentAttachValue',
    'msgsWinSentSelAttachValue', 'msgsWinRecvAttachValue', 'msgsWinRecvSelAttachValue', 'msgsWinSentPreviewLabel',
    'msgsWinSentSelPreviewLabel', 'msgsWinRecvPreviewLabel', 'msgsWinRecvSelPreviewLabel', 'msgsWinSentPreviewTitle',
    'msgsWinSentSelPreviewTitle', 'msgsWinRecvPreviewTitle', 'msgsWinRecvSelPreviewTitle', 'msgsWinSentPreviewDesc',
    'msgsWinSentSelPreviewDesc', 'msgsWinRecvPreviewDesc', 'msgsWinRecvSelPreviewDesc', 'msgsWinSentThumbLabel',
    'msgsWinSentSelThumbLabel', 'msgsWinRecvThumbLabel', 'msgsWinRecvSelThumbLabel', 'msgsWinSentThumbValue',
    'msgsWinSentSelThumbValue', 'msgsWinRecvThumbValue', 'msgsWinRecvSelThumbValue', 'msgsWinSentMsgBG',
    'msgsWinSentSelMsgBG', 'msgsWinRecvMsgBG', 'msgsWinRecvSelMsgBG', 'msgsWinSentQuoteLabel',
    'msgsWinSentSelQuoteLabel', 'msgsWinRecvQuoteLabel', 'msgsWinRecvSelQuoteLabel', 'msgsWinSentQuoteThumbLabel',
    'msgsWinSentSelQuoteThumbLabel', 'msgsWinRecvQuoteThumbLabel', 'msgsWinRecvSelQuoteThumbLabel',
    'msgsWinSentQuoteThumbValue', 'msgsWinSentSelQuoteThumbValue', 'msgsWinRecvQuoteThumbValue',
    'msgsWinRecvSelQuoteThumbValue', 'msgsWinSentQuoteAttachLabel', 'msgsWinSentSelQuoteAttachLabel',
    'msgsWinRecvQuoteAttachLabel', 'msgsWinRecvSelQuoteAttachLabel', 'msgsWinSentQuoteAttachValue',
    'msgsWinSentSelQuoteAttachValue', 'msgsWinRecvQuoteAttachValue', 'msgsWinRecvSelQuoteAttachValue',
    'msgsWinSentQuoteText', 'msgsWinSentSelQuoteText', 'msgsWinRecvQuoteText', 'msgsWinRecvSelQuoteText',
    'msgsWinSentQuoteAuthor', 'msgsWinSentSelQuoteAuthor', 'msgsWinRecvQuoteAuthor', 'msgsWinRecvSelQuoteAuthor',

]
"""Primary attribute theme keys."""

_TITLE_CHAR_PRIMARY_KEYS: list[str] = ['mainWinTitleChars', 'contWinTitleChars', 'msgsWinTitleChars',
                                       'typeWinTitleChars', 'setWinTitleChars', 'quitWinTitleChars',
                                       'keysWinTitleChars', 'aboutWinTitleChars', 'verWinTitleChars',
                                       'switchWinTitleChars', 'linkWinTitleChars', 'regWinTitleChars',
                                       'qrcodeWinTitleChars', 'contactsTitleChars', 'groupsTitleChars',
                                       'mainWinFTitleChars', 'contWinFTitleChars', 'msgsWinFTitleChars',
                                       'typeWinFTitleChars', 'setWinFTitleChars', 'quitWinFTitleChars',
                                       'keysWinFTitleChars', 'aboutWinFTitleChars', 'verWinFTitleChars',
                                       'switchWinFTitleChars', 'linkWinFTitleChars', 'regWinFTitleChars',
                                       'qrcodeWinFTitleChars', 'contactsFTitleChars', 'groupsFTitleChars',
                                       ]
"""Title characters primary keys."""

_BUTTON_BORDER_CHAR_PRIMARY_KEYS: list[str] = ['linkWinBtnBorderChars',
                                               ]
"""Button border character primary keys."""
_SELECTION_PRIMARY_KEYS: list[str] = ['menuBarSelChars', 'menuSelChars', 'buttonSelChars',
                                      ]
"""Menu selection primary keys."""

_BORDER_PRIMARY_KEYS: list[str] = [
    'mainBorderChars', 'contWinBorderChars', 'msgsWinBorderChars', 'typeWinBorderChars',
    'menuBorderChars', 'setWinBorderChars', 'quitWinBorderChars', 'switchWinBorderChars',
    'keysWinBorderChars', 'verWinBorderChars', 'linkWinBorderChars', 'regWinBorderChars',
    'qrcodeWinBorderChars', 'contactsBorderChars', 'groupsBorderChars',
    'mainFBorderChars', 'contWinFBorderChars', 'msgsWinFBorderChars', 'typeWinFBorderChars',
    'setWinFBorderChars', 'quitWinFBorderChars', 'switchWinFBorderChars',
    'keysWinFBorderChars', 'verWinFBorderChars', 'linkWinFBorderChars', 'regWinFBorderChars',
    'qrcodeWinFBorderChars', 'contactsFBorderChars', 'groupsFBorderChars', 'messageBorderUnselChars',
    'messageBorderSelChars',
]
"""Keys with border strings."""

# Sub keys:
_ATTR_KEYS: list[str] = ['fg', 'bg', 'bold', 'underline', 'reverse']
"""Attribute keys."""

_BORDER_CHAR_KEYS: list[str] = ['ts', 'bs', 'ls', 'rs', 'tl', 'tr', 'bl', 'br']
"""Border character keys."""

_TITLE_CHAR_KEYS: list[str] = ['lead', 'tail']
"""Title character keys."""

_BUTTON_CHAR_KEYS: list[str] = ['lead', 'tail']
"""Button character keys."""

_MENU_SEL_CHAR_KEYS: list[str] = ['leadSel', 'leadUnsel', 'tailSel', 'tailUnsel']
"""Menu selection indicator character keys."""

_BUTTON_BORDER_CHAR_KEYS: list[str] = ['lead', 'tail']
"""Button border character keys."""

_BACKGROUND_CHAR_KEYS: list[str] = ['menuItem', 'mainWin', 'contactsWin', 'linkWin', 'messagesWin', 'qrcodeWin',
                                    'quitWin', 'typingWin', 'menuBar', 'statusBar', 'versionWin',
                                    ]

_SCROLL_BAR_CHAR_KEYS: list[str] = [
    'up', 'pgUp', 'down', 'pgDown', 'left', 'pgLeft', 'right', 'pgRight', 'vHandle', 'hHandle', 'bg',
]

_MESSAGE_CHAR_KEYS: list[str] = [
    'undelivered', 'delivered', 'read', 'expires', 'noExpire', 'expired', 'headLead', 'headTail', 'footLead',
    'footTail', 'seperator', 'barLead', 'barMid', 'barTail', 'barTitleLead', 'barTitleTail'
]


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
            else:  # The rest must be boolean
                if not isinstance(theme[main_key][attr_key], bool):
                    return False, "Type error: ['%s']['%s'] is not a boolean." % (main_key, attr_key)
    # Border character keys:
    for border_key in _BORDER_PRIMARY_KEYS:
        if border_key not in theme.keys():
            return False, "Primary key '%s' doesn't exist." % border_key
        for border_char_key in _BORDER_CHAR_KEYS:
            if border_char_key not in theme[border_key].keys():
                return False, "Key '%s' missing from '%s'." % (border_char_key, border_key)

    # Menu selection character keys:
    for menu_sel_primary_key in _SELECTION_PRIMARY_KEYS:
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

    # Button border characters keys:
    for button_border_primary_key in _BUTTON_BORDER_CHAR_PRIMARY_KEYS:
        if button_border_primary_key not in theme.keys():
            return False, "Primary key '%s' doesn't exist." % button_border_primary_key
        for button_border_key in _BUTTON_BORDER_CHAR_KEYS:
            if button_border_key not in theme[button_border_primary_key].keys():
                return False, "Key '%s' missing from '%s'." % (button_border_key, button_border_primary_key)

    # Background characters:
    if 'backgroundChars' not in theme.keys():
        return False, "Primary key 'backgroundChars' doesn't exist."
    for bg_char_key in _BACKGROUND_CHAR_KEYS:
        if bg_char_key not in theme['backgroundChars'].keys():
            return False, "Key '%s' missing from 'backgroundChars'." % bg_char_key
    # Receive state characters:
    if 'receiveStateChars' not in theme.keys():
        return False, "Primary key 'receiveStateChars' doesn't exist."
    for char_key in theme['receiveStateChars'].keys():
        if char_key not in ('started', 'stopped'):
            return False, "Key '%s' not in 'receiveStateChars'." % char_key
    # Scroll bar characters:
    if 'scrollBarChars' not in theme.keys():
        return False, "Primary key 'scrollBarChars' doesn't exist."
    for char_key in theme['scrollBarChars'].keys():
        if char_key not in _SCROLL_BAR_CHAR_KEYS:
            return False, "Key '%s' not in 'scrollBarChars'." % char_key
    # Sub window chars:
    for pri_key in 'contactSubWinChars', 'groupSubWinChars':
        if pri_key not in theme.keys():
            return False, "Primary key '%s' doesn't exist." % pri_key
        for char_key in 'collapsed', 'expanded', 'selected', 'unselected', 'typing', 'expandLine':
            if char_key not in theme[pri_key].keys():
                return False, "Key '%s' not in '%s'." % (char_key, pri_key)

    if 'messages' not in theme.keys():
        return False, "Primary key 'messages' doesn't exist."
    for char_key in _MESSAGE_CHAR_KEYS:
        if char_key not in theme['messages'].keys():
            return False, "Key '%s' not found in 'messages'." % char_key

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
    ################
    # Main window:
    curses.init_pair(ThemeColours.MAIN_WIN, theme['mainWin']['fg'], theme['mainWin']['bg'])
    curses.init_pair(ThemeColours.MAIN_WIN_BORDER, theme['mainWinBorder']['fg'], theme['mainWinBorder']['bg'])
    curses.init_pair(ThemeColours.MAIN_WIN_FOCUS_BORDER, theme['mainWinFBorder']['fg'],
                     theme['mainWinFBorder']['bg'])
    curses.init_pair(ThemeColours.MAIN_WIN_TITLE, theme['mainWinTitle']['fg'], theme['mainWinTitle']['bg'])
    curses.init_pair(ThemeColours.MAIN_WIN_FOCUS_TITLE, theme['mainWinFTitle']['fg'],
                     theme['mainWinFTitle']['bg'])
    curses.init_pair(ThemeColours.MAIN_WIN_ERROR_TEXT, theme['mainWinErrorText']['fg'], theme['mainWinErrorText']['bg'])

    ##############
    # Contacts window:
    curses.init_pair(ThemeColours.CONTACTS_WIN, theme['contWin']['fg'], theme['contWin']['bg'])
    curses.init_pair(ThemeColours.CONTACT_WIN_BORDER, theme['contWinBorder']['fg'], theme['contWinBorder']['bg'])
    curses.init_pair(ThemeColours.CONTACTS_WIN_FOCUS_BORDER, theme['contWinFBorder']['fg'],
                     theme['contWinFBorder']['bg'])
    curses.init_pair(ThemeColours.CONTACT_WIN_TITLE, theme['contWinTitle']['fg'], theme['contWinTitle']['bg'])
    curses.init_pair(ThemeColours.CONTACTS_WIN_FOCUS_TITLE, theme['contWinFTitle']['fg'],
                     theme['contWinFTitle']['bg'])
    curses.init_pair(ThemeColours.CONTACTS_WIN_CONT_BORDER, theme['contWinContBorder']['fg'],
                     theme['contWinContBorder']['bg'])
    curses.init_pair(ThemeColours.CONTACTS_WIN_CONT_F_BORDER, theme['contWinContFBorder']['fg'],
                     theme['contWinContFBorder']['bg'])
    curses.init_pair(ThemeColours.CONTACTS_WIN_GRPS_BORDER, theme['contWinGrpsBorder']['fg'],
                     theme['contWinGrpsBorder']['bg'])
    curses.init_pair(ThemeColours.CONTACTS_WIN_GRPS_F_BORDER, theme['contWinGrpsFBorder']['fg'],
                     theme['contWinGrpsFBorder']['bg'])
    curses.init_pair(ThemeColours.CONTACTS_WIN_CONT_TITLE, theme['contWinContTitle']['fg'],
                     theme['contWinContTitle']['bg'])
    curses.init_pair(ThemeColours.CONTACTS_WIN_CONT_F_TITLE, theme['contWinContFTitle']['fg'],
                     theme['contWinContFTitle']['bg'])
    curses.init_pair(ThemeColours.CONTACTS_WIN_GRPS_TITLE, theme['contWinGrpsTitle']['fg'],
                     theme['contWinGrpsTitle']['bg'])
    curses.init_pair(ThemeColours.CONTACTS_WIN_GRPS_F_TITLE, theme['contWinGrpsFTitle']['fg'],
                     theme['contWinGrpsFTitle']['bg'])
    curses.init_pair(ThemeColours.CONTACTS_WIN_SEL_CONT, theme['contWinSelCont']['fg'], theme['contWinSelCont']['bg'])
    curses.init_pair(ThemeColours.CONTACTS_WIN_UNSEL_CONT, theme['contWinUnselCont']['fg'],
                     theme['contWinUnselCont']['bg'])
    curses.init_pair(ThemeColours.CONTACTS_WIN_SEL_GRP, theme['contWinSelGrp']['fg'], theme['contWinSelGrp']['bg'])
    curses.init_pair(ThemeColours.CONTACTS_WIN_UNSEL_GRP, theme['contWinUnselGrp']['fg'],
                     theme['contWinUnselGrp']['bg'])

    ###############
    # Messages window:
    curses.init_pair(ThemeColours.MESSAGES_WIN, theme['msgsWin']['fg'], theme['msgsWin']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_BORDER, theme['msgsWinBorder']['fg'], theme['msgsWinBorder']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_FOCUS_BORDER, theme['msgsWinFBorder']['fg'],
                     theme['msgsWinFBorder']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_TITLE, theme['msgsWinTitle']['fg'], theme['msgsWinTitle']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_FOCUS_TITLE, theme['msgsWinFTitle']['fg'],
                     theme['msgsWinFTitle']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_MSG_BG, theme['msgsWinSentMsgBG']['fg'],
                     theme['msgsWinSentMsgBG']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_SEL_MSG_BG, theme['msgsWinSentSelMsgBG']['fg'],
                     theme['msgsWinSentSelMsgBG']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_MSG_BG, theme['msgsWinRecvMsgBG']['fg'],
                     theme['msgsWinRecvMsgBG']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_SEL_MGS_BG, theme['msgsWinRecvSelMsgBG']['fg'],
                     theme['msgsWinRecvSelMsgBG']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_TEXT, theme['msgsWinSentText']['fg'],
                     theme['msgsWinSentText']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_TEXT, theme['msgsWinRecvText']['fg'],
                     theme['msgsWinRecvText']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_BORDER, theme['msgsWinSentBorder']['fg'],
                     theme['msgsWinSentBorder']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_SEL_BORDER, theme['msgsWinSentSelBorder']['fg'],
                     theme['msgsWinSentSelBorder']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_BORDER, theme['msgsWinRecvBorder']['fg'],
                     theme['msgsWinRecvBorder']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_SEL_BORDER, theme['msgsWinRecvSelBorder']['fg'],
                     theme['msgsWinRecvSelBorder']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_TIME, theme['msgsWinSentTime']['fg'],
                     theme['msgsWinSentTime']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_TIME, theme['msgsWinRecvTime']['fg'],
                     theme['msgsWinRecvTime']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_INDICATOR, theme['msgsWinSentIndicator']['fg'],
                     theme['msgsWinSentIndicator']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_SEL_INDICATOR, theme['msgsWinSentSelIndicator']['fg'],
                     theme['msgsWinSentSelIndicator']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_INDICATOR, theme['msgsWinRecvIndicator']['fg'],
                     theme['msgsWinRecvIndicator']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_SEL_INDICATOR, theme['msgsWinRecvSelIndicator']['fg'],
                     theme['msgsWinRecvSelIndicator']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_SEL_TEXT, theme['msgsWinSentSelText']['fg'],
                     theme['msgsWinSentSelText']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_SEL_TEXT, theme['msgsWinRecvSelText']['fg'],
                     theme['msgsWinRecvSelText']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_SEL_TIME, theme['msgsWinSentSelTime']['fg'],
                     theme['msgsWinSentSelTime']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_SEL_TIME, theme['msgsWinRecvSelTime']['fg'],
                     theme['msgsWinRecvSelTime']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_STICKER_LABEL, theme['msgsWinSentStickerLabel']['fg'],
                     theme['msgsWinSentStickerLabel']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_SEL_STICKER_LABEL, theme['msgsWinSentStickerLabel']['fg'],
                     theme['msgsWinSentStickerLabel']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_STICKER_LABEL, theme['msgsWinRecvStickerLabel']['fg'],
                     theme['msgsWinRecvStickerLabel']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_SEL_STICKER_LABEL, theme['msgsWinRecvSelStickerLabel']['fg'],
                     theme['msgsWinRecvSelStickerLabel']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_STICKER_VALUE, theme['msgsWinSentStickerValue']['fg'],
                     theme['msgsWinSentStickerValue']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_SEL_STICKER_VALUE, theme['msgsWinSentSelStickerValue']['fg'],
                     theme['msgsWinSentSelStickerValue']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_STICKER_VALUE, theme['msgsWinRecvStickerValue']['fg'],
                     theme['msgsWinRecvStickerValue']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_SEL_STICKER_VALUE, theme['msgsWinRecvSelStickerValue']['fg'],
                     theme['msgsWinRecvSelStickerValue']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_ATTACH_LABEL, theme['msgsWinSentAttachLabel']['fg'],
                     theme['msgsWinSentAttachLabel']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_SEL_ATTACH_LABEL, theme['msgsWinSentSelAttachLabel']['fg'],
                     theme['msgsWinSentSelAttachLabel']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_ATTACH_LABEL, theme['msgsWinRecvAttachLabel']['fg'],
                     theme['msgsWinRecvAttachLabel']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_SEL_ATTACH_LABEL, theme['msgsWinRecvSelAttachLabel']['fg'],
                     theme['msgsWinRecvSelAttachLabel']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_ATTACH_VALUE, theme['msgsWinSentAttachValue']['fg'],
                     theme['msgsWinSentAttachValue']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_SEL_ATTACH_VALUE, theme['msgsWinSentSelAttachValue']['fg'],
                     theme['msgsWinSentSelAttachValue']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_ATTACH_VALUE, theme['msgsWinRecvAttachValue']['fg'],
                     theme['msgsWinRecvAttachValue']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_SEL_ATTACH_VALUE, theme['msgsWinRecvSelAttachValue']['fg'],
                     theme['msgsWinRecvSelAttachValue']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_PREVIEW_LABEL, theme['msgsWinSentPreviewLabel']['fg'],
                     theme['msgsWinSentPreviewLabel']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_SEL_PREVIEW_LABEL, theme['msgsWinSentSelPreviewLabel']['fg'],
                     theme['msgsWinSentSelPreviewLabel']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_PREVIEW_LABEL, theme['msgsWinRecvPreviewLabel']['fg'],
                     theme['msgsWinRecvPreviewLabel']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_SEL_PREVIEW_LABEL, theme['msgsWinRecvSelPreviewLabel']['fg'],
                     theme['msgsWinRecvSelPreviewLabel']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_PREVIEW_TITLE, theme['msgsWinSentPreviewTitle']['fg'],
                     theme['msgsWinSentPreviewTitle']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_SEL_PREVIEW_TITLE, theme['msgsWinSentSelPreviewTitle']['fg'],
                     theme['msgsWinSentSelPreviewTitle']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_PREVIEW_TITLE, theme['msgsWinRecvPreviewTitle']['fg'],
                     theme['msgsWinRecvPreviewTitle']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_SEL_PREVIEW_TITLE, theme['msgsWinRecvSelPreviewTitle']['fg'],
                     theme['msgsWinRecvSelPreviewTitle']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_PREVIEW_DESC, theme['msgsWinSentPreviewDesc']['fg'],
                     theme['msgsWinSentPreviewDesc']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_SEL_PREVIEW_DESC, theme['msgsWinSentSelPreviewDesc']['fg'],
                     theme['msgsWinSentSelPreviewDesc']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_PREVIEW_DESC, theme['msgsWinRecvPreviewDesc']['fg'],
                     theme['msgsWinRecvPreviewDesc']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_SEL_PREVIEW_DESC, theme['msgsWinRecvSelPreviewDesc']['fg'],
                     theme['msgsWinRecvSelPreviewDesc']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_THUMB_LABEL, theme['msgsWinSentThumbLabel']['fg'],
                     theme['msgsWinSentThumbLabel']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_SEL_THUMB_LABEL, theme['msgsWinSentSelThumbLabel']['fg'],
                     theme['msgsWinSentSelThumbLabel']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_THUMB_LABEL, theme['msgsWinRecvThumbLabel']['fg'],
                     theme['msgsWinRecvThumbLabel']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_SEL_THUMB_LABEL, theme['msgsWinRecvSelThumbLabel']['fg'],
                     theme['msgsWinRecvSelThumbLabel']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_THUMB_VALUE, theme['msgsWinSentThumbValue']['fg'],
                     theme['msgsWinSentThumbValue']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_SEL_THUMB_VALUE, theme['msgsWinSentSelThumbValue']['fg'],
                     theme['msgsWinSentSelThumbValue']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_THUMB_VALUE, theme['msgsWinRecvThumbValue']['fg'],
                     theme['msgsWinRecvThumbValue']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_SEL_THUMB_VALUE, theme['msgsWinRecvSelThumbValue']['fg'],
                     theme['msgsWinRecvSelThumbValue']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_QUOTE_LABEL, theme['msgsWinSentQuoteLabel']['fg'],
                     theme['msgsWinSentQuoteLabel']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_SEL_QUOTE_LABEL, theme['msgsWinSentSelQuoteLabel']['fg'],
                     theme['msgsWinSentSelQuoteLabel']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_QUOTE_LABEL, theme['msgsWinRecvQuoteLabel']['fg'],
                     theme['msgsWinRecvQuoteLabel']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_SEL_QUOTE_LABEL, theme['msgsWinRecvSelQuoteLabel']['fg'],
                     theme['msgsWinRecvSelQuoteLabel']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_QUOTE_THUMB_LABEL, theme['msgsWinSentQuoteThumbLabel']['fg'],
                     theme['msgsWinSentQuoteThumbLabel']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_SEL_QUOTE_THUMB_LABEL, theme['msgsWinSentSelQuoteThumbLabel']['fg'],
                     theme['msgsWinSentSelQuoteThumbLabel']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_QUOTE_THUMB_LABEL, theme['msgsWinRecvQuoteThumbLabel']['fg'],
                     theme['msgsWinRecvQuoteThumbLabel']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_SEL_QUOTE_THUMB_LABEL, theme['msgsWinRecvSelQuoteThumbLabel']['fg'],
                     theme['msgsWinRecvSelQuoteThumbLabel']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_QUOTE_THUMB_VALUE, theme['msgsWinSentQuoteThumbValue']['fg'],
                     theme['msgsWinSentQuoteThumbValue']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_SEL_QUOTE_THUMB_VALUE, theme['msgsWinSentSelQuoteThumbValue']['fg'],
                     theme['msgsWinSentSelQuoteThumbValue']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_QUOTE_THUMB_VALUE, theme['msgsWinRecvQuoteThumbValue']['fg'],
                     theme['msgsWinRecvQuoteThumbValue']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_SEL_QUOTE_THUMB_VALUE, theme['msgsWinRecvSelQuoteThumbValue']['fg'],
                     theme['msgsWinRecvSelQuoteThumbValue']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_QUOTE_ATTACH_LABEL,
                     theme['msgsWinSentQuoteAttachLabel']['fg'], theme['msgsWinSentQuoteAttachLabel']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_SEL_QUOTE_ATTACH_LABEL,
                     theme['msgsWinSentSelQuoteAttachLabel']['fg'], theme['msgsWinSentSelQuoteAttachLabel']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_QUOTE_ATTACH_LABEL, theme['msgsWinRecvQuoteAttachLabel']['fg'],
                     theme['msgsWinRecvQuoteAttachLabel']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_SEL_QUOTE_ATTACH_LABEL, theme['msgsWinRecvSelQuoteAttachLabel']['fg'],
                     theme['msgsWinRecvSelQuoteAttachLabel']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_QUOTE_ATTACH_VALUE, theme['msgsWinSentQuoteAttachValue']['fg'],
                     theme['msgsWinSentQuoteAttachValue']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_SEL_QUOTE_ATTACH_VALUE, theme['msgsWinSentSelQuoteAttachValue']['fg'],
                     theme['msgsWinSentSelQuoteAttachValue']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_QUOTE_ATTACH_VALUE, theme['msgsWinRecvQuoteAttachValue']['fg'],
                     theme['msgsWinRecvQuoteAttachValue']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_SEL_QUOTE_ATTACH_VALUE, theme['msgsWinRecvSelQuoteAttachValue']['fg'],
                     theme['msgsWinRecvSelQuoteAttachValue']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_QUOTE_TEXT, theme['msgsWinSentQuoteText']['fg'],
                     theme['msgsWinSentQuoteText']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_SEL_QUOTE_TEXT, theme['msgsWinSentSelQuoteText']['fg'],
                     theme['msgsWinSentSelQuoteText']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_QUOTE_TEXT, theme['msgsWinRecvQuoteText']['fg'],
                     theme['msgsWinRecvQuoteText']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_RECV_SEL_QUOTE_TEXT, theme['msgsWinRecvSelQuoteText']['fg'],
                     theme['msgsWinRecvSelQuoteText']['bg'])

    ##########
    # Typing window:
    curses.init_pair(ThemeColours.TYPING_WIN, theme['typeWin']['fg'], theme['typeWin']['bg'])
    curses.init_pair(ThemeColours.TYPING_WIN_BORDER, theme['typeWinBorder']['fg'], theme['typeWinBorder']['bg'])
    curses.init_pair(ThemeColours.TYPING_WIN_FOCUS_BORDER, theme['typeWinFBorder']['fg'],
                     theme['typeWinFBorder']['bg'])
    curses.init_pair(ThemeColours.TYPING_WIN_TITLE, theme['typeWinTitle']['fg'], theme['typeWinTitle']['bg'])
    curses.init_pair(ThemeColours.TYPING_WIN_FOCUS_TITLE, theme['typeWinFTitle']['fg'],
                     theme['typeWinFTitle']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_SENT_BORDER, theme['msgsWinSentBorder']['fg'],
                     theme['msgsWinSentBorder']['bg'])

    curses.init_pair(ThemeColours.MENU_BAR_EMPTY, theme['menuBarBG']['fg'], theme['menuBarBG']['bg'])
    curses.init_pair(ThemeColours.MENU_BAR_SEL, theme['menuBarSel']['fg'], theme['menuBarSel']['bg'])
    curses.init_pair(ThemeColours.MENU_BAR_SEL_ACCEL, theme['menuBarSelAccel']['fg'], theme['menuBarSelAccel']['bg'])
    curses.init_pair(ThemeColours.MENU_BAR_UNSEL, theme['menuBarUnsel']['fg'], theme['menuBarUnsel']['bg'])
    curses.init_pair(ThemeColours.MENU_BAR_UNSEL_ACCEL, theme['menuBarUnselAccel']['fg'],
                     theme['menuBarUnselAccel']['bg'])
    curses.init_pair(ThemeColours.MENU_ACCT_LABEL, theme['menuBarAccountLabel']['fg'],
                     theme['menuBarAccountLabel']['bg'])
    curses.init_pair(ThemeColours.MENU_ACCT_TEXT, theme['menuBarAccountText']['fg'], theme['menuBarAccountText']['bg'])

    #############
    # Status bar:
    curses.init_pair(ThemeColours.STATUS_BAR_EMPTY, theme['statusBG']['fg'], theme['statusBG']['bg'])
    curses.init_pair(ThemeColours.STATUS_BAR_CHAR, theme['statusCC']['fg'], theme['statusCC']['bg'])
    curses.init_pair(ThemeColours.STATUS_BAR_MOUSE, theme['statusMouse']['fg'], theme['statusMouse']['bg'])
    curses.init_pair(ThemeColours.STATUS_RECEIVE, theme['statusReceive']['fg'], theme['statusReceive']['bg'])

    ##############
    # Menu's:
    curses.init_pair(ThemeColours.MENU_BORDER, theme['menuBorder']['fg'], theme['menuBorder']['bg'])
    curses.init_pair(ThemeColours.MENU_SEL, theme['menuSel']['fg'], theme['menuSel']['bg'])
    curses.init_pair(ThemeColours.MENU_UNSEL, theme['menuUnsel']['fg'], theme['menuUnsel']['bg'])
    curses.init_pair(ThemeColours.MENU_SEL_ACCEL, theme['menuSelAccel']['fg'], theme['menuSelAccel']['bg'])
    curses.init_pair(ThemeColours.MENU_UNSEL_ACCEL, theme['menuUnselAccel']['fg'], theme['menuUnselAccel']['bg'])

    ##############
    # Settings window:
    curses.init_pair(ThemeColours.SETTINGS_WIN, theme['setWin']['fg'], theme['setWin']['bg'])
    curses.init_pair(ThemeColours.SETTINGS_WIN_BORDER, theme['setWinBorder']['fg'], theme['setWinBorder']['bg'])
    curses.init_pair(ThemeColours.SETTINGS_WIN_FOCUS_BORDER, theme['setWinFBorder']['fg'], theme['setWinFBorder']['bg'])
    curses.init_pair(ThemeColours.SETTINGS_WIN_TITLE, theme['setWinTitle']['fg'], theme['setWinTitle']['bg'])
    curses.init_pair(ThemeColours.SETTINGS_WIN_FOCUS_TITLE, theme['setWinFTitle']['fg'], theme['setWinFTitle']['bg'])

    ##############
    # Quit window:
    curses.init_pair(ThemeColours.QUIT_WIN, theme['quitWin']['fg'], theme['quitWin']['bg'])
    curses.init_pair(ThemeColours.QUIT_WIN_BORDER, theme['quitWinBorder']['fg'], theme['quitWinBorder']['bg'])
    curses.init_pair(ThemeColours.QUIT_WIN_FOCUS_BORDER, theme['quitWinFBorder']['fg'], theme['quitWinFBorder']['bg'])
    curses.init_pair(ThemeColours.QUIT_WIN_TITLE, theme['quitWinTitle']['fg'], theme['quitWinTitle']['bg'])
    curses.init_pair(ThemeColours.QUIT_WIN_FOCUS_TITLE, theme['quitWinFTitle']['fg'], theme['quitWinFTitle']['bg'])
    curses.init_pair(ThemeColours.QUIT_WIN_TEXT, theme['quitWinText']['fg'], theme['quitWinText']['bg'])
    curses.init_pair(ThemeColours.QUIT_WIN_SEL_TEXT, theme['quitWinSelText']['fg'], theme['quitWinSelText']['bg'])
    curses.init_pair(ThemeColours.QUIT_WIN_SEL_ACCEL_TEXT, theme['quitWinSelAccelText']['fg'],
                     theme['quitWinSelAccelText']['bg'])
    curses.init_pair(ThemeColours.QUIT_WIN_UNSEL_TEXT, theme['quitWinUnselText']['fg'], theme['quitWinUnselText']['bg'])
    curses.init_pair(ThemeColours.QUIT_WIN_UNSEL_ACCEL_TEXT, theme['quitWinUnselAccelText']['fg'],
                     theme['quitWinUnselAccelText']['bg'])

    ############
    # Switch account window:
    curses.init_pair(ThemeColours.SWITCH_WIN, theme['switchWin']['fg'], theme['switchWin']['bg'])
    curses.init_pair(ThemeColours.SWITCH_WIN_BORDER, theme['switchWinBorder']['fg'], theme['switchWinBorder']['bg'])
    curses.init_pair(ThemeColours.SWITCH_WIN_FOCUS_BORDER, theme['switchWinFBorder']['fg'],
                     theme['switchWinFBorder']['bg'])
    curses.init_pair(ThemeColours.SWITCH_WIN_TITLE, theme['switchWinTitle']['fg'], theme['switchWinTitle']['bg'])
    curses.init_pair(ThemeColours.SWITCH_WIN_FOCUS_TITLE, theme['switchWinFTitle']['fg'],
                     theme['switchWinFTitle']['bg'])

    ###############
    # Link account window:
    curses.init_pair(ThemeColours.LINK_WIN, theme['linkWin']['fg'], theme['linkWin']['bg'])
    curses.init_pair(ThemeColours.LINK_WIN_BORDER, theme['linkWinBorder']['fg'], theme['linkWin']['bg'])
    curses.init_pair(ThemeColours.LINK_WIN_FOCUS_BORDER, theme['linkWinFBorder']['fg'], theme['linkWinFBorder']['bg'])
    curses.init_pair(ThemeColours.LINK_WIN_TITLE, theme['linkWinTitle']['fg'], theme['linkWinTitle']['bg'])
    curses.init_pair(ThemeColours.LINK_WIN_FOCUS_TITLE, theme['linkWinFTitle']['fg'], theme['linkWinFTitle']['bg'])
    curses.init_pair(ThemeColours.LINK_WIN_TEXT, theme['linkWinText']['fg'], theme['linkWinText']['bg'])

    ##############
    # Register new account window:
    curses.init_pair(ThemeColours.REGISTER_WIN, theme['regWin']['fg'], theme['regWin']['bg'])
    curses.init_pair(ThemeColours.REGISTER_WIN_BORDER, theme['regWinBorder']['fg'], theme['regWinBorder']['bg'])
    curses.init_pair(ThemeColours.REGISTER_WIN_FOCUS_BORDER, theme['regWinFBorder']['fg'], theme['regWinFBorder']['bg'])
    curses.init_pair(ThemeColours.REGISTER_WIN_TITLE, theme['regWinTitle']['fg'], theme['regWinTitle']['bg'])
    curses.init_pair(ThemeColours.REGISTER_WIN_FOCUS_TITLE, theme['regWinFTitle']['fg'], theme['regWinFTitle']['bg'])

    ###########
    # Shortcut keys help window:
    curses.init_pair(ThemeColours.KEYS_WIN, theme['keysWin']['fg'], theme['keysWin']['bg'])
    curses.init_pair(ThemeColours.KEYS_WIN_BORDER, theme['keysWinBorder']['fg'], theme['keysWinBorder']['bg'])
    curses.init_pair(ThemeColours.KEYS_WIN_FOCUS_BORDER, theme['keysWinFBorder']['fg'], theme['keysWinFBorder']['bg'])
    curses.init_pair(ThemeColours.KEYS_WIN_TITLE, theme['keysWinTitle']['fg'], theme['keysWinTitle']['bg'])
    curses.init_pair(ThemeColours.KEYS_WIN_FOCUS_TITLE, theme['keysWinFTitle']['fg'], theme['keysWinFTitle']['bg'])

    ############
    # About help window:
    curses.init_pair(ThemeColours.ABOUT_WIN, theme['aboutWin']['fg'], theme['aboutWin']['bg'])
    curses.init_pair(ThemeColours.ABOUT_WIN_BORDER, theme['aboutWinBorder']['fg'], theme['aboutWinBorder']['bg'])
    curses.init_pair(ThemeColours.ABOUT_WIN_FOCUS_BORDER, theme['aboutWinFBorder']['fg'],
                     theme['aboutWinFBorder']['bg'])
    curses.init_pair(ThemeColours.ABOUT_WIN_TITLE, theme['aboutWinTitle']['fg'], theme['aboutWinTitle']['bg'])
    curses.init_pair(ThemeColours.ABOUT_WIN_FOCUS_TITLE, theme['aboutWinFTitle']['fg'], theme['aboutWinFTitle']['bg'])

    ##############
    # Versions help window:
    curses.init_pair(ThemeColours.VERSION_WIN, theme['verWin']['fg'], theme['verWin']['bg'])
    curses.init_pair(ThemeColours.VERSION_WIN_BORDER, theme['verWinBorder']['fg'], theme['verWinBorder']['bg'])
    curses.init_pair(ThemeColours.VERSION_WIN_FOCUS_BORDER, theme['verWinFBorder']['fg'], theme['verWinFBorder']['bg'])
    curses.init_pair(ThemeColours.VERSION_WIN_TITLE, theme['verWinTitle']['fg'], theme['verWinTitle']['bg'])
    curses.init_pair(ThemeColours.VERSION_WIN_FOCUS_TITLE, theme['verWinFTitle']['fg'], theme['verWinFTitle']['bg'])
    curses.init_pair(ThemeColours.VERSION_TEXT, theme['verWinText']['fg'], theme['verWinText']['bg'])

    ##########
    # General message window: (NOT USED RN)
    curses.init_pair(ThemeColours.GEN_MESSAGE_WIN, theme['genMsgWin']['fg'], theme['genMsgWin']['bg'])
    curses.init_pair(ThemeColours.GEN_MESSAGE_WIN_BORDER, theme['genMsgWinBorder']['fg'],
                     theme['genMsgWinBorder']['bg'])
    curses.init_pair(ThemeColours.GEN_MESSAGE_WIN_FOCUS_BORDER, theme['genMsgWinFBorder']['fg'],
                     theme['genMsgWinFBorder']['bg'])
    curses.init_pair(ThemeColours.GEN_MESSAGE_WIN_TITLE, theme['genMsgWinTitle']['fg'], theme['genMsgWinTitle']['bg'])
    curses.init_pair(ThemeColours.GEN_MESSAGE_WIN_FOCUS_TITLE, theme['genMsgWinFTitle']['fg'],
                     theme['genMsgWinFTitle']['bg'])

    #############
    # QR-Code display window:
    curses.init_pair(ThemeColours.QRCODE_WIN, theme['qrcodeWin']['fg'], theme['qrcodeWin']['bg'])
    curses.init_pair(ThemeColours.QRCODE_WIN_BORDER, theme['qrcodeWinBorder']['fg'], theme['qrcodeWinBorder']['bg'])
    curses.init_pair(ThemeColours.QRCODE_WIN_FOCUS_BORDER, theme['qrcodeWinFBorder']['fg'],
                     theme['qrcodeWinFBorder']['bg'])
    curses.init_pair(ThemeColours.QRCODE_WIN_TITLE, theme['qrcodeWinTitle']['fg'], theme['qrcodeWinTitle']['bg'])
    curses.init_pair(ThemeColours.QRCODE_WIN_FOCUS_TITLE, theme['qrcodeWinFTitle']['fg'],
                     theme['qrcodeWinFTitle']['bg'])
    curses.init_pair(ThemeColours.QRCODE_TEXT, theme['qrcodeText']['fg'], theme['qrcodeText']['bg'])

    ###############
    # General button properties:
    curses.init_pair(ThemeColours.BUTTON_SEL, theme['buttonSel']['fg'], theme['buttonSel']['bg'])
    curses.init_pair(ThemeColours.BUTTON_UNSEL, theme['buttonUnsel']['fg'], theme['buttonUnsel']['bg'])
    curses.init_pair(ThemeColours.BUTTON_SEL_ACCEL, theme['buttonSelAccel']['fg'], theme['buttonSelAccel']['bg'])
    curses.init_pair(ThemeColours.BUTTON_UNSEL_ACCEL, theme['buttonUnselAccel']['fg'], theme['buttonUnselAccel']['bg'])

    ################
    # General scrollbar properties:
    curses.init_pair(ThemeColours.SCROLL_ENA_BG, theme['scrollBarEnaBg']['bg'], theme['scrollBarEnaBg']['bg'])
    curses.init_pair(ThemeColours.SCROLL_DIS_BG, theme['scrollBarDisBg']['fg'], theme['scrollBarDisBg']['bg'])
    curses.init_pair(ThemeColours.SCROLL_ENA_BTN, theme['scrollBarEnaBtn']['fg'], theme['scrollBarEnaBtn']['bg'])
    curses.init_pair(ThemeColours.SCROLL_DIS_BTN, theme['scrollBarDisBtn']['fg'], theme['scrollBarDisBtn']['bg'])
    curses.init_pair(ThemeColours.SCROLL_ENA_HAND, theme['scrollBarEnaHand']['fg'], theme['scrollBarEnaHand']['bg'])
    curses.init_pair(ThemeColours.SCROLL_DIS_HAND, theme['scrollBarDisHand']['fg'], theme['scrollBarDisHand']['bg'])

    return
