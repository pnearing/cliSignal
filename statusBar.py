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
                 std_screen: curses.window,
                 width: int,
                 top_left: tuple[int, int],
                 theme: dict[str, dict[str, bool | int | Optional[str]]]
                 ) -> None:
        """
        Initialize the status bar.
        :param std_screen: curses.window: The window to draw on.
        :param width: int: The width of the bar.
        :param top_left: tuple[int, int]: The top left corner of the status bar.
        :param theme: dict[str, dict[str, int | bool | Optional[str]]]: The theme to use.
        """
        empty_attrs: int = calc_attributes(ThemeColours.STATUS_BAR_EMPTY, theme['statusBG'])
        bg_char: str = STRINGS['background']['statusBar']
        Bar.__init__(self, std_screen, width, top_left, empty_attrs, bg_char)

        # Status indicator show / hide properties:
        self.is_char_code_visible: bool = False

        # Status indicator values to show:
        self._char_code: int = -1
        return

    def redraw(self) -> None:
        """
        Redraw the status bar.
        :return:
        """
        if not self.is_visible:
            return
        super().redraw()
        self._std_screen.move(self.top_left[ROW], self.top_left[COL])
        if self.is_char_code_visible:
            self._std_screen.addstr("-CharCode:%i-" % self.char_code, self._bg_attrs)
        self._std_screen.refresh()
        return

###########################################
# Properties:
###########################################
    @property
    def char_code(self) -> int:
        """
        The character code to display.
        :return: int
        """
        return self._char_code

    @char_code.setter
    def char_code(self, value: int) -> None:
        """
        The character code to display.
        Setter.
        :param value: int: The value to set the char code to.
        :return: None
        """
        self._char_code = value
        self.redraw()
        return
