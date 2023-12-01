#!/usr/bin/env pyton3
"""
File: statusBar.py
Maintain and control the status bar.
"""
import logging
from typing import Optional
import curses
from themes import ThemeColours
from common import ROW, COL, STRINGS, Focus
from cursesFunctions import calc_attributes
from bar import Bar
from typeError import __type_error__


class StatusBar(Bar):
    """
    Maintain and control a status bar.
    """

    def __init__(self,
                 std_screen: curses.window,
                 top_left: tuple[int, int],
                 theme: dict[str, dict[str, bool | int | Optional[str]]]
                 ) -> None:
        """
        Initialize the status bar.
        :param std_screen: curses.window: The window to draw on.
        :param top_left: tuple[int, int]: The top left corner of the status bar.
        :param theme: dict[str, dict[str, int | bool | Optional[str]]]: The theme to use.
        """
        empty_attrs: int = calc_attributes(ThemeColours.STATUS_BAR_EMPTY, theme['statusBG'])
        bg_char: str = theme['backgroundChars']['statusBar']

        Bar.__init__(self, std_screen, top_left[ROW], empty_attrs, bg_char, Focus.STATUS_BAR)
        # Status indicator attrs:
        self._char_code_attrs: int = calc_attributes(ThemeColours.STATUS_BAR_CHAR, theme['statusCC'])
        self._mouse_attrs: int = calc_attributes(ThemeColours.STATUS_BAR_MOUSE, theme['statusMouse'])
        self._receive_attrs: int = calc_attributes(ThemeColours.STATUS_RECEIVE, theme['statusReceive'])

        self.receive_started_char = theme['receiveStateChars']['started']
        self.receive_stopped_char = theme['receiveStateChars']['stopped']

        # Status indicator show / hide properties:
        self.is_char_code_visible: bool = False
        self.is_mouse_visible: bool = False

        # Status indicator values to show:
        self._char_code: int = -1
        self._mouse_pos: tuple[int, int] = (-1, -1)
        self._mouse_button_state: int = -1
        self._receive_state: bool = False
        return

    def redraw(self) -> None:
        """
        Redraw the status bar.
        :return:
        """
        logger: logging.Logger = logging.getLogger(__name__ + '.' + self.redraw.__name__)
        if not self.is_visible:
            return
        super().redraw()
        # Move the cursor to the beginning of the window:
        self._window.move(self.top_left[ROW], self.top_left[COL])

        # Redraw the receive state:
        self._window.addstr("Recv:", self._receive_attrs)
        if self._receive_state:
            self._window.addstr(self.receive_started_char, self._receive_attrs)
        else:
            self._window.addstr(self.receive_stopped_char, self._receive_attrs)
        # Redraw the character code:
        if self.is_char_code_visible:
            char_code_str: str = f"-\U0001F5AE:{self.char_code:4d}-"
            self._window.addstr(char_code_str, self._char_code_attrs)
        # Redraw the mouse info:
        if self.is_mouse_visible:
            mouse_row = self.mouse_pos[ROW]
            mouse_col = self.mouse_pos[COL]
            mouse_pos_string = f"({mouse_row:4d},{mouse_col:4d})"
            mouse_button_string = f"{self.mouse_button_state:11d}"
            self._window.addstr("-\U0001f5b1:%s:%s-" % (mouse_pos_string, mouse_button_string),
                                self._mouse_attrs)
        self._window.noutrefresh()
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
        if old_value != value and self.is_visible:
            self.redraw()
            curses.doupdate()
        return

    @property
    def mouse_pos(self) -> tuple[int, int]:
        """
        Mouse position.
        :return: tuple[int, int]: Mouse position in (ROW, COL) format.
        """
        return self._mouse_pos

    @mouse_pos.setter
    def mouse_pos(self, value: tuple[int, int]) -> None:
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
        if old_value != value and self.is_visible:
            self.redraw()
            curses.doupdate()
        return

    @property
    def mouse_button_state(self) -> int:
        """
        Mouse button state.
        :return: int: The button state.
        """
        return self._mouse_button_state

    @mouse_button_state.setter
    def mouse_button_state(self, value: int) -> None:
        """
        The mouse button state.
        Setter.
        :param value: int: The current button state.
        :return: None.
        """
        if not isinstance(value, int):
            __type_error__("value", 'int', value)
        old_value: int = self._mouse_button_state
        self._mouse_button_state = value
        if old_value != value and self.is_visible:
            self.redraw()
            curses.doupdate()
        return
