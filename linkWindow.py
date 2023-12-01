#!/usr/bin/env python3
"""
File: linkWindow.py
-> Handle linking messages while linking an existing account.
"""
import curses
from typing import Optional, Callable, Any
from enum import Enum
from common import ROW, HEIGHT, COL, WIDTH, STRINGS, KEYS_ENTER, Focus
from cursesFunctions import calc_attributes, center_string, calc_center_top_left, calc_center_col
from window import Window
from themes import ThemeColours
from typeError import __type_error__
from button import Button


class LinkMessages(Enum):
    """
    Link message selection values.
    """
    GENERATE = 'Generating and encoding link...'
    SUCCESS = 'Successfully linked account.'
    UNKNOWN = 'An unknown error occurred while linking account.'
    EXISTS = 'The account is already linked.'
    TIMEOUT = 'The link process timed-out.'


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
        bg_char: str = theme['backgroundChars']['linkWin']

        # Set the theme attrs:
        window_attrs: int = calc_attributes(ThemeColours.LINK_WIN, theme['linkWin'])
        border_attrs: int = calc_attributes(ThemeColours.LINK_WIN_BORDER, theme['linkWinBorder'])  # NOTE: Not used.
        border_focus_attrs: int = calc_attributes(ThemeColours.LINK_WIN_FOCUS_BORDER, theme['linkWinFBorder'])
        border_chars: dict[str, str] = theme['linkWinBorderChars']
        title_attrs: int = calc_attributes(ThemeColours.LINK_WIN_TITLE, theme['linkWinTitle'])
        title_focus_attrs: int = calc_attributes(ThemeColours.LINK_WIN_FOCUS_TITLE, theme['linkWinFTitle'])
        title_chars: dict[str, str] = theme['linkWinTitleChars']

        self._current_message: LinkMessages = LinkMessages.GENERATE
        """The current message to display."""
        # Calculate size:
        width: int = 0
        for message in iter(LinkMessages):
            width = max(width, len(message.value))
        width += 4
        height: int = 6
        top_left: tuple[int, int] = calc_center_top_left(std_screen.getmaxyx(), (height, width))

        # Make a curses window:
        window = curses.newwin(height, width, top_left[ROW], top_left[COL])

        # Super the window:
        Window.__init__(self, std_screen, window, title, top_left, window_attrs, border_attrs, border_focus_attrs,
                        border_chars, title_attrs, title_focus_attrs, title_chars, bg_char, Focus.LINK)
        # Store the std_screen for resize:
        self._std_screen: curses.window = std_screen
        """The std_screen curses.window object."""
        # Store the text attributes:
        self._text_attrs: int = calc_attributes(ThemeColours.LINK_WIN_TEXT, theme['linkWinText'])
        """The text attributes."""
        # Store show button:
        self._show_button: bool = False
        """Should we show the button?"""
        button_border_chars = theme['linkWinBtnBorderChars']
        button_label = STRINGS['buttonLabels']['okButton']
        button_width = len(button_label) + 2
        button_left: int = calc_center_col(self.size[WIDTH], button_width)
        button_top_left: tuple[int, int] = (self.size[HEIGHT] - 1, button_left)
        self._button = Button(window=self._window,
                              top_left=button_top_left,
                              label=button_label,
                              theme=theme,
                              lead_char='[',
                              tail_char=']',
                              lead_tail_attrs=self._text_attrs,
                              left_click_char_codes=[ord('O'), ord('o')],
                              )
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
        text: str = self._current_message.value
        center_string(self._window, row, text, self._text_attrs)
        self._button.redraw()
        self._window.noutrefresh()
        return

    def resize(self) -> None:
        """
        Resize the link window.
        :return: None
        """
        top_left: tuple[int, int] = calc_center_top_left(self._std_screen.getmaxyx(), self.real_size)
        super().resize((-1, -1), top_left, False, True)
        return

    def process_key(self, char_code: int) -> Optional[bool]:
        """
        Process a key press.
        :param char_code: int: The character code of the key pressed.
        :return: bool: True, the event was handled, False, it was not.
        """
        if self.show_button:
            return_value: Optional[bool] = self._button.process_key(char_code)
            if return_value is not None:
                return False
        return None

##############################
# Properties:
##############################
    @property
    def current_message(self) -> LinkMessages:
        """
        The current message selection.
        :return: LinkMessageSelections: The current selection.
        """
        return self._current_message

    @current_message.setter
    def current_message(self, value: LinkMessages | str) -> None:
        """
        The current message selection.
        Setter.
        :param value: LinkMessageSelections | str: The value to set current selection to.
        :return: None
        :raises ValueError: If value is not a valid LinkMessageSelections string value.
        :raises TypeError: If value is not a LinkMessageSelections item.
        """
        if not isinstance(value, (LinkMessages, str)):
            __type_error__('value', 'LinkMessageSelections | str', value)
        self._current_message = LinkMessages(value)  # Raises ValueError
        return

    @property
    def show_button(self) -> bool:
        """
        Should we show the button?
        :return: bool: True button is visible, False it is not.
        """
        return self._show_button

    @show_button.setter
    def show_button(self, value: bool) -> None:
        """
        Should we show the button?
        Setter.
        :param value: bool: The value to set to.
        :return: None.
        :raises TypeError: On invalid type.
        """
        if not isinstance(value, bool):
            __type_error__('value', 'bool', value)
        self._show_button = value
        self._button.is_visible = value
        return
