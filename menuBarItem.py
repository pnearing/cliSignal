#!/usr/bin/env python3
import logging
from typing import Optional, Callable, Any, Iterable
from warnings import warn
import curses
from common import ROW, COL, WIDTH, HEIGHT, KEYS_ENTER
from cursesFunctions import calc_attributes, add_accel_text, get_rel_mouse_pos
from typeError import __type_error__
from menu import Menu
from themes import ThemeColours
# from fileMenu import FileMenu
# from accountsMenu import AccountsMenu
# from helpMenu import HelpMenu


class MenuBarItem(object):
    """
    Class to hold a single menu item.
    """

#################################
# Initialize:
#################################
    def __init__(self,
                 std_screen: curses.window,
                 window,  # Type: curses._CursesWindow
                 top_left: tuple[int, int],
                 label: str,
                 theme: dict[str, dict[str, int | bool | str]],
                 menu: Optional[Menu],
                 activate_char_codes: Iterable[int],
                 deactivate_char_codes: Iterable[int],
                 ) -> None:
        """
        Initialize a menu item.
        :param std_screen: curses.window: The std_screen window object.
        :param window: curses.window: The window to draw on.
        :param top_left: tuple[int, int]: The top left corner of this menu item.
        :param label: str: The text of the menu item.
        :param theme: dict[str, dict[str, int | bool | str]]: The current theme.
        :param menu: Menu: The menu this item holds.
        :param activate_char_codes: Iterable[int]: The character codes that activate the menu.
        :param deactivate_char_codes: Iterable[int]: The character codes that deactivate the menu.
        """
        # Super:
        object.__init__(self)
        # Private properties
        self._std_screen: curses.window = std_screen
        """The std_screen window object."""
        self._window: curses.window = window  # Real type: curses._CursesWindow
        """The curses window object to draw on."""
        self._sel_attrs: int = calc_attributes(ThemeColours.MENU_BAR_SEL, theme['menuBarSel'])
        """The attributes to use when this item is selected."""
        self._sel_accel_attrs: int = calc_attributes(ThemeColours.MENU_BAR_SEL_ACCEL, theme['menuBarSelAccel'])
        """The attributes to use for the accelerator."""
        self._unsel_attrs: int = calc_attributes(ThemeColours.MENU_BAR_UNSEL, theme['menuBarUnsel'])
        """The attributes to use when this item is unselected."""
        self._unsel_accel_attrs: int = calc_attributes(ThemeColours.MENU_BAR_UNSEL_ACCEL, theme['menuBarUnselAccel'])
        """The attributes to use for the accelerator when item is unselected."""
        self._sel_lead_indicator: str = theme['menuBarSelChars']['leadSel']
        """The string to append to the beginning of the label when selected."""
        self._sel_tail_indicator: str = theme['menuBarSelChars']['tailSel']
        """The string to append to the end of the label when selected."""
        self._unsel_lead_indicator: str = theme['menuBarSelChars']['leadUnsel']
        """The string to append to the beginning of the label when unselected."""
        self._unsel_tail_indicator: str = theme['menuBarSelChars']['tailUnsel']
        """The string to append to the end of the label when unselected."""
        self._is_selected: bool = False
        """If this item is selected."""
        self._menu: Menu = menu
        """The menu object this menu bar item holds."""

        # Public properties:
        self.top_left: tuple[int, int] = top_left
        """This items top left corner."""
        width: int = len(label)  # This is 2 chars longer than the actual width of the title due to accel chars.
        self.size: tuple[int, int] = (1, width)
        """The size of this item in ROW, COL format."""
        self.bottom_right: tuple[int, int] = (top_left[ROW], top_left[COL] + width - 1)
        """The bottom right of this menu item."""
        self.label: str = label
        """The label to display."""
        self.activate_char_codes: tuple[int] = (*activate_char_codes,)
        """Character codes that activate this menu."""
        self.deactivate_char_codes: tuple[int] = (*deactivate_char_codes,)
        """Character codes that deactivate this menu."""
        return

