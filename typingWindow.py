#!/usr/bin/env python3
"""
File: typingWindow.py
Message typing area window.
"""
from typing import Optional
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
                 theme: dict[str, dict[str, int | bool | Optional[str]]]
                 ) -> None:
        """
        Initialize the typing window.
        :param size: tuple[int, int]: The size of the window.
        :param top_left: tuple[int, int]: The top left corner of the window.
        :param theme: dict[str, dict[str, int | bool | Optional[str]]]: The theme to use.
        """
        window_attrs: int = calc_attributes(ThemeColours.TYPING_WIN, theme['typeWin'])
        border_attrs: int = calc_attributes(ThemeColours.TYPING_WIN_BORDER, theme['typeWinBorder'])
        border_focus_attrs: int = calc_attributes(ThemeColours.TYPING_WIN_FOCUS_BORDER, theme['typeWinFBorder'])
        title_attrs: int = calc_attributes(ThemeColours.TYPING_WIN_TITLE, theme['typeWinTitle'])
        title_focus_attrs: int = calc_attributes(ThemeColours.TYPING_WIN_FOCUS_TITLE, theme['typeWinFTitle'])
        window = curses.newwin(size[ROW], size[COL], top_left[ROW], top_left[COL])
        Window.__init__(self, window, theme['titles']['typing'], top_left, window_attrs, border_attrs,
                        border_focus_attrs, title_attrs, title_focus_attrs, theme)
        return
