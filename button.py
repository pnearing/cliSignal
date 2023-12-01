#!/usr/bin/env python3
"""
File: button.py
-> Store, handle, and display a button.
"""

import curses
import logging
from typing import Optional, Callable, Any, Final, Iterable
from themes import ThemeColours
from common import ROW, HEIGHT, COL, WIDTH, CBStates, __type_check_position_or_size__, KEYS_ENTER
from cursesFunctions import add_accel_text, calc_attributes, get_left_click, get_left_double_click, get_right_click, \
    get_right_double_click
import typeError
from typeError import __type_error__
from runCallback import __run_callback__, __type_check_callback__, type_string
from cliExceptions import ParameterError

typeError.use_logging = True


class Button(object):
    """
    Class to handle a button.
    """

    def __init__(self,
                 window,  # Type: curses._CursesWindow | curses.window
                 top_left: tuple[int, int],
                 label: str,
                 theme: dict[str, dict[str, int | bool | str]],
                 lead_char: Optional[str] = None,
                 tail_char: Optional[str] = None,
                 lead_tail_attrs: Optional[int] = None,
                 callback: Optional[tuple[Callable, Optional[list[Any]] | tuple[Any, ...]]] = None,
                 left_click_char_codes: Optional[Iterable[int]] = None,
                 left_double_click_char_codes: Optional[Iterable[int]] = None,
                 right_click_char_codes: Optional[Iterable[int]] = None,
                 right_double_click_char_codes: Optional[Iterable[int]] = None,
                 enter_runs_callback_state: CBStates = CBStates.LEFT_CLICK,
                 ) -> None:
        """
        Initialize a button.
        :param window: curses.window: The window to draw to.
        :param top_left: tuple[int, int]: The top left corner of the button: (ROW, COL).
        :param label: str: The accelerator-enabled text.
        :param theme: dict[str, dict[str, int | bool | str]]: The current theme in use.
        :param lead_char: Optional[str]: The start character, if None, it's not printed.
        :param tail_char: Optional[str]: The end character, if None it's not printed.
        :param lead_tail_attrs: Optional[int]: The attributes to use for the start and end characters.
        :param callback: Optional[tuple[Callable, Optional[list[Any] | tuple[Any]]]]: The callback.
            If it is None, no callback is run, otherwise it's a tuple where the first element is the Callable abject,
            and the second element is Optionally a list or tuple of any params to the callback. The callback should
            return an Optional[bool]; Which has multiple meanings depending on where it's called. The return value of
            the callback will be returned through to process_key or process_mouse accordingly. The signature of the
            callback should be: some_callback(state: str, *args)
        :param left_click_char_codes: Optional[list[int]]: Character codes that cause the 'on_left_click' action to be
            activated.
        :param left_double_click_char_codes: Optional[list[int]]: Character codes that cause the 'on_left_double_click'
            action to be activated.
        :param right_click_char_codes: Optional[list[int]]: Character codes that cause the 'on_right_click' action to
            be activated.
        :param right_double_click_char_codes: Optional[list[int]]: Character codes that cause the
            'on_right_double_click' action to be activated.
        :param enter_runs_callback_state: Optional[CBStates]: The callback state that enter runs, defaults to CBState.LEFT_CLICK.
        :raises TypeError: If a parameter is of the wrong type.
        :raises ParameterError: If a parameter conflict occurs.
        """
        # Setup logging:
        logger: logging.Logger = logging.getLogger(__name__ + '.' + self.__init__.__name__)

        # Type Checks:
        if not isinstance(window, curses.window):
            logger.critical("Raising TypeError:")
            __type_error__('window', 'curses.window', window)
        if not __type_check_position_or_size__(top_left):
            logger.critical("Raising TypeError:")
            __type_error__('top_left', 'tuple[int, int]', top_left)
        if not isinstance(label, str):
            logger.critical("Raising TypeError:")
            __type_error__('label', 'str', label)
        if lead_char is not None and not isinstance(lead_char, str):
            logger.critical("Raising TypeError:")
            __type_error__('lead_char', 'str', lead_char)
        if tail_char is not None and not isinstance(tail_char, str):
            logger.critical("Raising TypeError:")
            __type_error__('tail_char', 'str', tail_char)
        if lead_tail_attrs is not None and not isinstance(lead_tail_attrs, int):
            logger.critical("Raising TypeError:")
            __type_error__('lead_tail_attrs', 'Optional[int]', lead_tail_attrs)
        if callback is not None and not __type_check_callback__(callback)[0]:
            logger.critical("Raising TypeError:")
            __type_error__('left_click_callback', type_string(), callback)
        if left_click_char_codes is not None and not isinstance(left_click_char_codes, Iterable):
            logger.critical("Raising TypeError:")
            __type_error__('left_click_char_codes', 'Optional[Iterable[int]]', left_click_char_codes)
        if left_double_click_char_codes is not None and not isinstance(left_double_click_char_codes, Iterable):
            logger.critical("Raising TypeError:")
            __type_error__("left_double_click_char_codes", "Optional[Iterable[int]]", left_double_click_char_codes)
        if right_click_char_codes is not None and not isinstance(right_click_char_codes, Iterable):
            logger.critical("Raising TypeError:")
            __type_error__('right_click_char_codes', 'Optional[Iterable[int]]', right_click_char_codes)
        if right_double_click_char_codes is not None and not isinstance(right_double_click_char_codes, Iterable):
            logger.critical("Raising TypeError:")
            __type_error__("right_double_click_char_codes", "Optional[Iterable[int]]", right_double_click_char_codes)
        if not isinstance(enter_runs_callback_state, CBStates):
            logger.critical("Raising TypeError:")
            __type_error__('enter_runs_callback_state', 'CBStates', enter_runs_callback_state)
        # Parameter Checks:
        if lead_char is not None and tail_char is None:
            raise ParameterError('lead_char', "If not None, tail_char must not be None.")
        elif tail_char is not None and lead_char is None:
            raise ParameterError('tail_char', "If not None lead_char must not be None.")
        if lead_tail_attrs is None:
            if lead_char is not None or tail_char is not None:
                raise ParameterError('border_attrs', 'If using lead / tail characters, lead_tail_attrs must not be '
                                                     'None.')

        # Private properties:
        self._window: Final[curses.window] = window
        """The curses window to draw on."""
        self._label: Final[str] = label
        """The accelerated label text."""

        self._lead_char: Final[Optional[str]] = lead_char
        """The border lead character of the button."""
        self._tail_char: Final[Optional[str]] = tail_char
        """The border tail character of the button."""
        self._lead_tail_attrs: Final[Optional[int]] = lead_tail_attrs
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

        self._callback: Final[Optional[tuple[Callable, Optional[list[Any] | tuple[Any, ...]]]]] = callback
        """The on_left_click callback of the button."""

        self._left_click_chars_codes: Optional[tuple[int, ...]] = None
        """Character codes that cause the 'on_click' action to be fired in process_key."""
        if left_click_char_codes is not None:
            self._left_click_chars_codes = (*left_click_char_codes,)
        self._left_double_click_char_codes: Optional[list[int]] = None
        """Character codes that cause the 'on_double_click' action to be fired in process key."""
        if left_double_click_char_codes is not None:
            self._left_double_click_char_codes = (*left_double_click_char_codes,)

        self._right_click_chars_codes: Optional[tuple[int, ...]] = None
        """Character codes that cause the 'on_click' action to be fired in process_key."""
        if right_click_char_codes is not None:
            self._right_click_chars_codes = (*right_click_char_codes,)
        self._right_double_click_char_codes: Optional[list[int]] = None
        """Character codes that cause the 'on_double_click' action to be fired in process key."""
        if right_double_click_char_codes is not None:
            self._right_double_click_char_codes = (*right_double_click_char_codes,)

        self._enter_runs_cb_state: CBStates = enter_runs_callback_state
        """What callback state the enter key runs with."""

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

