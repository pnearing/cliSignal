#!/usr/bin/env python3
"""
File: messagesWindow.py
Messages list window handling.
"""
from typing import Optional
import curses
from common import ROW, COL, STRINGS, Focus
from cursesFunctions import calc_attributes
from themes import ThemeColours
from window import Window


class MessagesWindow(Window):
    """
    Class to store the messages' window.
    """
    def __init__(self,
                 std_screen: curses.window,
                 size: tuple[int, int],
                 top_left: tuple[int, int],
                 theme: dict[str, dict[str, int | bool | str]]
                 ) -> None:
        """
        Initialize the messages window.
        :param size: tuple[int, int]: The size of the window: (ROWS, COLS).
        :param top_left: tuple[int, int]: The top left corner of the window: (ROW, COL).
        :param theme: dict[str, dict[str, int | bool | str]]: The current theme.
        """
        # Set title and background character:
        title: str = STRINGS['titles']['messages']
        bg_char: str = theme['backgroundChars']['messagesWin']

        # Set theme attrs and strings:
        window_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN, theme['msgsWin'])
        border_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_BORDER, theme['msgsWinBorder'])
        border_focus_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_FOCUS_BORDER, theme['msgsWinFBorder'])
        border_chars: dict[str, str] = theme['msgsWinBorderChars']
        title_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_TITLE, theme['msgsWinTitle'])
        title_focus_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_FOCUS_TITLE, theme['msgsWinFTitle'])
        title_chars: dict[str, str] = theme['msgsWinTitleChars']

        # Create the curses window:
        window = curses.newwin(size[ROW], size[COL], top_left[ROW], top_left[COL])

        # Run Super:
        Window.__init__(self, std_screen, window, title, top_left, window_attrs, border_attrs, border_focus_attrs,
                        border_chars, title_attrs, title_focus_attrs, title_chars, bg_char, Focus.MESSAGES)

        # Set this window as always visible:
        self.always_visible = True
        self.is_static_size = False
        return

