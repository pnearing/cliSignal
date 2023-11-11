#!/usr/bin/env python3
"""
File: quitWindow.py
Quit "are you sure?" message.
"""
from typing import Optional
import curses
from common import ROW, ROWS, COL, COLS, calc_attributes, STRINGS
from themes import ThemeColours
from window import Window

class QuitWindow(Window):
    """
    The quit "Are you sure?" message window.
    """
    def __init__(self,
                 size: tuple[int, int],
                 top_left: tuple[int, int],
                 theme: dict[str, dict[str, int | bool | str]]
                 ) -> None:
        """
        Initialize the quit window.
        :param size: tuple[int, int]: The size of the window: (ROWS, COLS).
        :param top_left: tuple[int, int]: The top left corner of the window: (ROW, COL).
        :param theme: dict[str, dict[str, int | bool | str]]: The current theme.
        """
        # Set title and background character.
        title: str = STRINGS['titles']['quit']
        bg_char: str = STRINGS['background']['quitWin']

        # Set the theme attrs:
        window_attrs: int = calc_attributes(ThemeColours.QUIT_WIN, theme['quitWin'])
        border_attrs: int = calc_attributes(ThemeColours.QUIT_WIN_BORDER, theme['quitWinBorder'])
        border_focus_attrs: int = calc_attributes(ThemeColours.QUIT_WIN_FOCUS_BORDER, theme['quitWinFBorder'])
        border_chars: dict[str, str] = theme['quitWinBorderChars']
        title_attrs: int = calc_attributes(ThemeColours.QUIT_WIN_TITLE, theme['quitWinTitle'])
        title_focus_attrs: int = calc_attributes(ThemeColours.QUIT_WIN_FOCUS_TITLE, theme['quitWinFTitle'])
        title_chars: dict[str, str] = theme['quitWinTitleChars']

        # Make a curses window:
        window = curses.newwin(size[ROWS], size[COLS], top_left[ROW], top_left[COL])

        # Super the window:
        Window.__init__(self, window, title, top_left, window_attrs, border_attrs, border_focus_attrs,
                        border_chars, title_attrs, title_focus_attrs, title_chars, bg_char, False,
                        True)
        # Set this by default as invisible.
        self.is_visible = False
        return