#####################################
# External methods:
#####################################
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
        if self._lead_char is not None:
            self._window.addstr(self._lead_char, self._lead_tail_attrs)
        # Add the lead indicator char:
        self._window.addstr(indicator_lead, text_attrs)
        # Add the label:
        add_accel_text(self._window, self._label, text_attrs, accel_attrs)
        # Add the tail indicator char:
        self._window.addstr(indicator_tail, text_attrs)
        # Add the border tail char:
        if self._tail_char is not None:
            self._window.addstr(self._tail_char, self._lead_tail_attrs)
        return

    def resize(self, top_left: tuple[int, int]) -> None:
        """
        Resize the button:
        :param top_left: tuple[int, int]: The new top left corner of the button.
        :return: None
        """
        # Calculate top-left and real top-left:
        self.real_top_left = top_left
        if self._lead_char is not None:
            self.top_left = (top_left[ROW], top_left[COL] + 1)
        else:
            self.top_left = top_left

        # Calculate width:
        if self._lead_char is not None:
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

    def is_mouse_over(self, rel_mouse_pos: tuple[int, int]) -> bool:
        """
        Is the mouse over this button?
        :param rel_mouse_pos: tuple[int, int]: The current relative mouse position: (ROW, COL).
        :return: bool: True the given mouse position is over this button, False it's not.
        """
        if self.top_left[ROW] <= rel_mouse_pos[ROW] <= self.bottom_right[ROW]:
            if self.top_left[COL] <= rel_mouse_pos[COL] <= self.bottom_right[COL]:
                return True
        return False

    def process_key(self, char_code: int) -> Optional[bool]:
        """
        Process a key press.
        :param char_code: int: The character code of the key pressed.
        :return: bool: True this has been handled, False it has not been handled.
        """
        # Setup logging:
        logger: logging.Logger = logging.getLogger(__name__ + '.' + self.process_key.__name__)
        # On left click:
        if self._left_click_chars_codes is not None and char_code in self._left_click_chars_codes:
            if self._callback is not None:
                logger.debug("Running callback 'on left click' ...")
                return __run_callback__(self._callback, CBStates.LEFT_CLICK.value)
            return True
        # On left double-click:
        elif self._left_double_click_char_codes is not None and char_code in self._left_double_click_char_codes:
            if self._callback is not None:
                logger.debug("Running callback 'on left double click' ...")
                return __run_callback__(self._callback, CBStates.LEFT_DOUBLE_CLICK.value)
            return True
        # On right click:
        elif self._right_click_chars_codes is not None and char_code in self._right_click_chars_codes:
            if self._callback is not None:
                logger.debug("Running callback 'on right click' ...")
                return __run_callback__(self._callback, CBStates.RIGHT_CLICK.value)
            return True
        # On right double-click:
        elif self._right_double_click_char_codes is not None and char_code in self._right_double_click_char_codes:
            if self._callback is not None:
                logger.debug("Running callback 'on right double click' ...")
                return __run_callback__(self._callback, CBStates.RIGHT_DOUBLE_CLICK.value)
            return None
        elif char_code in KEYS_ENTER:
            if self._callback is not None:
                logger.debug("Enter hit running callback '%s'..." % self._enter_runs_cb_state.value)
                return __run_callback__(self._callback, self._enter_runs_cb_state.value)
        return None

    def process_mouse(self, mouse_pos: tuple[int, int], button_state: int) -> Optional[bool]:
        """
        Process a mouse event.
        :param mouse_pos: tuple[int, int]: The mouse position: (ROW, COL).
        :param button_state: int: The button state.
        :return: bool: True the mouse event has been handled, False it has not.
        """
        # Setup logging:
        logger: logging.Logger = logging.getLogger(__name__ + '.' + self.process_mouse.__name__)
        if self.is_mouse_over(mouse_pos):
            if self._callback is not None:
                # On left click:
                if get_left_click(button_state):
                    logger.debug("Running callback 'on left click'...")
                    return __run_callback__(self._callback, CBStates.LEFT_CLICK.value)
                # On left double click:
                elif get_left_double_click(button_state):
                    logger.debug("Running callback 'on left double click'...")
                    return __run_callback__(self._callback, CBStates.LEFT_DOUBLE_CLICK.value)
                # On right click:
                elif get_right_click(button_state):
                    logger.debug("Running callback 'on right click' ...")
                    return __run_callback__(self._callback, CBStates.RIGHT_CLICK.value)
                # On right double click:
                elif get_right_double_click(button_state):
                    logger.debug("Running callback 'on right double click' ...")
                    return __run_callback__(self._callback, CBStates.RIGHT_DOUBLE_CLICK.value)
        return None  # The mouse was not handled.

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
