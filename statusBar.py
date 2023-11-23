#!/usr/bin/env pyton3
"""
File: statusBar.py
Maintain and control the status bar.
"""
import logging
from typing import Optional
import curses
from themes import ThemeColours
from common import ROW, COL, STRINGS
from cursesFunctions import calc_attributes
from bar import Bar
from typeError import __type_error__


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
        bg_char: str = theme['backgroundChars']['statusBar']

        Bar.__init__(self, std_screen, width, top_left, empty_attrs, bg_char)
        # Status indicator attrs:
        self._char_code_attrs: int = calc_attributes(ThemeColours.STATUS_BAR_CC, theme['statusCC'])
        self._mouse_attrs: int = calc_attributes(ThemeColours.STATUS_BAR_MOUSE, theme['statusMouse'])

        # Status indicator show / hide properties:
        self.is_char_code_visible: bool = False
        self.is_mouse_visible: bool = False

        # Status indicator values to show:
        self._char_code: int = -1
        self._mouse_pos: tuple[int, int] = (-1, -1)
        return

    def redraw(self) -> None:
        """
        Redraw the status bar.
        :return:
        """
        logger: logging.Logger = logging.getLogger(__name__ + '.' + self.redraw.__name__)
        if not self.is_visible:
            return

        rows, cols = self._std_screen.getmaxyx()
        # if self.top_left[ROW] >= rows - 1 or self.top_left[COL] + self.width >= cols - 1:
        if self.top_left[ROW] >= rows - 1:
            logger.debug("top_left[ROW]:%i >= max_row:%i or top_left[COL]+ self.width:%i >= max_col:%i"
                         % (self.top_left[ROW], rows - 1, self.top_left[COL] + self.width, cols - 1))
            return

        super().redraw()
        self._std_screen.move(self.top_left[ROW], self.top_left[COL])
        if self.is_char_code_visible:
            char_code_str: str = f"-\U0001F5AE:{self.char_code:4d}-"
            self._std_screen.addstr(char_code_str, self._char_code_attrs)
        if self.is_mouse_visible:
            self._std_screen.addstr("-\U0001f5b1(R,C):%s-" % str(self.mouse_pos), self._mouse_attrs)
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
        if not isinstance(value, int):
            raise __type_error__('value', 'int', value)
        old_value = self._char_code
        self._char_code = value
        if old_value != value:
            self.redraw()
        return

    @property
    def mouse_pos(self) -> tuple[int, int]:
        """
        Mouse position.
        :return: tuple[int, int]: Mouse position in (ROW, COL) format.
        """
        return self._mouse_pos

    @mouse_pos.setter
    def mouse_pos(self, value):
        """
        Mouse position
        Setter.
        :param value: tuple[int, int]: The position to set to: (ROW, COL).
        :return: None
        """
        if not isinstance(value, tuple):
            __type_error__('value', 'tuple[int, int]', value)
        elif len(value) != 2:
            raise ValueError("value must have only 2 elements.")
        elif not isinstance(value[0], int):
            __type_error__('value[0]', 'int', value[0])
        elif not isinstance(value[1], int):
            __type_error__('value[1]', 'int', value[1])
        old_value = self._mouse_pos
        self._mouse_pos = value
        if old_value != value:
            self.redraw()
        return
