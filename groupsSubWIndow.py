#!/usr/bin/env python3
"""
File: groupsSubWindow.py
    Store and handle the groups sub window.
"""

import curses
import logging
from typing import Optional, Iterable

import common
from SignalCliApi import SignalGroup
from SignalCliApi.signalGroups import SignalGroups
from common import HEIGHT, WIDTH, TOP, LEFT, STRINGS, ContactsFocus, RIGHT, BOTTOM
from cursesFunctions import calc_attributes, add_ch, terminal_bell
from groupItem import GroupItem
from horizontalScrollBar import HorizontalScrollBar
from themes import ThemeColours
from typeError import __type_error__
from verticalScrollBar import VerticalScrollBar
from window import Window


class GroupsSubWindow(Window):
    """
    The groups sub window.
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
        :param focus_chars: Iterable[int]: The characters that cause this window to take focus.
        """

        # Store the theme for later:
        self._theme: dict[str, dict[str, int | bool | str]] = theme
        """The current theme."""
        self._focus_chars: tuple[int, ...] = (*focus_chars, )
        """The characters that cause this to take focus."""

        # Create the window parameters:
        window = curses.newwin(size[HEIGHT], size[WIDTH], top_left[TOP], top_left[LEFT])
        window_attrs: int = calc_attributes(ThemeColours.CONTACTS_WIN, theme['contWin'])
        border_attrs = calc_attributes(ThemeColours.CONTACTS_WIN_GRPS_BORDER, theme['contWinGrpsBorder'])
        border_focus_attrs = calc_attributes(ThemeColours.CONTACTS_WIN_GRPS_F_BORDER, theme['contWinGrpsFBorder'])
        border_chars = theme['groupsBorderChars']
        border_focus_chars = theme['groupsFBorderChars']
        title = STRINGS['titles']['groupsSubWin']
        title_attrs = calc_attributes(ThemeColours.CONTACTS_WIN_GRPS_TITLE, theme['contWinGrpsTitle'])
        title_focus_attrs = calc_attributes(ThemeColours.CONTACTS_WIN_GRPS_F_TITLE, theme['contWinGrpsFTitle'])
        title_chars = theme['groupsTitleChars']
        title_focus_chars = theme['groupsFTitleChars']
        self._bg_char: str = theme['backgroundChars']['contactsWin']
        # Super the window:
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
                         focus_id=ContactsFocus.GROUPS
                         )
        # Set this window's properties:
        self.always_visible = True

        # Create the vertical scroll bar:
        self._v_scrollbar: VerticalScrollBar = VerticalScrollBar(
            height=self.height - 1,
            top_left=(self.real_top_left[TOP] + 1, self.real_bottom_right[RIGHT] - 1),
            theme=theme
        )
        """The vertical scroll bar object."""
        self._v_scrollbar.is_visible = True
        # Create the horizontal scroll bar:
        self._h_scrollbar: HorizontalScrollBar = HorizontalScrollBar(
            width=self.width - 1,
            top_left=(self.real_bottom_right[BOTTOM] - 1, self.real_top_left[LEFT] + 1),
            theme=theme
        )
        """The horizontal scroll bar object."""
        self._h_scrollbar.is_visible = True

        # Set the internal properties:
        self._groups: Optional[SignalGroups] = None
        """The signal groups object for this account."""
        self._group_items: list[GroupItem] = []
        """The list of group items."""
        self._pad = None  # Set by update.
        """The curses pad for this window."""
        self._pad_width: int = 0
        """The width of the pad."""
        self._pad_height: int = 0
        """The height of the pad."""
        self._selection: Optional[int] = None
        """The current selection."""
        self._last_selection: Optional[int] = None
        """The last selection."""
        self._display_top_left: tuple[int, int] = (0, 0)
        """The top left of the pad to start the display at."""
        self._pad_effective_height: int = 0
        """The effective height of the pad."""
        self._pad_effective_width: int = 0
        """The effective width of the pad."""
        self._moving_down: bool = True
        """If the scrolling of the display is moving down."""
        self._group_list: list[SignalGroup] = []
        """The list of groups we get the group item list for."""

        # Run account changed for the first time:
        self.account_changed()
        return

