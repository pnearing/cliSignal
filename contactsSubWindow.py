#!/usr/bin/env python3
"""
File: contactsSubWindow.py
    The 'contacts' sub window.
"""

import curses
from typing import Optional, Iterable

import common
from SignalCliApi import SignalContacts, SignalContact
from SignalCliApi.signalCommon import UNKNOWN_CONTACT_NAME
from common import HEIGHT, TOP, LEFT, WIDTH, STRINGS, ContactsFocus, RIGHT, BOTTOM
from contactItem import ContactItem
from cursesFunctions import calc_attributes, terminal_bell, add_str, add_ch
from horizontalScrollBar import HorizontalScrollBar
from themes import ThemeColours
from typeError import __type_error__
from verticalScrollBar import VerticalScrollBar
from window import Window


class ContactsSubWindow(Window):
    """
    The contacts sub window object.
    """
    def __init__(self,
                 std_screen: curses.window,
                 size: tuple[int, int],
                 top_left: tuple[int, int],
                 theme: dict[str, dict[str, int | bool | str]],
                 focus_chars: Iterable[int],
                 ) -> None:
        """
        Initialize the contact sub window.
        :param std_screen: curses.window: The std_screen object.
        :param size: tuple[int, int]: The size of the window.
        :param top_left: tuple[int, int]: The top left corner of the window.
        :param theme: dict[str, dict[str, int | bool | str]]: The current theme.
        :param focus_chars: Iterable[int]: The character codes that make this take focus.
        """
        # Store the theme for future use.
        self._theme = theme
        """The current theme."""
        self._focus_chars: tuple[int, ...] = (*focus_chars, )
        """The characters that make this sub window take focus."""

        window = curses.newwin(size[HEIGHT], size[WIDTH], top_left[TOP], top_left[LEFT])
        window_attrs: int = calc_attributes(ThemeColours.CONTACTS_WIN, theme['contWin'])
        border_attrs = calc_attributes(ThemeColours.CONTACTS_WIN_CONT_BORDER, theme['contWinContBorder'])
        border_focus_attrs = calc_attributes(ThemeColours.CONTACTS_WIN_CONT_F_BORDER, theme['contWinContFBorder'])
        border_chars = theme['contactsBorderChars']
        border_focus_chars = theme['contactsFBorderChars']
        title = STRINGS['titles']['contactsSubWin']
        title_attrs = calc_attributes(ThemeColours.CONTACTS_WIN_CONT_TITLE, theme['contWinContTitle'])
        title_focus_attrs = calc_attributes(ThemeColours.CONTACTS_WIN_CONT_F_TITLE, theme['contWinContFTitle'])
        title_chars = theme['contactsTitleChars']
        title_focus_chars = theme['contactsFTitleChars']
        self._bg_char: str = theme['backgroundChars']['contactsWin']

        super().__init__(std_screen=std_screen,
                         window=window,
                         title=title,
                         top_left=top_left,
                         window_attrs=window_attrs,
                         border_attrs=border_attrs,
                         border_focus_attrs=border_focus_attrs,
                         border_chars=border_chars,
                         border_focus_chars=border_focus_chars,
                         title_attrs=title_attrs,
                         title_focus_attrs=title_focus_attrs,
                         title_chars=title_chars,
                         title_focus_chars=title_focus_chars,
                         bg_char=self._bg_char,
                         focus_id=ContactsFocus.CONTACTS
                         )
        self.always_visible = True

        self._v_scrollbar: VerticalScrollBar = VerticalScrollBar(
            height=self.height - 1,
            top_left=(self.real_top_left[TOP] + 1, self.real_bottom_right[RIGHT] - 1),
            theme=theme
        )
        self._v_scrollbar.is_visible = True

        self._h_scrollbar: HorizontalScrollBar = HorizontalScrollBar(
            width=self.width - 1,
            top_left=(self.real_bottom_right[BOTTOM] - 1, self.real_top_left[LEFT] + 1),
            theme=theme
        )
        self._h_scrollbar.is_visible = True

        self._contacts: Optional[SignalContacts] = None
        """The signal Contacts object for this account."""
        self._contact_items: list[ContactItem] = []
        """The list of contact items."""
        self._pad = None  # Set by update().
        """The pad to show for this window."""
        self._pad_width: int = 0
        """The width of the pad."""
        self._pad_height: int = 0
        """The height of the pad."""
        self._selection: Optional[int] = None
        """The current selected contact item."""
        self._last_selection: Optional[int] = None
        """The last selected contact item."""
        self._display_top_left: tuple[int, int] = (0, 0)
        """The top left of the pad to start the display at."""
        self._pad_effective_height: int = 0
        """The effective height of the pad."""
        self._pad_effective_width: int = 0
        """The effective width of the pad."""
        self._moving_down: bool = True
        """If the scrolling of the display is moving down."""
        self._contact_list: list[SignalContact] = []
        """The list of contacts we use to make the contact item list for."""

        # Run account changed for the first time:
        self.account_changed()
        return

