#!/usr/bin/env pyton3
"""
File: statusBar.py
Maintain and control the status bar.
"""
from typing import Optional
import curses
from themes import ThemeColours
from common import ROW, COL, calc_attributes, STRINGS
from bar import Bar


class StatusBar(Bar):
    """
    Maintain and control a status bar.
    """
    def __init__(self,
                 window: curses.window,
                 width: int,
                 top_left: tuple[int, int],
                 theme: dict[str, dict[str, bool | int | Optional[str]]]
                 ) -> None:
        """
        Initialize the status bar.
        :param window: curses.window: The window to draw on.
        :param width: int: The width of the bar.
        :param top_left: tuple[int, int]: The top left corner of the status bar.
        :param theme: dict[str, dict[str, int | bool | Optional[str]]]: The theme to use.
        """
        empty_attrs: int = calc_attributes(ThemeColours.STATUS_BAR_EMPTY, theme['statusBG'])
        bg_char: str = STRINGS['background']['statusBar']
        Bar.__init__(self, window, width, top_left, empty_attrs, bg_char)
        return

    def redraw(self) -> None:
        """
        Redraw the status bar.
        :return:
        """
        if not self.is_visible:
            return
        super().redraw()
        self._window.refresh()
        return
