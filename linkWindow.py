#!/usr/bin/env python3
"""
File: linkWindow.py
Handle linking a phone number to this signal-cli instance.
"""
import curses
from typing import Optional, Callable, Any
from common import ROW, ROWS, COL, COLS, STRINGS, calc_attributes
from window import Window
from themes import ThemeColours
import SignalCliApi


class LinkWindow(Window):
    """
    Handle linking a phone number to this signal-cli process.
    """
    def __init__(self,
                 size: tuple[int, int],
                 top_left: tuple[int, int],
                 theme: dict[str, dict[str, int | bool | str]],
                 ) -> None:
        """
        Initialize the link window.
        :param window: curses.window: The curses window object.
        :param theme: dict[str, dict[str, int | bool | str]]: The current theme.
        :param callbacks: dict[str, tuple[Optional[Callable], Optional[list[Any]]]]: The call backs for activations.
        """
        # Set title and background character:
        title: str = STRINGS['titles']['link']
        bg_char: str = STRINGS['background']['linkWin']

        # Set the theme attrs:
        window_attrs: int = calc_attributes(ThemeColours.LINK_WIN, theme['linkWin'])
        border_attrs: int = calc_attributes(ThemeColours.LINK_WIN_BORDER, theme['linkWinBorder'])
        border_focus_attrs: int = calc_attributes(ThemeColours.LINK_WIN_FOCUS_BORDER, theme['linkWinFBorder'])
        border_chars: dict[str, str] = theme['linkWinBorderChars']
        title_attrs: int = calc_attributes(ThemeColours.LINK_WIN_TITLE, theme['linkWinTitle'])
        title_focus_attrs: int = calc_attributes(ThemeColours.LINK_WIN_FOCUS_TITLE, theme['linkWinFTitle'])
        title_chars: dict[str, str] = theme['linkWinTitleChars']

        # Make a curses window:
        window = curses.newwin(size[ROWS], size[COLS], top_left[ROW], top_left[COL])

        # Super the window:
        Window.__init__(self, window, title, top_left, window_attrs, border_attrs, border_focus_attrs, border_chars,
                        title_attrs, title_focus_attrs, title_chars, bg_char, False)
        self.is_visible = False
        return

