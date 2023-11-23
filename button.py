#!/usr/bin/env python3
"""
File: button.py
-> Store, handle, and display a button.
"""

import curses
import logging
from typing import Optional, Callable, Any, Final
from themes import ThemeColours
from common import ROW, HEIGHT, COL, WIDTH, ButtonCBKeys, CBStates, __run_callback__
from cursesFunctions import add_accel_text, calc_attributes
from typeError import __type_error__
from cliExceptions import ParameterError


class Button(object):
    """
    Class to handle a button.
    """

    def __init__(self,
                 window: curses.window,
                 top_left: tuple[int, int],
                 label: str,
                 theme: dict[str, dict[str, int | bool | str]],
                 border_lead_char: Optional[str],
                 border_tail_char: Optional[str],
                 border_attrs: Optional[int],
                 click_callback: Optional[tuple[Callable, Optional[list[Any]] | tuple[Any, ...]]],
                 double_click_callback: Optional[tuple[Callable, Optional[list[Any] | tuple[Any, ...]]]],
                 click_char_codes: Optional[list[int]],
                 double_click_char_codes: Optional[list[int]],
                 ) -> None:
        """
        Initialize a button.
        :param window: curses.window: The window to draw to.
        :param top_left: tuple[int, int]: The top left corner of the button: (ROW, COL).
        :param label: str: The accelerator-enabled text.
        :param theme: dict[str, dict[str, int | bool | str]]: The current theme in use.
        :param border_lead_char: Optional[str]: The start character, if None, it's not printed.
        :param border_tail_char: Optional[str]: The end character, if None it's not printed.
        :param border_attrs: Optional[int]: The attributes to use for the start and end characters.
        :param click_callback: Optional[tuple[Callable, Optional[list[Any] | tuple[Any]]]]: The on_click callback.
            If it is None, no callback is run, otherwise it's a tuple where the first element is the Callable abject,
            and the second element is Optionally a list or tuple of any params to the callback. The callback should
            return a boolean where if True, the handling of the key / mouse is stopped, and if False, the handling of
            the key / mouse continues.
        :param double_click_callback:Optional[tuple[Callable, Optional[list[Any]]]]: The on_double_click callback.
            If it is None, no callback is run, otherwise it's a tuple where the first element is the Callable abject,
            and the second element is Optionally a list or tuple of any params to the callback. The callback should
            return a boolean where if True, the handling of the key / mouse is stopped, and if False, the handling of
            the key / mouse continues.
        :param click_char_codes: Optional[list[int]]: Character codes that cause the 'on_click' action to be activated.
        :param double_click_char_codes: Optional[list[int]]: Character codes that cause the 'on_double_click' action
            to be activated.
        """
        # Setup logging:
        logger: logging.Logger = logging.getLogger(__name__ + '.' + self.__init__.__name__)
        if border_lead_char is not None and border_tail_char is None:
            raise ParameterError('border_lead_char', "If not None, border_tail_char must not be None.")
        elif border_tail_char is not None and border_lead_char is None:
            raise ParameterError('border_tail_char', "If not None border_lead_char must not be None.")
        if border_attrs is not None:
            if border_lead_char is None and border_tail_char is None:
                raise ParameterError('border_attrs', 'If using border characters, border_attrs must not be None.')

        # Private properties:
        self._window: Final[curses.window] = window
        """The curses window to draw on."""
        self._label: Final[str] = label
        """The accelerated label text."""
        self._click_callback: Final[Optional[tuple[Callable, Optional[list[Any]]]]] = click_callback
        """The on_click callback of the button."""
        self._double_click_callback: Final[Optional[tuple[Callable, Optional[list[Any]]]]] = double_click_callback
        self._border_lead_char: Final[Optional[str]] = border_lead_char
        """The border lead character of the button."""
        self._border_tail_char: Final[Optional[str]] = border_tail_char
        """The border tail character of the button."""
        self._border_attrs: Final[Optional[int]] = border_attrs
        """The border attributes to use."""
        self._sel_attrs: Final[int] = calc_attributes(ThemeColours.BUTTON_SEL, theme['buttonSel'])
        """The selected text attributes."""
        self._sel_accel_attrs: Final[int] = calc_attributes(ThemeColours.BUTTON_SEL_ACCEL, theme['buttonSelAccel'])
        """The selected accelerator text attributes."""
        self._unsel_attrs: Final[int] = calc_attributes(ThemeColours.BUTTON_UNSEL, theme['buttonUnsel'])
        """The unselected text attributes."""
        self._unsel_accel_attrs: Final[int] = calc_attributes(ThemeColours.BUTTON_UNSEL_ACCEL,
                                                              theme['buttonUnselAccel'])
        """The unselected accelerator attributes."""
        self._sel_chars: Final[dict[str, str]] = theme['buttonSelChars']
        """The selection indicator characters."""
        self._is_selected: bool = False
        """Is this button selected?"""
        self._is_visible: bool = False
        """Is this button visible?"""
        self._click_chars_codes: Optional[list[int]] = click_char_codes
        """Character codes that cause the 'on_click' action to be fired in process_key."""
        self._double_click_char_codes: Optional[list[int]] = double_click_char_codes
        """Character codes that cause the 'on_double_click' action to be fired in process key."""

        # Public properties:
        self.real_top_left: tuple[int, int] = (-1, -1)
        """The real top left of this button."""
        self.top_left: tuple[int, int] = (-1, -1)
        """The top left corner of this button."""
        self.real_size: tuple[int, int] = (-1, -1)
        """The real size of the button."""
        self.size: tuple[int, int] = (-1, -1)
        """The size of this button."""
        self.real_bottom_right: tuple[int, int] = (-1, -1)
        """The real bottom right of this button."""
        self.bottom_right: tuple[int, int] = (-1, -1)
        """The bottom right corner of this button."""
        self.resize(top_left)
        return

    def redraw(self) -> None:
        """
        Redraw this button.
        :return: None.
        """
        # If we're not visible, return:
        if not self.is_visible:
            return
        # Determine attrs and indicator characters:
        text_attrs: int
        accel_attrs: int
        indicator_lead: str
        indicator_tail: str
        if self.is_selected:
            text_attrs = self._sel_attrs
            accel_attrs = self._sel_accel_attrs
            indicator_lead = self._sel_chars['leadSel']
            indicator_tail = self._sel_chars['tailSel']
        else:
            text_attrs = self._unsel_attrs
            accel_attrs = self._unsel_accel_attrs
            indicator_lead = self._sel_chars['leadUnsel']
            indicator_tail = self._sel_chars['tailUnsel']

        # Move the cursor:
        self._window.move(self.top_left[ROW], self.top_left[COL])
        # Add the border lead char:
        if self._border_lead_char is not None:
            self._window.addstr(self._border_lead_char, self._border_attrs)
        # Add the lead indicator char:
        self._window.addstr(indicator_lead, text_attrs)
        # Add the label:
        add_accel_text(self._window, self._label, text_attrs, accel_attrs)
        # Add the tail indicator char:
        self._window.addstr(indicator_tail, text_attrs)
        # Add the border tail char:
        if self._border_tail_char is not None:
            self._window.addstr(self._border_tail_char, self._border_attrs)
        return

    def resize(self, top_left: tuple[int, int]) -> None:
        """
        Resize the button:
        :param top_left: tuple[int, int]: The new top left corner of the button.
        :return: None
        """
        # Calculate top-left and real top-left:
        self.real_top_left = top_left
        if self._border_lead_char is not None:
            self.top_left = (top_left[ROW], top_left[COL] + 1)
        else:
            self.top_left = top_left

        # Calculate width:
        if self._border_lead_char is not None:
            real_width = (len(self._label) - 2) + 4
            width = real_width - 2
        else:
            self.top_left = top_left
            real_width = (len(self._label) - 2) + 2
            width = real_width

        # Calculate size and real size:
        self.real_size = (1, real_width)
        self.size = (1, width)

        # Calculate bottom-right, and real bottom-right:
        self.real_bottom_right = (self.real_top_left[ROW], self.real_top_left[COL] + real_width)
        self.bottom_right = (self.top_left[ROW], self.top_left[COL] + width)
        return

    def is_mouse_over(self, mouse_pos: tuple[int, int]) -> bool:
        """
        Is the mouse over this button?
        :param mouse_pos: tuple[int, int]: The mouse position: (ROW, COL).
        :return: bool: True the given mouse position is over this button, False it's not.
        """
        if self.top_left[ROW] <= mouse_pos[ROW] <= self.bottom_right[ROW]:
            if self.top_left[COL] <= mouse_pos[COL] <= self.bottom_right[COL]:
                return True
        return False

    def process_key(self, char_code: int) -> bool:
        """
        Process a key press.
        :param char_code: int: The character code of the key pressed.
        :return: bool: True this has been handled, False it has not been handled.
        """
        if self._click_chars_codes is not None and char_code in self._click_chars_codes:
            if self._click_callback is not None:
                return __run_callback__(self._click_callback, CBStates.ACTIVATED.value)
            return True
        elif self._double_click_char_codes is not None and char_code in self._double_click_char_codes:
            # Run 'on_double_click' callback:
            if self._double_click_callback is not None:
                return __run_callback__(self._double_click_callback, CBStates.ACTIVATED.value)
            return True
        return False

    def process_mouse(self, mouse_pos: tuple[int, int], button_state: int) -> bool:
        """
        Process a mouse event.
        :param mouse_pos: tuple[int, int]: The mouse position: (ROW, COL).
        :param button_state: int: The button state.
        :return: bool: True the mouse event has been handled, False it has not.
        """

        clicked: bool = bool(button_state & (curses.BUTTON1_CLICKED | curses.BUTTON1_PRESSED | curses.BUTTON3_CLICKED
                                             | curses.BUTTON3_PRESSED))
        double_clicked: bool = bool(button_state & (curses.BUTTON1_DOUBLE_CLICKED | curses.BUTTON3_DOUBLE_CLICKED))

        if clicked or double_clicked and self.is_mouse_over(mouse_pos):
            logger: logging.Logger = logging.getLogger(__name__ + '.' + self.process_mouse.__name__)
            if clicked:
                if self._click_callback is not None:
                    logger.debug("Running callback 'on_click'...")
                    return __run_callback__(self._click_callback, CBStates.ACTIVATED.value)
                return True  # Assume if no callback, the mouse was handled.
            elif double_clicked:
                if self._double_click_callback is not None:
                    logger.debug("Running callback 'on_double_click'...")
                    return_value: Any = __run_callback__(self._double_click_callback, CBStates.ACTIVATED.value)
                return True  # Assume if no callback, the mouse was handled.
        return False  # The mouse was not handled.

    ##############################
    # Properties:
    ##############################
    @property
    def is_selected(self) -> bool:
        """
        Is this button selected?
        :return: bool: True button selected, False button unselected.
        """
        return self._is_selected

    @is_selected.setter
    def is_selected(self, value: bool) -> None:
        """
        Is this button selected?
        Setter.
        :param value: bool: The value to set to.
        :return: None
        """
        if not isinstance(value, bool):
            __type_error__("value", "bool", value)
        old_value = self._is_selected
        self._is_selected = value
        if old_value != value:
            self.redraw()
        return

    @property
    def is_visible(self) -> bool:
        """
        Is this button visible?
        :return: bool: True, the button is visible, False the button is not visible.
        """
        return self._is_visible

    @is_visible.setter
    def is_visible(self, value: bool) -> None:
        """
        Is this button visible?
        Setter.
        :param value: bool: The value to set the property to.
        :return: None
        """
        if not isinstance(value, bool):
            __type_error__('value', 'bool', value)
        old_value: bool = value
        self._is_visible = value
        if old_value is False and value is True:
            self.redraw()
        return
