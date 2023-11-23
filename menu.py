#!/usr/bin/env python3
"""
File: menu.py
Handle basic menu display and control.
"""
from typing import Any, Optional
import curses
from common import ROW, COL, HEIGHT, WIDTH, KEY_ESC, KEYS_ENTER, KEY_BACKSPACE
from cursesFunctions import draw_border_on_win, calc_attributes
from menuItem import MenuItem
from typeError import __type_error__
from themes import ThemeColours


def calc_size(menu_labels) -> tuple[int, int]:
    """
    Calculate the menu size given the menu keys and values.
    :param menu_labels: The list of the menu labels.
    :return: tuple[int, int]: The size: (ROWS, COLS).
    """
    # Determine size:
    width: int = 0
    for label in menu_labels:
        width = max(width, len(label))
    height: int = len(menu_labels)
    return height + 2, width + 2  # Add 2 for a border.


class Menu(object):
    """
    Handle basic menu display and control.
    """
########################################
# Initialize:
########################################
    def __init__(self,
                 std_screen: curses.window,
                 size: tuple[int, int],
                 top_left: tuple[int, int],
                 menu_items: list[MenuItem],
                 theme: dict[str, dict[str, int | bool | str]],
                 ) -> None:
        """
        Initialize a basic menu.
        :param std_screen: curses.window: The window to draw on.
        :param size: tuple[int, int]: The size of the menu: (ROWS, COLS).
        :param top_left: tuple[int, int]: The top left corner of the menu: (ROW, COL).
        :param menu_items: list[MenuItem]: The items in this menu.
        :param theme: dict[str, dict[str, int | bool | str]]: The current theme.
        """
        # Run super:
        object.__init__(self)

        # Internal Properties:
        self._std_screen: curses.window = std_screen
        """The curses window to draw on."""
        self._menu_items: list[MenuItem] = menu_items
        """The list of MenuItems for this menu."""
        self._is_activated: bool = False
        """Is this menu activated?"""
        self._border_chars: dict[str, str] = theme['menuBorderChars']
        """The characters to use for the border."""
        self._border_attrs: int = calc_attributes(ThemeColours.MENU_BORDER, theme['menuBorder'])
        """The attributes to use for the border of this menu."""
        self._selection: Optional[int] = None
        """The current selection."""
        self._last_selection: Optional[int] = None
        """The previous selection."""
        self._min_selection: Optional[int] = None
        """The minimum selection."""
        self._max_selection: Optional[int] = None

        # External properties:
        self.real_size: tuple[int, int] = size
        """The real size of the menu."""
        self.size: tuple[int, int] = (size[HEIGHT] - 2, size[WIDTH] - 2)
        """The drawable size of the menu."""
        self.real_top_left: tuple[int, int] = top_left
        """The real top left corner of this menu."""
        self.top_left: tuple[int, int] = (top_left[ROW] + 1, top_left[COL] + 1)
        """The effective top left corner of this menu."""
        self.real_bottom_right: tuple[int, int] = (self.real_top_left[ROW] + self.real_size[HEIGHT],
                                                   self.real_top_left[COL] + self.real_size[WIDTH])
        """The real bottom right corner of this menu."""
        self.bottom_right: tuple[int, int] = (self.top_left[ROW] + self.size[ROW], self.top_left[COL] + self.size[COL])
        """The effective bottom right corner of this menu."""
        self.is_visible: bool = False
        """Is this menu visible?"""
        return

