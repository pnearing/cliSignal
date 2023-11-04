#!/usr/bin/env python3
"""
File: typingWindow.py
Message typing area window.
"""
import curses
from common import ROW, COL, calc_attributes
from themes import ThemeColours
from window import Window


class TypingWindow(Window):
    """
    Message typing window. You know, where you type your message. I didn't know what else to call it.
    """
    def __init__(self,
                 size: tuple[int, int],
                 top_left: tuple[int, int],
                 theme: dict[str, dict[str, int | bool]]
                 ) -> None:
        """

        :param size:
        :param top_left:
        :param theme:
        """
        window_attrs: int = calc_attributes(ThemeColours.TYPING_WIN, theme['typeWin'])
        border_attrs: int = calc_attributes(ThemeColours.TYPING_WIN_BORDER, theme['typeWinBorder'])
        title_attrs: int = calc_attributes(ThemeColours.TYPING_WIN_TITLE, theme['typeWinTitle'])
        window = curses.newwin(size[ROW], size[COL], top_left[ROW], top_left[COL])
        Window.__init__(self, window, None, top_left, window_attrs, border_attrs, title_attrs, theme)
        return
