#!/usr/bin/env python3
"""
File: linkWindow.py
Handle linking a phone number to this signal-cli instance.
"""
import curses
from typing import Optional, Callable, Any
from enum import Enum
from common import ROW, ROWS, COL, COLS, STRINGS, calc_attributes, calc_center_top_left, center_string
from window import Window
from themes import ThemeColours
from typeError import __type_error__


class LinkMessageSelections(Enum):
    """
    Link message selection values.
    """
    GENERATE = 'generate'
    SUCCESS = 'success'
    FAILURE = 'failure'


class LinkWindow(Window):
    """
    Handle linking a phone number to this signal-cli process.
    """
    def __init__(self,
                 std_screen: curses.window,
                 theme: dict[str, dict[str, int | bool | str]],
                 ) -> None:
        """
        Initialize the link window.
        :param std_screen: curses.window: The std_screen curses.window object.
        :param theme: dict[str, dict[str, int | bool | str]]: The current theme.
        """
        # Set title and background character:
        title: str = STRINGS['titles']['link']
        bg_char: str = STRINGS['background']['linkWin']

        # Set the theme attrs:
        window_attrs: int = calc_attributes(ThemeColours.LINK_WIN, theme['linkWin'])
        border_attrs: int = calc_attributes(ThemeColours.LINK_WIN_BORDER, theme['linkWinBorder'])  # NOTE: Not used.
        border_focus_attrs: int = calc_attributes(ThemeColours.LINK_WIN_FOCUS_BORDER, theme['linkWinFBorder'])
        border_chars: dict[str, str] = theme['linkWinBorderChars']
        title_attrs: int = calc_attributes(ThemeColours.LINK_WIN_TITLE, theme['linkWinTitle'])
        title_focus_attrs: int = calc_attributes(ThemeColours.LINK_WIN_FOCUS_TITLE, theme['linkWinFTitle'])
        title_chars: dict[str, str] = theme['linkWinTitleChars']

        # Set window contents:
        self._window_messages: dict[LinkMessageSelections, str] = {
            LinkMessageSelections.GENERATE: STRINGS['messages']['linkGen'],
            LinkMessageSelections.SUCCESS: STRINGS['messages']['linkOk'],
            LinkMessageSelections.FAILURE: STRINGS['messages']['linkErr'],
        }

        self._current_message: LinkMessageSelections = LinkMessageSelections.GENERATE

        # Calculate size:
        width: int = 0
        for message in self._window_messages.values():
            width = max(width, len(message))
        width += 4
        height: int = 5
        top_left: tuple[int, int] = calc_center_top_left(std_screen.getmaxyx(), (height, width))

        # Make a curses window:
        window = curses.newwin(height, width, top_left[ROW], top_left[COL])

        # Super the window:
        Window.__init__(self, window, title, top_left, window_attrs, border_attrs, border_focus_attrs, border_chars,
                        title_attrs, title_focus_attrs, title_chars, bg_char)
        self.is_visible = False

        # Store the std_screen for resize:
        self._std_screen: curses.window = std_screen

        # Store the text attributes:
        self._text_attrs: int = calc_attributes(ThemeColours.LINK_WIN_TEXT, theme['linkWinText'])

        # Store show button:
        self.show_button: bool = False
        return

    ############################
    # Overrides:
    ############################
    def redraw(self) -> None:
        """
        Redraw the link window.
        :return: None
        """
        if not self.is_visible:
            return
        # Draw the window and title:
        super().redraw()
        row: int = 2
        text: str = self._window_messages[self._current_message]
        center_string(self._window, row, text, self._text_attrs)
        self._window.noutrefresh()
        return

    def resize(self) -> None:
        """
        Resize the link window.
        :return: None
        """
        top_left = calc_center_top_left(self._std_screen.getmaxyx(), self.real_size)
        super().resize((-1, -1), top_left)
        return

##############################
# Properties:
##############################
    @property
    def current_message(self) -> LinkMessageSelections:
        """
        The current message selection.
        :return: LinkMessageSelections: The current selection.
        """
        return self._current_message

    @current_message.setter
    def current_message(self, value: LinkMessageSelections | str) -> None:
        """
        The current message selection.
        Setter.
        :param value: LinkMessageSelections | str: The value to set current selection to.
        :return: None
        :raises ValueError: If value is not a valid LinkMessageSelections string value.
        :raises TypeError: If value is not a LinkMessageSelections item.
        """
        if not isinstance(value, (LinkMessageSelections, str)):
            __type_error__('value', 'LinkMessageSelections | str', value)
        self._current_message = LinkMessageSelections(value)  # Raises ValueError