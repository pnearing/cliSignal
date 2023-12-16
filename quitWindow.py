#!/usr/bin/env python3
"""
File: quitWindow.py
Quit "are you sure?" message.
"""
import logging
from typing import Optional, Final
import curses

import common
from button import Button
from cliExceptions import Quit
from common import ROW, COL, STRINGS, KEYS_ENTER, KEY_ESC, KEY_BACKSPACE, Focus
from cursesFunctions import calc_center_top_left, calc_attributes, center_string, get_rel_mouse_pos
from themes import ThemeColours
from typeError import __type_error__
from window import Window


class QuitWindow(Window):
    """
    The quit "Are you sure?" message window.
    """
    ##########################################
    # Initialize:
    ##########################################
    def __init__(self,
                 std_screen: curses.window,
                 theme: dict[str, dict[str, int | bool | str]]
                 ) -> None:
        """
        Initialize the quit window.
        :param std_screen: curses.window: The std_screen window.
        :param theme: dict[str, dict[str, int | bool | str]]: The current theme.
        """
        # Set title and background character.
        title: str = STRINGS['titles']['quit']
        bg_char: str = theme['backgroundChars']['quitWin']

        # Set the theme attrs:
        window_attrs: int = calc_attributes(ThemeColours.QUIT_WIN, theme['quitWin'])
        border_attrs: int = calc_attributes(ThemeColours.QUIT_WIN_BORDER, theme['quitWinBorder'])
        border_focus_attrs: int = calc_attributes(ThemeColours.QUIT_WIN_FOCUS_BORDER, theme['quitWinFBorder'])
        border_chars: dict[str, str] = theme['quitWinBorderChars']
        border_focus_chars: dict[str, str] = theme['quitWinFBorderChars']
        title_attrs: int = calc_attributes(ThemeColours.QUIT_WIN_TITLE, theme['quitWinTitle'])
        title_focus_attrs: int = calc_attributes(ThemeColours.QUIT_WIN_FOCUS_TITLE, theme['quitWinFTitle'])
        title_chars: dict[str, str] = theme['quitWinTitleChars']
        title_focus_chars: dict[str, str] = theme['quitWinFTitleChars']

        # Window contents:
        self._confirm_message: str = STRINGS['messages']['quit']

        # Calculate window size:
        width: int = len(self._confirm_message) + 4
        height: int = 6

        # Calculate top_left:
        containing_size: tuple[int, int] = std_screen.getmaxyx()
        top_left: tuple[int, int] = calc_center_top_left(containing_size, (height, width))
        # Make a curses window:
        window = curses.newwin(height, width, top_left[ROW], top_left[COL])

        # Super the window:
        Window.__init__(self, std_screen, window, title, top_left, window_attrs, border_attrs, border_focus_attrs,
                        border_chars, border_focus_chars, title_attrs, title_focus_attrs, title_chars,
                        title_focus_chars, bg_char, Focus.QUIT)

        # Set the text attributes:
        self._text_attrs: int = calc_attributes(ThemeColours.QUIT_WIN_TEXT, theme['quitWinText'])
        """Quit window text attributes."""
        center_col = int(width / 2)
        # Create the yes button:
        self._yes_button: Final[Button] = Button(
            window=window,
            top_left=(4, center_col - 7),
            label=STRINGS['other']['yes'],
            theme=theme,
            callback=(self._yes_click_cb, None),
            left_click_char_codes=(ord('y'), ord('Y')),
            )
        """The yes button object."""
        self._no_button: Final[Button] = Button(
            window=window,
            top_left=(4, center_col + 1),
            label=STRINGS['other']['no'],
            theme=theme,
            lead_tail_attrs=self._text_attrs,
            callback=(self._no_click_cb, None),
            left_click_char_codes=(ord('n'), ord('N'))
        )
        """The no button object."""

        # Set the buttons visible:
        self._yes_button.is_visible = True
        self._no_button.is_visible = True

        # Current default selection between yes and no for are you sure message:
        self._yes_button.is_selected = True
        self._yes_selected: bool = True
        """If yes is selected."""

        return

    #####################################
    # Overrides:
    #####################################
    def redraw(self) -> None:
        """
        Redraw the window:
        :return: None
        """
        if not self.is_visible:
            return
        # Draw the border, title, and background:
        super().redraw()

        # # Add the message to the window:
        center_string(self._window, 2, self._confirm_message, self._text_attrs)
        self._yes_button.redraw()
        self._no_button.redraw()
        self._window.noutrefresh()
        return

    def resize(self) -> None:
        """
        Resize the quit window.
        :return: None
        """
        top_left: tuple[int, int] = calc_center_top_left(self._std_screen.getmaxyx(), self.real_size)
        super().resize(None, top_left, False, True)
        return

    def process_key(self, char_code: int) -> Optional[bool]:
        """
        Process a key press given the character code.
        :param char_code: int: The character code of the key pressed.
        :return: bool: True, the user wants to quit, False, the user doesn't want to quit, and None if not handled.
        """
        return_value: Optional[bool]
        # Pass the key to the yes button:
        if self.yes_selected:
            return_value = self._yes_button.process_key(char_code)
            if return_value is True:  # User wants to quit.
                raise Quit()
        # Pass the key to the no button:
        else:
            return_value = self._no_button.process_key(char_code)
            if return_value is False:  # User doesn't want to quit.
                return False

        # Process the key press:
        if char_code in KEYS_ENTER:
            if self._yes_selected:
                raise Quit()
            else:
                return False
        elif char_code in (KEY_ESC, KEY_BACKSPACE):
            return False
        elif char_code in (curses.KEY_LEFT, curses.KEY_RIGHT):
            self.yes_selected = not self.yes_selected
            return True
        return None

    def process_mouse(self, mouse_pos: tuple[int, int], button_state: int) -> Optional[bool]:
        """
        Process a mouse event.
        :param mouse_pos: tuple[int, int]: The current mouse position: (ROW, COL).
        :param button_state: int: The current button state.
        :return: Optional[bool]: Return True, mouse handled, processing should stop, Return False, close the window, and
            processing should stop, return None, the character wasn't handled, and processing should continue.
        """
        # Declare vars:
        return_value: Optional[bool]

        # Get the relative mouse position:
        rel_mouse_pos = get_rel_mouse_pos(mouse_pos, self.real_top_left)

        # Pass the mouse to the yes button:
        return_value = self._yes_button.process_mouse(rel_mouse_pos, button_state)
        if return_value is True:
            raise Quit()

        # Pass the mouse to the no button:
        return_value = self._no_button.process_mouse(rel_mouse_pos, button_state)
        if return_value is False:
            return False

        # Parse mouse movement:
        if common.SETTINGS['mouseMoveFocus']:
            if self._yes_button.is_mouse_over(rel_mouse_pos):
                self.yes_selected = True
            elif self._no_button.is_mouse_over(rel_mouse_pos):
                self.yes_selected = False
        return None

    def _yes_click_cb(self, *args) -> Optional[bool]:
        """
        The callback for the yes button.
        :param state: str: The button state, one of 'common.CBStates'.
        :param args: Any additional arguments.
        :return: Optional[bool]
        """
        logger: logging.Logger = logging.getLogger(__name__ + '.' + self._yes_click_cb.__name__)
        logger.debug(args[0])
        return True

    def _no_click_cb(self, *args) -> Optional[bool]:
        """
        The callback for the no button.
        :param state: The button state, one of 'common.CBStates'.
        :param args: Any additional arguments
        :return: Optional[bool]:
        """
        logger: logging.Logger = logging.getLogger(__name__ + '.' + self._no_click_cb.__name__)
        logger.debug(args[0])
        return False

##########################################
# Properties:
##########################################
    @property
    def yes_selected(self) -> bool:
        """
        Is the 'yes' button selected?
        :return: bool: True the 'yes' button is selected, False it is not.
        """
        return self._yes_selected

    @yes_selected.setter
    def yes_selected(self, value: bool) -> None:
        """
        Is the 'yes' button selected?
        :param value: bool: The value to set.
        :return: None.
        :raises TypeError: If value is not a bool.
        """
        if not isinstance(value, bool):
            __type_error__('value', 'bool', value)
        self._yes_selected = value
        if value:
            self._yes_button.is_selected = True
            self._no_button.is_selected = False
        else:
            self._yes_button.is_selected = False
            self._no_button.is_selected = True