################################################
# Internal methods:
################################################
    def __determine_pad_height__(self) -> int:
        """
        Determine the pad height based on the number of contacts.
        :return: int: The pad height.
        """
        num_rows: int = 0
        for contact_item in self._contact_items:
            num_rows += contact_item.height
        return num_rows

    def __determine_pad_width__(self) -> int:
        """
        Determine the width based on the contact names:
        :return: int: The width of the pad.
        """
        num_cols: int = 0
        for contact_item in self._contact_items:
            num_cols = max(num_cols, contact_item.max_width)
        return num_cols

    def __clear_pad__(self, pad) -> None:
        """
        Draw the background on the given pad.
        :param pad: curses._CursesWindow: the pad to draw on.
        :return: None
        """
        num_rows, num_cols = pad.getmaxyx()
        for row in range(0, num_rows):
            for col in range(0, num_cols):
                add_ch(pad, self._bg_char, self._bg_attrs, row, col)
        return

    def __generate_empty_pad__(self, size: tuple[int, int]):  # Return Type: _CursesWindow.
        """
        Generate a new pad, draw the background, and return it.
        :param size: tuple[int, int]: The size of the pad: (ROWS, COLS).
        :return: _CursesWindow. The new pad.
        """
        if size[HEIGHT] < 1:
            raise RuntimeError('bad height: %i' % size[HEIGHT])
        elif size[WIDTH] < 1:
            raise RuntimeError('bad width: %i' % size[WIDTH])
        pad = curses.newpad(size[HEIGHT], size[WIDTH])
        self.__clear_pad__(pad)
        return pad

    def __update_contacts__(self) -> None:
        """
        Update the "SignalContacts" object.
        :return: None
        """
        def _sort_(item: SignalContact):
            if item.last_seen is not None:
                return item.last_seen.timestamp
            return 0

        if common.CURRENT_ACCOUNT is None:
            self._contacts = None
            return

        self._contacts = common.CURRENT_ACCOUNT.contacts

        self_contact: SignalContact = self._contacts.get_self()
        unblocked_contacts = self._contacts.get_unblocked(include_self=False)
        if common.SETTINGS['hideUnknownContacts']:
            known_contacts = []
            for contact in unblocked_contacts:
                if contact.get_display_name() != UNKNOWN_CONTACT_NAME:
                    known_contacts.append(contact)
            final_contacts = known_contacts
        else:
            final_contacts = unblocked_contacts

        final_contacts.sort(key=_sort_, reverse=True)

        self._contact_list = [self_contact, *final_contacts]
        return

    def __update_contact_items__(self) -> None:
        """
        Update the contact items list.
        :return: None
        """
        # Reset vars:
        self._contact_items = []

        # If no contacts, do nothing.
        if len(self._contact_list) == 0:
            return

        # Create the contact items:
        pad_top: int = self.pad_top
        self._pad_effective_width = 0
        self._pad_effective_height = 0
        for contact in self._contact_list:
            contact_item = ContactItem(pad_top_left=(pad_top, 0),
                                       theme=self._theme,
                                       contact=contact
                                       )
            self._contact_items.append(contact_item)
            pad_top += contact_item.height

            self._pad_effective_width = max(self._pad_effective_width, contact_item.width)
            self._pad_effective_height += contact_item.height
        return

    def __create_pad__(self) -> None:
        """
        Create a pad.
        :return: None
        """
        # Determine the size of the pad:
        self._pad_height = self.__determine_pad_height__()
        self._pad_width = self.__determine_pad_width__()
        # Create the pad:
        if self._pad_width == 0 or self._pad_height == 0:
            self._pad = self.__generate_empty_pad__((self.display_height, self.display_width))
        else:
            self._pad = self.__generate_empty_pad__((self._pad_height, self._pad_width))
        # Set the pad on the contact items:
        for contact_item in self._contact_items:
            contact_item.pad = self._pad
        return

    def __inc_selection__(self, step: int = 1) -> None:
        """
        Increment the selection.
        :param step: int: The amount to add to the selection, defaults to 1.
        :return: None
        """
        # If the selection is None, return the first selection.
        if self.selection is None:
            self.selection = self.min_selection
            return
        # Collapse the current item, and store if we should expand the next item.
        should_expand: bool = self.selected_item.is_expanded
        self.selected_item.is_expanded = False
        # Increment the selection:
        next_selection = self.selection + step
        if next_selection > self.max_selection:
            next_selection = self.max_selection
            terminal_bell()
        self.selection = next_selection
        # If we should expand the selection do so.
        if should_expand:
            self.selected_item.is_expanded = True
        return

    def __dec_selection__(self, step: int = 1) -> None:
        """
        Decrement the selection.
        :param step: int: The amount to subtract from the selection, defaults to 1.
        :return: None
        """
        # If the selection is None, return the last selection:
        if self.selection is None:
            self.selection = self.min_selection
            return
        # Collapse the current selection and store if we should expand the next selection:
        should_expand = self.selected_item.is_expanded
        self.selected_item.is_expanded = False
        # Decrement the selection:
        next_selection = self.selection - step
        if next_selection < self.min_selection:
            next_selection = self.min_selection
            terminal_bell()
        self.selection = next_selection
        # Expand the new selection if required:
        if should_expand:
            self.selected_item.is_expanded = True
        return