#############################################
# Internal methods:
#############################################
    def __determine_pad_height__(self) -> int:
        """
        Determine the pad height based on the groups.
        :return: int: The height.
        """
        num_rows: int = 0
        for group_item in self._group_items:
            num_rows += group_item.height
        return num_rows

    def __determine_pad_width__(self) -> int:
        """
        Determine the pad width based on the groups object.
        :return: int: The width.
        """
        num_cols: int = 0
        for group_item in self._group_items:
            num_cols = max(num_cols, group_item.max_width)
        return num_cols

    def __clear_pad__(self, pad) -> None:
        num_rows, num_cols = pad.getmaxyx()
        for row in range(0, num_rows):
            for col in range(0, num_cols):
                add_ch(pad, self._bg_char, self._bg_attrs, row, col)
        return

    def __generate_empty_pad__(self, size: tuple[int, int]):  # Return Type: _CursesWindow
        """
        Create a new pad, draw the background and return it.
        :param size: tuple[int, int]: The size of the pad to create: (ROWS, COLS).
        :return: curses.window: The new pad.
        """
        if size[HEIGHT] < 1:
            raise RuntimeError("Bad height: %i" % size[HEIGHT])
        if size[WIDTH] < 1:
            raise RuntimeError("bad width: %i" % size[WIDTH])
        pad = curses.newpad(size[HEIGHT], size[WIDTH])
        self.__clear_pad__(pad)
        return pad

    def __update_groups__(self) -> None:
        def _sort_(item: SignalGroup):
            if item.last_seen is not None:
                return item.last_seen.timestamp
            return 0

        self._group_list = []

        if common.CURRENT_ACCOUNT is None:
            self._groups = None
            return
        self._groups = common.CURRENT_ACCOUNT.groups

        for group in self._groups:
            if not group.is_blocked and group.is_member:
                self._group_list.append(group)
        self._group_list.sort(key=_sort_, reverse=True)
        return

    def __update_group_items__(self) -> None:
        self._group_items = []
        if len(self._group_list) == 0:
            return

        pad_top: int = self.pad_top
        self._pad_effective_width = 0
        self._pad_effective_height = 0
        for group in self._group_list:
            group_item = GroupItem(pad_top_left=(pad_top, 0),
                                   theme=self._theme,
                                   group=group,
                                   )
            self._group_items.append(group_item)
            pad_top += group_item.height
            self._pad_effective_height += group_item.height
            self._pad_effective_width = max(self._pad_effective_width, group_item.width)
        return

    def __create_pad__(self) -> None:
        self._pad_height = self.__determine_pad_height__()
        self._pad_width = self.__determine_pad_width__()

        if self._pad_width == 0 or self._pad_height == 0:
            self._pad = self.__generate_empty_pad__((self.display_height, self.display_width))
        else:
            self._pad = self.__generate_empty_pad__((self._pad_height, self._pad_width))
        for group_item in self._group_items:
            group_item.pad = self._pad
        return

    def __inc_selection__(self, step: int = 1) -> None:
        if self.selection is None:
            self.selection = self.min_selection
            return
        should_expand: bool = self.selected_item.is_expanded
        self.selected_item.is_expanded = False
        next_selection = self.selection + step
        if next_selection > self.max_selection:
            next_selection = self.max_selection
            terminal_bell()
        self.selection = next_selection
        if should_expand:
            self.selected_item.is_expanded = True
        return

    def __dec_selection__(self, step: int = 1):
        if self.selection is None:
            self.selection = self.min_selection
            return
        should_expand: bool = self.selected_item.is_expanded
        self.selected_item.is_expanded = False
        next_selection = self.selection - step
        if next_selection < self.min_selection:
            next_selection = self.min_selection
            terminal_bell()
        self.selection = next_selection
        if should_expand:
            self.selected_item.is_expanded = True
        return

#############################################
# External methods:
#############################################
    def account_changed(self) -> None:
        self.__update_groups__()
        self.__update_group_items__()
        self.__create_pad__()
        return

    def update(self) -> None:
        self.account_changed()
        return

    def update_pad(self) -> None:
        item_top = 0
        self._pad_effective_height = 0
        self._pad_effective_width = 0
        for group_item in self._group_items:
            group_item.pad = self._pad
            group_item.top = item_top
            group_item.redraw()
            item_top += group_item.height
            self._pad_effective_height += group_item.height
            self._pad_effective_width = max(self._pad_effective_width, group_item.width)
        return