########################################
# Methods:
########################################
    def redraw(self) -> None:
        """
        Redraw the menu.
        :return: None:
        """
        if not self.is_visible:
            return
        # Draw a border:
        draw_border_on_win(window=self._std_screen, border_attrs=self._border_attrs,
                           ts=self._border_chars['ts'], bs=self._border_chars['bs'], ls=self._border_chars['ls'],
                           rs=self._border_chars['rs'], tl=self._border_chars['tl'], tr=self._border_chars['tr'],
                           bl=self._border_chars['bl'], br=self._border_chars['br'], size=self.real_size,
                           top_left=self.real_top_left)
        # Draw the menu items:
        for menu_item in self._menu_items:
            menu_item.redraw()
        self._std_screen.refresh()
        return

    def inc_selection(self) -> None:
        """
        Increment the selection wrapping if necessary.
        :return: None
        """
        next_selection = self.selection + 1
        if next_selection > self._max_selection:
            next_selection = self._min_selection
        self.selection = next_selection
        return

    def dec_selection(self) -> None:
        """
        Decrement the selection, wrapping if necessary.
        :return: None
        """
        next_selection: int = self.selection - 1
        if next_selection < self._min_selection:
            next_selection = self._max_selection
        self.selection = next_selection
        return

    def process_key(self, char_code: int) -> Optional[bool]:
        """
        Process a key press.
        :param char_code: int: The character code.
        :return: bool: True, character handled, False, it was not handled and menuBar shouldn't process it, None it was
            not handled and menuBar should handle it.
        """
        # Check that an accelerator was pressed:
        for menu_item in self._menu_items:
            if char_code in menu_item.char_codes:
                self.is_activated = False
                menu_item.activate()
                return True
        if char_code in KEYS_ENTER:
            self.is_activated = False
            self._menu_items[self.selection].activate()
            return True
        elif char_code == curses.KEY_UP:
            self.dec_selection()
            return True
        elif char_code == curses.KEY_DOWN:
            self.inc_selection()
            return True
        return None

    def is_mouse_over(self, mouse_pos: tuple[int, int]) -> bool:
        """
        Is the mouse over this menu:
        :param mouse_pos: tuple[int, int]: The current mouse position: (ROW, COL).
        :return: bool: True if the mouse is over this menu, False it is not.
        """
        if (self.top_left[ROW]) <= mouse_pos[ROW] <= (self.bottom_right[ROW]):
            if (self.top_left[COL]) <= mouse_pos[COL] <= (self.bottom_right[COL]):
                return True
        return False

    def process_mouse(self, mouse_pos: tuple[int, int], button_state: int) -> bool:
        """
        Process the mouse state.
        :param mouse_pos: tuple[int, int]: The current mouse position.
        :param button_state: int: The current button state.
        :return: bool: True, the mouse event has been handled, False it has not.
        """
        if button_state & curses.BUTTON1_CLICKED != 0 or button_state & curses.BUTTON1_DOUBLE_CLICKED != 0:
            for menu_item in self._menu_items:
                if menu_item.is_mouse_over(mouse_pos):
                    self.is_activated = False
                    menu_item.activate()
                    return True
        return False

########################################
# Properties:
########################################
    @property
    def last_selection(self) -> Optional[int]:
        """
        The previous selection.
        :return: Optional[int]: The previous selection or None if None.
        """
        return self._last_selection

    @last_selection.setter
    def last_selection(self, value: Optional[int]) -> None:
        """
        The previous selection.
        Setter.
        :param value: Optional[int]: The value to set the last selection to.
        :return: None
        """
        if value is not None and not isinstance(value, int):
            __type_error__('value', 'Optional[int]', value)
        elif value is not None and (value < self._min_selection or value > self._max_selection):
            raise ValueError("'value' out of range: %i->%i" % (self._min_selection, self._max_selection))
        self._last_selection = value
        return

    @property
    def selection(self) -> Optional[int]:
        """
        The current selection.
        :return: Optional[int]: The current selection or None if nothing selected.
        """
        return self._selection

    @selection.setter
    def selection(self, value: Optional[int]) -> None:
        """
        The current selection.
        Setter.
        :param value: Optional[int]: The current selection, None for nothing selected.
        :raises TypeError: If value is not an int or None.
        :raises ValueError: If value is out of range defined by self._max_selection and self._min_selection.
        :return: None
        """
        # Value type and value checks:
        if value is not None and not isinstance(value, int):
            __type_error__('value', 'Optional[int]', value)
        elif value is not None and (value < self._min_selection or value > self._max_selection):
            raise ValueError("'value' out of range: %i->%i." % (self._min_selection, self._max_selection))
        # Update last selection:
        self.last_selection = self._selection
        # Update selection:
        self._selection = value
        # Act on selection change:
        if self.last_selection is not None:
            self._menu_items[self.last_selection].is_selected = False
        if self._selection is not None:
            self._menu_items[self._selection].is_selected = True
        return

    @property
    def is_activated(self) -> bool:
        """
        Is this menu activated?
        :return: True if this menu is activated, False if not.
        """
        return self._is_activated

    @is_activated.setter
    def is_activated(self, value: bool) -> None:
        """
        Is this menu activated?
        :param value: bool: True, this window is activated, False if not.
        :return: None
        """
        if not isinstance(value, bool):
            __type_error__('value', 'bool', value)
        old_value = self._is_activated
        self._is_activated = value
        if old_value != value:
            self.is_visible = value
            if value:
                self.redraw()
        return

    @property
    def std_screen(self) -> curses.window:
        """
        The std screen curses.window object.
        :return: curses.window: The std screen.
        """
        return self._std_screen