################################################
# External method overrides:
################################################
    def account_changed(self) -> None:
        """
        Update the sub-window based on the new account.
        :return: None
        """
        self.__update_contacts__()
        self.__update_contact_items__()
        self.__create_pad__()
        return

    def update_pad(self) -> None:
        """
        Update the pad.
        :return: None
        """
        # Clear the existing pad:
        # self.__clear_pad__(self._pad)

        # Move the group items according to the item height, and redraw the items:

        item_top = 0
        self._pad_effective_height = 0
        self._pad_effective_width = 0
        for contact_item in self._contact_items:
            contact_item.pad = self._pad
            contact_item.top = item_top
            contact_item.redraw()
            item_top += contact_item.height
            self._pad_effective_height += contact_item.height
            self._pad_effective_width = max(self._pad_effective_width, contact_item.width)
        return

    def resize(self,
               size: Optional[tuple[int, int]],
               real_top_left: Optional[tuple[int, int]],
               do_resize: bool = True,
               do_move: bool = True,
               ) -> None:
        """
        Resize the groups sub window.
        :param size: tuple[int, int]: The new size
        :param real_top_left: tuple[int, int]: The new top left corner of the window.
        :param do_resize: bool: Do the resize action.
        :param do_move: bool: Do the move action.
        :return: None.
        """
        super().resize(size, real_top_left, do_resize, do_move)
        self._v_scrollbar.resize(self.height - 1, (self.real_top_left[TOP] + 1, self.real_bottom_right[RIGHT] - 1))
        self._h_scrollbar.resize(self.width - 1, (self.real_bottom_right[BOTTOM] - 1, self.real_top_left[LEFT] + 1))
        # self._pad_out_bottom_right = (self.real_bottom_right[BOTTOM] - 2, self.real_bottom_right[RIGHT] - 2)
        self.__create_pad__()
        return

    def redraw(self) -> None:
        """
        Redraw the 'contacts' sub window.
        :return: None.
        """
        super().redraw()
        self.update_pad()

        # Set the scroll bar enabled according to pad size:
        if self._pad_effective_height > self.display_height:
            self._v_scrollbar.is_enabled = True
        else:
            self._v_scrollbar.is_enabled = False
        if self._pad_effective_width > self.display_width:
            self._h_scrollbar.is_enabled = True
        else:
            self._h_scrollbar.is_enabled = False

        self._v_scrollbar.redraw()
        self._h_scrollbar.redraw()

        if self.selected_item is not None:
            self.display_middle_row = self.selected_item.top

            if self.display_bottom > self.pad_effective_bottom:
                self.display_bottom = self.pad_effective_height - 1

        self._pad.noutrefresh(self.display_top, self.display_left,
                              self.pad_out_top, self.pad_out_left,
                              self.pad_out_bottom, self.pad_out_right)
        return

    def process_key(self, char_code: int) -> Optional[bool]:
        """
        Process a key press.
        :param char_code: int: The character code of the key pressed.
        :return: Optional[bool]: Return None: Char not handled and processing should continue. Return True: Char was
            handled, and processing should stop. Return False: Char was not handled and processing should stop.
        """
        if self.is_focused:
            if char_code == curses.KEY_UP:
                self.__dec_selection__()
                self._moving_down = False
                return True
            elif char_code == curses.KEY_DOWN:
                self.__inc_selection__()
                self._moving_down = True
                return True
            elif char_code in common.KEYS_PG_UP:
                self.__dec_selection__(5)
                self._moving_down = False
                return True
            elif char_code in common.KEYS_PG_DOWN:
                self.__inc_selection__(5)
                self._moving_down = True
                return True
            elif char_code == ord('x') or char_code == ord('X'):
                if self.selection is not None:
                    self.selected_item.is_expanded = not self.selected_item.is_expanded
                    self.__create_pad__()
                    return True
            if char_code in common.KEYS_ENTER:
                if self.selection is not None:
                    common.CURRENT_RECIPIENT = self.selected_item.contact
                    common.CURRENT_RECIPIENT_CHANGED = True
            elif char_code == curses.KEY_LEFT:
                if self.display_left > 0:
                    self.display_left -= 1
                else:
                    terminal_bell()
            elif char_code == curses.KEY_RIGHT:
                self.display_left += 1
                if self.display_right > self.pad_effective_right:
                    self.display_right = self.pad_effective_right
                    terminal_bell()
        return None

    def process_mouse(self, mouse_pos: tuple[int, int], button_state: int) -> Optional[bool]:
        """
        Process the mouse.
        :param mouse_pos: tuple[int, int]: The current mouse position
        :param button_state: int: The current button state.
        :return: Optional[bool]: TODO: Fill this out.
        """


        return None