#################################
# Methods:
#################################
    def redraw(self) -> None:
        """
        Redraw this menu item.
        :return: None
        """
        logger: logging.Logger = logging.getLogger(__name__ + '.' + self.redraw.__name__)
        # Determine attrs, and lead / tail characters:
        text_attrs: int
        accel_attrs: int
        lead_indicator: str
        tail_indicator: str
        if self.is_selected:
            text_attrs = self._sel_attrs
            accel_attrs = self._sel_accel_attrs
            lead_indicator = self._sel_lead_indicator
            tail_indicator = self._sel_tail_indicator
        else:
            text_attrs = self._unsel_attrs
            accel_attrs = self._unsel_accel_attrs
            lead_indicator = self._unsel_lead_indicator
            tail_indicator = self._unsel_tail_indicator

        # logger.debug("menuBarItem: %s: top_left: %s" % (self.label, self.top_left))
        # Move the cursor to the top left corner:
        self._window.move(self.top_left[ROW], self.top_left[COL])
        # Write the leading indicator character:
        self._window.addstr(lead_indicator, text_attrs)
        # Write the label, parsing the _ as accel indicator start / stop char.
        add_accel_text(self._window, self.label, text_attrs, accel_attrs)
        # Add the trailing selection indicator:
        self._window.addstr(tail_indicator, text_attrs)
        # Redraw the menu:
        self._menu.redraw()
        # Refresh the window:
        self._window.noutrefresh()
        return

    def is_mouse_over(self, rel_mouse_pos: tuple[int, int]) -> bool:
        """
        Return True if the mouse is over this menu item.
        :param rel_mouse_pos: tuple[int, int]: The relative mouse position: (ROW, COL).
        :return: bool: True if the mouse is over this menu bar item, False it is not.
        """
        if rel_mouse_pos[ROW] == self.top_left[ROW]:
            if self.top_left[COL] <= rel_mouse_pos[COL] <= self.bottom_right[COL]:
                return True
        return False

    def process_key(self, char_code: int) -> Optional[bool]:
        """
        Process a key press.
        :param char_code: int: The character code of the pressed key.
        :return: Optional[bool]: If None, the character wasn't handled, processing should continue.
        If False, the character wasn't handled and processing shouldn't continue.
        If True, the character was handled and processing shouldn't continue.
        """
        # If the menu is active, send the key press there:
        if self._menu.is_activated:
            handled: Optional[bool] = self._menu.process_key(char_code)
            if handled is not None:
                return handled
        # Handle activate char codes:
        if char_code in self.activate_char_codes:
            self.is_activated = True
            return True
        # Handle deactivate char codes:
        if char_code in self.deactivate_char_codes:
            self.is_activated = False
            return True
        return None

#################################
# Properties:
#################################
    @property
    def is_selected(self) -> bool:
        """
        Is this item selected?
        :return: bool: True item selected, False item is unselected.
        """
        return self._is_selected

    @is_selected.setter
    def is_selected(self, value: bool) -> None:
        """
        Is this item selected?
        Setter.
        :param value: bool: The value to set is_selected to.
        :raises TypeError: When value is not a bool.
        :return: None
        """
        if not isinstance(value, bool):
            __type_error__('value', 'bool', value)
        old_value = self._is_selected
        self._is_selected = value
        if value != old_value and value:
            self.redraw()
        return

    @property
    def is_activated(self) -> bool:
        """
        Is this menu bar item activated?
        :return: bool: True, this menu bar is activated, False, it is not.
        """
        return self._menu.is_activated

    @is_activated.setter
    def is_activated(self, value: bool) -> None:
        """
        Is this menu bar item activated?
        Setter.
        :param value: bool: True, this menu bar item is activated, False, it is not.
        :return: None
        :raises TypeError: If value is not a bool.
        """
        if not isinstance(value, bool):
            __type_error__('value', 'bool', value)
        self._menu.is_activated = value
        return

    @property
    def std_screen(self) -> curses.window:
        """
        Return the std_screen window object..
        :return: curses.window: The std_screen window object.
        """
        return self._std_screen

    @property
    def width(self) -> int:
        """
        The width of the menu bar item.
        :return: int: The width.
        """
        return self.size[WIDTH]

    @property
    def height(self) -> int:
        """
        The height of the menu bar item.
        :return: int: The height.
        """
        return self.size[HEIGHT]

    @property
    def menu(self) -> Menu:
        """
        Return the menu associated with this menu bar item.
        :return: Menu: The menu object.
        """
        return self._menu