#############################################
# External method overrides:
#############################################
    def resize(self,
               size: Optional[tuple[int, int]],
               real_top_left: tuple[int, int],
               do_resize: bool = True,
               do_move: bool = True,
               ) -> None:
        """
        Resize the window.
        :param size: Optional[tuple[int, int]]: The new size.
        :param real_top_left: Optional[tuple[int, int]] The new top left corner.
        :param do_resize: bool: Do the resize of the window.
        :param do_move: bool: Do the move of the window.
        :return: None.
        """
        super().resize(size, real_top_left, do_resize, do_move)
        self._v_scrollbar.resize(self.height - 1, (self.real_top_left[TOP] + 1, self.real_bottom_right[RIGHT] - 1))
        self._h_scrollbar.resize(self.width - 1, (self.real_bottom_right[BOTTOM] - 1, self.real_top_left[LEFT] + 1))
        self.__create_pad__()
        return

    def redraw(self) -> None:
        """
        Redraw the 'groups' sub window.
        :return: None.
        """
        super().redraw()
        self.update_pad()
        # Set the scroll bar enabled according to pad size:
        if self.pad_effective_height > self.display_height:
            self._v_scrollbar.is_enabled = True
        else:
            self._v_scrollbar.is_enabled = False

        if self.pad_effective_width > self.display_width:
            self._h_scrollbar.is_enabled = True
        else:
            self._h_scrollbar.is_enabled = False

        self._v_scrollbar.redraw()
        self._h_scrollbar.redraw()

        if self.selected_item is not None:
            self.display_middle_row = self.selected_item.top

            if self.display_bottom > self.pad_effective_height:
                self.display_bottom = self.pad_effective_height - 1

        self._pad.noutrefresh(self.display_top, self.display_left,
                              self.pad_out_top, self.pad_out_left,
                              self.pad_out_bottom, self.pad_out_right)

        return

    def process_key(self, char_code: int) -> Optional[bool]:
        logger: logging.Logger = logging.getLogger(__name__ + '.' + self.process_key.__name__)
        if self.is_focused:
            if char_code == curses.KEY_UP:
                self.__dec_selection__()
                self._moving_down = False
                return True
            elif char_code == curses.KEY_DOWN:
                self.__inc_selection__()
                self._moving_down = True
                return True
            elif char_code == common.KEYS_PG_UP:
                self.__dec_selection__(5)
                self._moving_down = False
                return True
            elif char_code == common.KEYS_PG_DOWN:
                self.__inc_selection__(5)
                self._moving_down = True
                return True
            elif char_code == ord('x') or char_code == ord('X'):
                if self.selection is not None:
                    self.selected_item.is_expanded = not self.selected_item.is_expanded
                    self.__create_pad__()
                    return True
            elif char_code in common.KEYS_ENTER:
                if self.selection is not None:
                    logger.debug("Setting recipient to group: %s" % self.selected_item.group.get_display_name())
                    common.CURRENT_RECIPIENT = self.selected_item.group
                    common.CURRENT_RECIPIENT_CHANGED = True
            elif char_code == curses.KEY_LEFT:
                if self.display_left > 0:
                    self.display_left -= 1
                else:
                    terminal_bell()
            elif char_code == curses.KEY_RIGHT:
                self.display_right += 1
                if self.display_right > self.pad_effective_right:
                    self.display_right = self.pad_effective_right
                    terminal_bell()
        return None

    def process_mouse(self, mouse_pos: tuple[int, int], button_state: int) -> Optional[bool]:
        return None