##############################################
# Expanded properties:
##############################################
    @property
    def is_expanded(self) -> bool:
        """
        Is something expanded?
        :return: bool: True something is expanded, False it is not.
        """
        for contact_item in self._contact_items:
            if contact_item.is_expanded:
                return True
        return False

###############################################
# Selection properties:
###############################################
    @property
    def max_selection(self) -> int:
        """
        Return the max selection.
        :return: int: The max selection.
        """
        return len(self._contact_items) - 1
    
    @property
    def min_selection(self) -> int:
        """Return the min selection."""
        return 0
    
    @property
    def selection(self) -> Optional[int]:
        """
        The current selection
        :return: Optional[int]: The selection index, or None if nothing selected.
        """
        return self._selection

    @selection.setter
    def selection(self, value: Optional[int]) -> None:
        """
        The current selection. Setter.
        :param value: Optional[int]: The group item index to select.
        :return: None
        :raises TypeError: If value is not None or an int.
        :raises ValueError: If value is out of range.
        """
        if value is not None and not isinstance(value, int):
            __type_error__('value', 'Optional[int]', value)
        if value < self.min_selection or value > self.max_selection:
            raise ValueError("Selection out of range.")
        self._last_selection = self._selection
        self._selection = value
        if self._last_selection is not None:
            self._contact_items[self._last_selection].is_selected = False
        if self._selection is not None:
            self._contact_items[self._selection].is_selected = True
        return

    @property
    def last_selection(self) -> Optional[int]:
        """
        The previous selection.
        :return: Optional[int]: The previous selection.
        """
        return self._last_selection

    @property
    def selected_item(self) -> Optional[ContactItem]:
        """
        The selected contact item, or None if nothing selected.
        :return: Optional[ContactItem]: The selected item.
        """
        if self._selection is not None:
            return self._contact_items[self._selection]
        return None

###########################################
# Character properties:
###########################################
    @property
    def focus_chars(self) -> tuple[int, ...]:
        """
        The character codes this sub window responds to.
        :return: tuple[int, ...]: The list of codes.
        """
        return self._focus_chars

####################################
# Pad output on the screen co-ords:
####################################
    @property
    def pad_out_top_left(self) -> tuple[int, int]:
        """
        Pad output window top left.
        :return: tuple[int, int]: The top left: (ROW, COL).
        """
        return self.real_top_left[TOP] + 1, self.real_top_left[LEFT] + 1

    @property
    def pad_out_bottom_right(self) -> tuple[int, int]:
        """
        Pad output window bottom right.
        :return: tuple[int, int]: The bottom right: (ROW, COL).
        """
        return self.real_bottom_right[BOTTOM] - 2, self.real_bottom_right[RIGHT] - 2

    @property
    def pad_out_top(self) -> int:
        return self.real_top_left[TOP] + 1

    @property
    def pad_out_left(self) -> int:
        return self.real_top_left[LEFT] + 1

    @property
    def pad_out_bottom(self) -> int:
        return self.real_bottom_right[BOTTOM] - 2

    @property
    def pad_out_right(self) -> int:
        return self.real_bottom_right[RIGHT] - 2

    @property
    def pad_out_height(self) -> int:
        return self.pad_out_bottom - self.pad_out_top + 1

    @property
    def pad_out_width(self) -> int:
        return self.pad_out_right - self.pad_out_left + 1

