#!/usr/bin/env python3
"""
File: contactsWindow.py
Contacts window management.
"""
from typing import Optional
from enum import IntEnum
import curses

from SignalCliApi import SignalContact
from common import ROW, COL, STRINGS, Focus, HEIGHT, WIDTH, TOP, LEFT, ContactsFocus
from contactsSubWindow import ContactsSubWindow
from cursesFunctions import calc_attributes, draw_border_on_win, add_title_to_win
from groupsSubWIndow import GroupsSubWindow
from themes import ThemeColours
from typeError import __type_error__
from window import Window


class ContactsWindow(Window):
    """
    Class to store the contacts' window.
    """
    def __init__(self,
                 std_screen: curses.window,
                 size: tuple[int, int],
                 top_left: tuple[int, int],
                 theme: dict[str, dict[str, int | bool | str]]
                 ) -> None:
        """
        Initialize the contacts' window.
        :param std_screen: curses.window: The std_screen window object.
        :param size: tuple[int, int]: The size of the window, (rows, cols).
        :param top_left: tuple[int, int]: The co-ords of the top left corner, (ROW, COL)
        :param theme: dict[str, dict[str, int | bool]]: The theme to use.
        :returns None
        """
        # Set title and background:
        title: str = STRINGS['titles']['contacts']
        bg_char: str = theme['backgroundChars']['contactsWin']

        # Set the theme attrs:
        window_attrs: int = calc_attributes(ThemeColours.CONTACTS_WIN, theme['contWin'])
        border_attrs: int = calc_attributes(ThemeColours.CONTACT_WIN_BORDER, theme['contWinBorder'])
        border_focus_attrs: int = calc_attributes(ThemeColours.CONTACTS_WIN_FOCUS_BORDER, theme['contWinFBorder'])
        border_chars: dict[str, str] = theme['contWinBorderChars']
        border_focus_chars: dict[str, str] = theme['contWinFBorderChars']
        title_attrs: int = calc_attributes(ThemeColours.CONTACT_WIN_TITLE, theme['contWinTitle'])
        title_focus_attrs: int = calc_attributes(ThemeColours.CONTACTS_WIN_FOCUS_TITLE, theme['contWinFTitle'])
        title_chars: dict[str, str] = theme['contWinTitleChars']
        title_focus_chars: dict[str, str] = theme['contWinFTitleChars']

        # Make a curses window:
        window = curses.newwin(size[ROW], size[COL], top_left[ROW], top_left[COL])

        # Super the window.
        Window.__init__(self, std_screen, window, title, top_left, window_attrs, border_attrs, border_focus_attrs,
                        border_chars, border_focus_chars, title_attrs, title_focus_attrs, title_chars,
                        title_focus_chars, bg_char, Focus.CONTACTS)

        # Set this window as always visible:
        self.always_visible = True
        self.is_static_size = False

        # Calculate the contacts window size and position:
        contacts_win_size: tuple[int, int] = (int(self.height / 2), self.width)
        contacts_win_top_left: tuple[int, int] = (self.real_top_left[ROW] + 1, self.real_top_left[COL] + 1)

        # Calculate the groups window size and position:
        groups_win_size: tuple[int, int] = (self.height - contacts_win_size[HEIGHT], self.width)
        groups_win_top_left: tuple[int, int] = (self.real_top_left[ROW] + contacts_win_size[HEIGHT] + 1,
                                                self.real_top_left[COL] + 1)

        # Create the 'Contacts' sub window:
        self._contacts_win = ContactsSubWindow(std_screen, contacts_win_size, contacts_win_top_left, theme, (ord('C'),))
        """The contacts sub window."""
        self._contacts_win.selection = self._contacts_win.min_selection
        # Create the 'Groups' sub window:
        self._groups_win = GroupsSubWindow(std_screen, groups_win_size, groups_win_top_left, theme, (ord('G'),))
        """The groups sub window."""
        # Store the windows as a tuple indexed by ContactsFocus:
        self.focus_windows: tuple[ContactsSubWindow, GroupsSubWindow] = (self._contacts_win, self._groups_win)
        """The list of windows that can get focus."""
        self._current_focus: Optional[ContactsFocus] = None
        """The currently focused sub window."""
        self._last_focus: Optional[ContactsFocus] = None
        """The last focused sub window."""
        # Set initial focus:
        self.current_focus = ContactsFocus.CONTACTS
        return

#################################################
# External methods:
#################################################
    def hover_focus(self, mouse_pos: tuple[int, int]) -> None:
        """
        Do hover focus.
        :param mouse_pos: tuple[int, int]: The current mouse position: (ROW, COL).
        :return: None
        """
        if self._contacts_win.is_mouse_over(mouse_pos):
            self.current_focus = ContactsFocus.CONTACTS
        elif self._groups_win.is_mouse_over(mouse_pos):
            self.current_focus = ContactsFocus.GROUPS
        return

    def account_changed(self) -> None:
        """
        The account has changed.
        :return: None
        """
        self._contacts_win.account_changed()
        return