########################################
# Properties:
########################################
    ################
    # Expanded:
    @property
    def is_expanded(self) -> bool:
        for group_item in self._group_items:
            if group_item.is_expanded:
                return True
        return False

    #############
    # Selection:
    @property
    def max_selection(self) -> Optional[int]:
        if len(self._group_items) > 0:
            return len(self._group_items) - 1
        return None

    @property
    def min_selection(self) -> Optional[int]:
        if len(self._group_items) > 0:
            return 0
        return None

    @property
    def selection(self) -> Optional[int]:
        return self._selection

    @selection.setter
    def selection(self, value: Optional[int]) -> None:
        if value is not None and not isinstance(value, int):
            __type_error__('value', 'Optional[int]', value)
        if value is not None and (value < self.min_selection or value > self.max_selection):
            raise ValueError("Selection out of range.")
        self._last_selection = self._selection
        self._selection = value
        if self._last_selection is not None:
            self._group_items[self._last_selection].is_selected = False
        if self._selection is not None:
            self._group_items[self._selection].is_selected = True
        return

    @property
    def last_selection(self):
        return self._last_selection

    @property
    def selected_item(self) -> Optional[GroupItem]:
        if self._selection is not None:
            return self._group_items[self._selection]
        return None

    ##################
    # Character properties:
    @property
    def focus_chars(self) -> tuple[int, ...]:
        """
        The character codes this sub window responds to.
        :return: tuple[int]: The list of codes.
        """
        return self._focus_chars

    #############
    # Pad output on the screen co-ords:
    @property
    def pad_out_top_left(self) -> tuple[int, int]:
        return self.real_top_left[TOP] + 1, self.real_top_left[LEFT] + 1

    @property
    def pad_out_bottom_right(self):
        return self.real_bottom_right[BOTTOM] - 2, self.real_bottom_right[RIGHT] - 2

    @property
    def pad_out_top(self):
        return self.real_top_left[TOP] + 1

    @property
    def pad_out_left(self):
        return self.real_top_left[LEFT] + 1

    @property
    def pad_out_bottom(self):
        return self.real_bottom_right[BOTTOM] - 2

    @property
    def pad_out_right(self):
        return self.real_bottom_right[RIGHT] - 2

    @property
    def pad_out_height(self):
        return self.pad_out_bottom - self.pad_out_top + 1

    @property
    def pad_out_width(self):
        return self.pad_out_right - self.pad_out_left + 1

    ##############
    # Pad effective size, width height, top, left, bottom and right:
    @property
    def pad_effective_size(self):
        return self._pad_effective_height, self._pad_effective_width

    @property
    def pad_effective_width(self):
        return self._pad_effective_width

    @property
    def pad_effective_height(self):
        return self._pad_effective_height

    @property
    def pad_effective_top_left(self):
        return 0, 0

    @property
    def pad_effective_top(self):
        return 0

    @property
    def pad_effective_left(self):
        return 0

    @property
    def pad_effective_bottom_right(self):
        return self._pad_effective_height - 1, self._pad_effective_width - 1

    @property
    def pad_effective_bottom(self):
        return self._pad_effective_height - 1

    @property
    def pad_effective_right(self):
        return self._pad_effective_width - 1

    ##################
    # Pad display window properties:
    @property
    def display_height(self):
        return self.pad_out_height

    @property
    def display_width(self):
        return self.pad_out_width

    @property
    def display_top(self):
        return self._display_top_left[TOP]

    @display_top.setter
    def display_top(self, value: int) -> None:
        if not isinstance(value, int):
            __type_error__('value', 'int', value)
        if value > 0:
            self._display_top_left = (value, self._display_top_left[LEFT])
        else:
            self._display_top_left = (0, self._display_top_left[LEFT])
        return

    @property
    def display_left(self):
        return self._display_top_left[LEFT]

    @display_left.setter
    def display_left(self, value: int):
        if not isinstance(value, int):
            __type_error__('value', 'int', value)
        if value > 0:
            self._display_top_left = (self._display_top_left[TOP], value)
        else:
            self._display_top_left = (self._display_top_left[TOP], 0)
        return

    @property
    def display_bottom(self):
        return self.display_top + self.display_height + 1

    @display_bottom.setter
    def display_bottom(self, value: int):
        if not isinstance(value, int):
            __type_error__('value', 'int', value)
        self.display_top = value - self.display_height + 1
        return

    @property
    def display_right(self):
        return self.display_left + self.display_width - 1

    @display_right.setter
    def display_right(self, value: int):
        if not isinstance(value, int):
            __type_error__('value', 'int', value)
        self.display_left = value - self.display_width + 1
        return

    @property
    def display_middle_row(self):
        return self.display_top + int(self.display_height / 2)

    @display_middle_row.setter
    def display_middle_row(self, value):
        self.display_top = value - int(self.display_height / 2)
        return

    @property
    def display_middle_col(self):
        return self.display_left + int(self.display_width / 2)

    @display_middle_col.setter
    def display_middle_col(self, value):
        self.display_left = value - int(self.display_width / 2)
        return

    #############
    # Properties of the pad its self:

    @property
    def pad_top_left(self):
        return 0, 0

    @property
    def pad_top(self):
        return 0

    @property
    def pad_left(self):
        return 0

    @property
    def pad_width(self):
        return self._pad_width

    @pad_width.setter
    def pad_width(self, value):
        if not isinstance(value, int):
            __type_error__('value', 'int', value)
        self._pad_width = value

    @property
    def pad_height(self):
        return self._pad_height

    @pad_height.setter
    def pad_height(self, value):
        if not isinstance(value, int):
            __type_error__('value', 'int', value)
        self._pad_height = value
        return

    @property
    def pad_bottom(self):
        return self.pad_top + self.pad_height - 1

    @property
    def pad_right(self):
        return self.pad_left + self.pad_width - 1

    @property
    def pad_bottom_right(self):
        return self.pad_bottom, self.pad_right