########################################
# Pad effective size, width, and height and top, left, bottom, and right:
########################################
    @property
    def pad_effective_size(self) -> tuple[int, int]:
        """
        The effective size of the pad.
        :return: tuple[int, int]: The size: (ROWS, COLS).
        """
        return self._pad_effective_height, self._pad_effective_width

    @property
    def pad_effective_width(self) -> int:
        """
        The effective width of the pad.
        :return: int: The width.
        """
        return self._pad_effective_width

    @property
    def pad_effective_height(self) -> int:
        """
        The effective height of the pad.
        :return: self._pad_effective_height.
        """
        return self._pad_effective_height

    @property
    def pad_effective_top_left(self) -> tuple[int, int]:
        return 0, 0

    @property
    def pad_effective_top(self) -> int:
        return 0

    @property
    def pad_effective_left(self) -> int:
        return 0

    @property
    def pad_effective_bottom_right(self) -> tuple[int, int]:
        return self._pad_effective_height - 1, self._pad_effective_width - 1

    @property
    def pad_effective_bottom(self) -> int:
        return self._pad_effective_height - 1

    @property
    def pad_effective_right(self) -> int:
        return self._pad_effective_width - 1

########################################
# Pad display window properties:
########################################
    @property
    def display_height(self) -> int:
        return self.pad_out_height

    @property
    def display_width(self) -> int:
        return self.pad_out_width

    @property
    def display_top(self) -> int:
        """
        The top most row to start the display at.
        :return: the top most row.
        """
        return self._display_top_left[TOP]

    @display_top.setter
    def display_top(self, value: int) -> None:
        """
        The top most row to start the display at. Setter.
        :param value: int: The value to set.
        :return: None
        """
        if not isinstance(value, int):
            __type_error__('value', 'int', value)
        if value > 0:
            self._display_top_left = (value, self._display_top_left[LEFT])
        else:
            self._display_top_left = (0, self._display_top_left[LEFT])
        return

    @property
    def display_left(self) -> int:
        """
        The left most column to start the display at.
        :return: int: The left most column.
        """
        return self._display_top_left[LEFT]

    @display_left.setter
    def display_left(self, value: int) -> None:
        """
        The left most colum to start the display at. Setter.
        :param value: int: The value to set.
        :return: None
        """
        if not isinstance(value, int):
            __type_error__('value', 'int', value)
        if value > 0:
            self._display_top_left = (self._display_top_left[TOP], value)
        else:
            self._display_top_left = (self._display_top_left[TOP], 0)
        return

    @property
    def display_bottom(self) -> int:
        """
        The bottom most row to stop the display at.
        :return: int: The bottom most row.
        """
        return self.display_top + self.display_height - 1

    @display_bottom.setter
    def display_bottom(self, value: int) -> None:
        if not isinstance(value, int):
            __type_error__('value', 'int', value)
        self.display_top = value - self.display_height + 1
        return

    @property
    def display_right(self) -> int:
        """
        The right most column to stop the display at.
        :return: int: The right most column.
        """
        return self.display_left + self.display_width - 1

    @display_right.setter
    def display_right(self, value: int) -> None:
        if not isinstance(value, int):
            __type_error__('value', 'int', value)
        self.display_left = value - self.display_width + 1
        return

    @property
    def display_middle_row(self) -> int:
        return self.display_top + int(self.display_height / 2)

    @display_middle_row.setter
    def display_middle_row(self, value: int) -> None:
        self.display_top = value - int(self.display_height / 2)
        return

    @property
    def display_middle_col(self) -> int:
        return self.display_left + int(self.width / 2)

    @display_middle_col.setter
    def display_middle_col(self, value: int) -> None:
        self.display_left = value - int(self.display_width / 2)
        return

#########################################
# Properties of the pad itself:
#########################################
    @property
    def pad_top_left(self) -> tuple[int, int]:
        return 0, 0

    @property
    def pad_top(self) -> int:
        return 0

    @property
    def pad_left(self) -> int:
        return 0

    @property
    def pad_width(self) -> int:
        return self._pad_width

    @pad_width.setter
    def pad_width(self, value: int) -> None:
        if not isinstance(value, int):
            __type_error__('value', 'int', value)
        self._pad_width = value
        return

    @property
    def pad_height(self) -> int:
        return self._pad_height

    @pad_height.setter
    def pad_height(self, value: int) -> None:
        if not isinstance(value, int):
            __type_error__('value', 'int', value)
        self._pad_height = value

    @property
    def pad_bottom(self) -> int:
        return self.pad_top + self._pad_height - 1

    @property
    def pad_right(self) -> int:
        return self.pad_left + self._pad_width - 1

    @property
    def pad_bottom_right(self) -> tuple[int, int]:
        return self.pad_bottom, self.pad_right


