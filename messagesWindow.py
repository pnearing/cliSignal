#!/usr/bin/env python3
"""
File: messagesWindow.py
Messages list window handling.
"""
import curses

from common import ROW, COL, calc_attributes
from themes import ThemeColours
from window import Window


class MessagesWindow(Window):
    """
    Class to store the messages' window.
    """
    def __init__(self,
                 size: tuple[int, int],
                 top_left: tuple[int, int],
                 theme: dict[str, dict[str, int | bool]]
                 ) -> None:
        window_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN, theme['msgsWin'])
        border_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_BORDER, theme['msgsWinBorder'])
        title_attrs: int = calc_attributes(ThemeColours.MESSAGES_WIN_TITLE, theme['msgsWinTitle'])
        window = curses.newwin(size[ROW], size[COL], top_left[ROW], top_left[COL])
        Window.__init__(self, window, "Messages", top_left, window_attrs, border_attrs, title_attrs, theme)
        return