#################################################
# External Overrides:
#################################################
    def redraw(self) -> None:
        super().redraw()
        self._contacts_win.redraw()
        self._groups_win.redraw()
        return

    def resize(self,
               size: Optional[tuple[int, int]],
               real_top_left: Optional[tuple[int, int]],
               do_resize: bool = True,
               do_move: bool = True,
               ) -> None:
        """
        Resize the 'Contacts' window.
        :param size: The new size.
        :param real_top_left: The new real top left.
        :param do_resize: bool: Do the resize operation. Defaults to True.
        :param do_move: bool: Do the move window operation. Defaults to True.
        :return: None.
        """
        super().resize(size, real_top_left, do_resize, do_move)
        contacts_win_size: tuple[int, int] = (int(self.height / 2), self.width)
        contacts_win_top_left: tuple[int, int] = (self.real_top_left[ROW] + 1, self.real_top_left[COL] + 1)
        groups_win_size: tuple[int, int] = (self.height - contacts_win_size[HEIGHT], self.width)
        groups_win_top_left: tuple[int, int] = (self.real_top_left[ROW] + contacts_win_size[HEIGHT] + 1,
                                                self.real_top_left[COL] + 1)

        self._contacts_win.resize(contacts_win_size, contacts_win_top_left)
        self._groups_win.resize(groups_win_size, groups_win_top_left)
        return

    def process_key(self, char_code: int) -> Optional[bool]:
        """
        Process a key press.
        :param char_code: int: The character code of the pressed key.
        :return: Optional[bool]: Return None char not handled, processing should continue. Return True Char handled and
            we should grab focus. Return False Char was handled, and processing should stop.
        """
        # Check to see if we should take focus by matching against the focus chars:
        if char_code in self._contacts_win.focus_chars:
            self.current_focus = ContactsFocus.CONTACTS
            return True
        elif char_code in self._groups_win.focus_chars:
            self.current_focus = ContactsFocus.GROUPS
            return True

        # Only if we're focused do we want to process the key:
        if self.is_focused:
            char_handled: Optional[bool] = None
            char_handled = self.focus_windows[self.current_focus].process_key(char_code)
            if char_handled is not None:
                return char_handled
        return None

#########################################
# Properties:
#########################################
    @property
    def current_focus(self) -> Optional[ContactsFocus]:
        """
        The currently focused index.
        :return: Optional[ContactsFocus]: The current focus index object, or None if nothing focused.
        """
        return self._current_focus

    @current_focus.setter
    def current_focus(self, value: Optional[ContactsFocus | int]) -> None:
        """
        The currently focused index.
        Setter.
        :param value: Optional[ContactsFocus | int]: The value to set to.
        :return: None.
        """
        # Type check value:
        if value is not None and not isinstance(value, (ContactsFocus, int)):
            __type_error__('value', 'Optional[ContactsFocus | int]', value)
        # Set last focus:
        self._last_focus = self._current_focus
        # set focus:
        if value is not None:
            self._current_focus = ContactsFocus(value)
        else:
            self._current_focus = None
        # Set the focus of the sub windows based on the focus value:
        if self._last_focus != self._current_focus:
            if value is None:
                self._contacts_win.is_focused = False
                self._groups_win.is_focused = False
            elif value == ContactsFocus.CONTACTS:
                self._contacts_win.is_focused = True
                self._groups_win.is_focused = False
            elif value == ContactsFocus.GROUPS:
                self._contacts_win.is_focused = False
                self._groups_win.is_focused = True
        return

    @property
    def last_focus(self) -> Optional[ContactsFocus]:
        """
        The last focus.
        :return: Optional[ContactsFocus]: The last focused window.
        """
        return self._last_focus

#########################################
# Property hooks:
#########################################
    def __is_focused_hook__(self, is_get: bool, value: bool) -> Optional[bool]:
        """
        Is focused Window hook.
        :param is_get: bool: True, this is the Getter, False this is the Setter.
        :param value: Optional[bool]: If 'is_get' is true this is the current value, if 'is_get' is False, this is the
            new value.
        :return: Optional[bool]: If 'is_get' is False, the return value is ignored, otherwise if the return value is
            None, the setter returns the current value, and if the return value is not None this is the value the getter
            will return.
        """
        if not is_get:
            if value:
                if self.last_focus is not None:
                    self.current_focus = self.last_focus
                else:
                    self.current_focus = ContactsFocus.CONTACTS
            else:
                self.current_focus = None
        return None
