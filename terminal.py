#!/usr/bin/env python3
from typing import Pattern, Final, Match, Optional
import re
import os

# Regex to validate basic colour / control strings.
_is_four_bit_regex: Pattern = re.compile(r'^\033\[(?P<value>\d+)m$')
"""Regex to match a four bit colour string."""
_is_eight_bit_regex: Pattern = re.compile(r'^\033\[(?P<fgBg>[34]8);5;(?P<value>\d{1,3})m$')
"""Regex to match a eight bit colour string."""
_is_sixteen_bit_regex: Pattern = re.compile(r'^\033\[(?P<fgBg>[34]8);2;(?P<red>\d{1,3});(?P<green>\d{1,3});'
                                            r'(?P<blue>\d{1,3})m$')
"""Regex to match a sixteen bit colour string."""

_control_values: Final[list[str]] = ['0', '01', '02', '03', '04', '05', '06', '07', '08', '09']
"""List of valid four bit control values, for things like blink and reset."""
_four_bit_fg_values: Final[list[str]] = [
    '30', '31', '32', '33', '34', '35', '36', '37', '90', '91', '92', '93', '94', '95', '96', '97'
]
"""List of valid four bit foreground colour values."""
_four_bit_bg_values: Final[list[str]] = [
    '40', '41', '42', '43', '44', '45', '46', '47', '100', '101', '102', '103', '104', '105', '106', '107'
]
"""List of valid four bit background colour values."""

# Valid 8-bit foreground / background values:
_eight_bit_fg_value: Final[str] = '38'
"""Eight bit foreground colour value."""
_eight_bit_bg_value: Final[str] = '48'
"""Eight bit background colour value."""
# Valid 16-bit foreground / background values:
_sixteen_bit_fg_value: Final[str] = '38'
"""Sixteen bit foreground colour value."""
_sixten_bit_bg_value: Final[str] = '48'
"""Sixteen bit background colour value."""


def __value_is_valid__(value: str) -> bool:
    str_value: str = value
    int_value: int = int(value)
    if 0 <= int_value <= 9:
        if len(str_value) == 1:
            return True
    elif 10 <= int_value <= 99:
        if len(str_value) == 2:
            return True
    elif 100 <= int_value <= 255:
        if len(str_value) == 3:
            return True
    return False


class Terminal(object):
    """Class to control terminal."""
    def __init__(self) -> None:
        object.__init__(self)
        return

    @staticmethod
    def size(file_descriptor: Optional[int] = None) -> tuple[int, int]:
        """
        Get the size of the terminal, returns a tuple of columns, and rows.
        :param file_descriptor: Optional[int]: The file descriptor number, defaults to None for STDOUT.
        :returns: Tuple[int, int]: Element 0, columns; Element 1, rows;
        """
        if file_descriptor is not None:
            cols, rows = os.get_terminal_size(file_descriptor)
            return cols, rows
        else:
            cols, rows = os.get_terminal_size()
            return cols, rows

    @staticmethod
    def columns(file_descriptor: Optional[int] = None) -> int:
        """
        Return the number of columns in the terminal.
        :param file_descriptor: Optional[int]: The file descriptor, defaults to None from STDOUT.
        :returns: Int: The number of columns.
        """
        if file_descriptor is not None:
            return os.get_terminal_size(file_descriptor)[0]
        else:
            return os.get_terminal_size()[0]

    @staticmethod
    def rows(file_descriptor: Optional[int] = None) -> int:
        """
        Return the number of rows in the terminal.
        :param file_descriptor: Optional[int]: The file descriptor, defaults to None for STDOUT.
        :returns: Int: The number of rows.
        """
        if file_descriptor is not None:
            return os.get_terminal_size(file_descriptor)[1]
        else:
            return os.get_terminal_size()[1]

    @staticmethod
    def beep() -> None:
        """
        Ring the bell.
        :returns: None
        """
        print('\a', end='', flush=True)
        return


class Cursor(object):
    """Class to control the cursor."""

    def __init__(self) -> None:
        object.__init__(self)
        return

    @staticmethod
    def set_cursor(row: int, col: int, do_print: bool = True, end: str = '', **print_kwargs: dict) -> str:
        """
        Return a control string setting the cursor position to row, col.
        :param row: Int: The row to set the cursor at.
        :param col: Int: The column to set the cursor at.
        :param do_print: Bool: Actually print the control string, defaults to True.
        :param end: Str: The value to pass to print as the end keyword, defaults to an empty string.
        :param print_kwargs: Dict: Other keyword arguments to pass to print.
        :returns: Str: The control string.
        """
        control_string: str = "\033[%i;%iH" % (row, col)
        if do_print:
            print(control_string, end=end, **print_kwargs)
        return control_string

    @staticmethod
    def move_cursor_up(num_rows: int, do_print: bool = True, end: str = '', **print_kwargs: dict) -> str:
        """
        Return a control string that moves the cursor up num_rows rows / lines.
        :param num_rows: Int: The number of rows to move the cursor.
        :param do_print: Bool: Actually print the control string, defaults to True.
        :param end: Str: The value to pass to print as the end keyword, defaults to an empty string.
        :param print_kwargs: Dict: Any other keyword arguments to pass to print.
        :returns: Str: The control string.
        """
        control_string: str = "\033[%iA" % num_rows
        if do_print:
            print(control_string, end=end, **print_kwargs)
        return control_string

    @staticmethod
    def move_cursor_down(num_rows: int, do_print: bool = True, end: str = '', **print_kwargs: dict) -> str:
        """
        Return a control string that moves the cursor down num_rows rows / lines.
        :param num_rows: Int: The number of rows to move the cursor.
        :param do_print: Bool: Actually print the control string, defaults to True.
        :param end: Str: The value to pass to print as the end key word, defaults to an empty string.
        :param print_kwargs: Dict: Any other key word arguments to pass to print.
        :returns: Str: The control string.
        """
        control_string: str = "\033[%iB" % num_rows
        if do_print:
            print(control_string, end=end, **print_kwargs)
        return control_string

    @staticmethod
    def move_cursor_forward(num_cols: int, do_print: bool = True, end: str = '', **print_kwargs: dict) -> str:
        """
        Return a control string that moves the cursor forward num_cols columns / spaces.
        :param num_cols: Int: The number of columns to move forward.
        :param do_print: Bool: Actually print the control string, defaults to True.
        :param end: Str: The value to pass to print as the end keyword, defaults to an empty string.
        :param print_kwargs: Dict: Any other key word arguments to pass to print.
        :returns: Str: The control string.
        """
        control_string: str = '\033[%iC' % num_cols
        if do_print:
            print(control_string, end=end, **print_kwargs)
        return control_string

    @staticmethod
    def move_cursor_backward(num_cols: int, do_print: bool = True, end: str = '', **print_kwargs: dict) -> str:
        """
        Return a control string that moves the cursor backward num_cols columns / spaces.
        :param num_cols: Int: The number of columns to move.
        :param do_print: Bool: Actually print the control string, defaults to True.
        :param end: Str: The value to pass as the end keyword value, defaults to an empty string.
        :param print_kwargs: Dict: Any other key word arguments to pass to print.
        :returns: Str: The control string.
        """
        control_string: str = '\033[%iD' % num_cols
        if do_print:
            print(control_string, end=end, **print_kwargs)
        return control_string

    @staticmethod
    def previous_row(num_rows: int, do_print: bool = True, end: str = '', **print_kwargs: dict) -> str:
        """
        Return a control string that moves the cursor up num_rows, rows, and to the beginning of the line.
            (Sets col to 0)
        :param num_rows: Int: The number of rows to move.
        :param do_print: Bool: Actually print the control string, defaults to True.
        :param end: Str: The value to pass to print as the end keyword argument, defaults to an empty string.
        :param print_kwargs: Dict: Any other key word arguments to pass to print.
        :returns: Str: The control string.
        """
        control_string = '\033[%iF' % num_rows
        if do_print:
            print(control_string, end=end, **print_kwargs)
        return control_string

    @staticmethod
    def next_row(num_rows: int, do_print: bool = True, end: str = '', **print_kwargs: dict) -> str:
        """
        Returns a control string that moves the cursor down num_rows rows / lines, and to the beginning of the line.
            (Sets col to 0)
        :param num_rows: Int: The number of rows to move down.
        :param do_print: Bool: Actually print the control string, defaults to True.
        :param end: Str: The value to pass to print as the end key word argument, defaults to an empty string.
        :param print_kwargs: Dict: Any other key word arguments to pass to print.
        :returns: Str: The control string.
        """
        control_string: str = '\033[%iE' % num_rows
        if do_print:
            print(control_string, end=end, **print_kwargs)
        return control_string

    @staticmethod
    def clear_screen_to_end(do_print: bool = True, end: str = '', **print_kwargs: dict) -> str:
        """
        Clear the screen from the cursor to the end of the display.
        :param do_print: Bool: Actually print the control string, defaults to True.
        :param end: Str: The value to pass to print as the end key word argument, defaults to an empty string.
        :param print_kwargs: Dict: Any other key word arguments to pass to print.
        :returns: Str: The control string.
        """
        control_string: str = '\033[0J'
        if do_print:
            print(control_string, end=end, **print_kwargs)
        return control_string

    @staticmethod
    def clear_screen_to_beginning(do_print: bool = True, end: str = '', **print_kwargs: dict) -> str:
        """
        Clear the screen from the cursor to the beginning of the display.
        :param do_print: Bool: Actually print the control string, defaults to True.
        :param end: Str: The value to pass to print as the end key word argument, defaults to an empty string.
        :param print_kwargs: Dict: Any other key word arguments to pass to print.
        :returns: Str: The control character.
        """
        control_string: str = '\033[1J'
        if do_print:
            print(control_string, end=end, **print_kwargs)
        return control_string

    @staticmethod
    def clear_screen(do_print: bool = True, end: str = '', **print_kwargs: dict) -> str:
        """
        Clear the screen and relocate the cursor to 0,0.
        :param do_print: Bool: Actually print the control string, defaults to True.
        :param end: Str: The value to pass as the end key word argument, defaults to an empty string.
        :param print_kwargs: Any other key word arguments to pass to print.
        :returns: Str: The control string.
        """
        control_string: str = '\033[2J'
        if do_print:
            print(control_string, end=end, **print_kwargs)
        return control_string

    @staticmethod
    def clear_screen_and_buffer(do_print: bool = True, end: str = '', **print_kwargs: dict) -> str:
        """
        Clears the entire screen and clears the scroll back buffer.
        :param do_print: Bool: Actually print the control string, defaults to True.
        :param end: Str: The value to pass to string as the end key word argument, defaults to an empty string.
        :param print_kwargs: Dict: Any other key word arguments to pass to print.
        :returns: Str: The control string.
        """
        control_string: str = '\033[3J'
        if do_print:
            print(control_string, end=end, **print_kwargs)
        return control_string

    @staticmethod
    def clear_line_to_end(do_print: bool = True, end: str = '', **print_kwargs: dict) -> str:
        """
        Clear from the current cursor position to the end of the line.
        :param do_print: Bool: Actually print the control string, defaults to True.
        :param end: Str: The value to pass to print as the end key word argument, defaults to an empty string.
        :param print_kwargs: Dict: Any other key word arguments to pass to print.
        :returns: Str: The control string.
        """
        control_string: str = '\033[0K'
        if do_print:
            print(control_string, end=end, **print_kwargs)
        return control_string

    @staticmethod
    def clear_line_to_beginning(do_print: bool = True, end: str = '', **print_kwargs: dict) -> str:
        """
        Clear from the current cursor position to the beginning of the line.
        :param do_print: Bool: Actually print the control string, defaults to True
        :param end: Str: The value to pass to print as the end keyword, defaults to an empty string.
        :param print_kwargs: Dict: Any other key word arguments to pass to print.
        :returns: Str: The control string.
        """
        control_string: str = '\033[1K'
        if do_print:
            print(control_string, end=end, **print_kwargs)
        return control_string

    @staticmethod
    def clear_line(do_print: bool = True, end: str = '', **print_kwargs: dict) -> str:
        """
        Clear the entire current line.
        :param do_print: Bool: Actually print the control string, defaults to True.
        :param end: Str: The value to pass to print as the end key word argument, defaults to an empty string.
        :param print_kwargs: Dict: Any other key word arguments to pass to print.
        :returns: Str: The control string.
        """
        control_string: str = '\033[2K'
        if do_print:
            print(control_string, end=end, **print_kwargs)
        return control_string

    @staticmethod
    def scroll_up(num_rows: int, do_print: bool = True, end: str = '', **print_kwargs: dict) -> str:
        """
        Scroll the whole screen up by num_rows rows / lines, new lines are added to the bottom of the screen.
        :param num_rows: Int: The number of rows to scroll.
        :param do_print: Bool: Actually print the control string, defaults to True.
        :param end: Str: The value to pass to print as the end key word argument, defaults to an empty string.
        :param print_kwargs: Dict: Any other key word arguments to pass to print.
        :returns: Str: The control string.
        """
        control_string: str = '\033[%iS' % num_rows
        if do_print:
            print(control_string, end=end, **print_kwargs)
        return control_string

    @staticmethod
    def scroll_down(num_rows: int, do_print: bool = True, end: str = '', **print_kwargs: dict) -> str:
        """
        Scroll whole screen down by num_rows rows / lines, new lines are added to the top of the screen.
        :param num_rows: Int: The number of rows to scroll.
        :param do_print: Bool: Actually print the control string, defaults to True.
        :param end: Str: The value to pass to print as the end key word argument, defaults to an empty string.
        :param print_kwargs: Dict: Any other keyword args to pass to print.
        :returns: Str: The control string.
        """
        control_string: str = '\033[%iT' % num_rows
        if do_print:
            print(control_string, end=end, **print_kwargs)
        return control_string

    @staticmethod
    def show_cursor(do_print: bool = True, end: str = '', **print_kwargs: dict) -> str:
        """
        Turn the cursor on.
        :param do_print: Bool: Actually print the control string, defaults to True.
        :param end: Str: The value to pass to print as the end key word argument, defaults to an empty string.
        :param print_kwargs: Dict: Any other key word arguments to pass to print.
        :returns: Str: The control string.
        """
        control_string: str = '\033[25h'
        if do_print:
            print(control_string, end=end, **print_kwargs)
        return control_string

    @staticmethod
    def hide_cursor(do_print: bool = True, end: str = '', **print_kwargs: dict) -> str:
        """
        Turn the cursor off.
        :param do_print: Bool: Actually print the control string, defaults to True.
        :param end: Str: The value to pass to the end key word argument, defaults to an empty string.
        :param print_kwargs: Dict: Any other key word arguments to pass to print.
        :returns: Str: The control string.
        """
        control_string: str = '\033[25l'
        if do_print:
            print(control_string, end=end, **print_kwargs)
        return control_string

    @staticmethod
    def save_position(do_print: bool = True, end: str = '', **print_kwargs: dict) -> str:
        """
        Saves the current cursor position. NOTE: Not supported by all terminals.
        :param do_print: Bool: Actually print the control string, defaults to True.
        :param end: Str: The value to pass to print as the end keyword value, defaults to an empty string.
        :param print_kwargs: Dict: Any other key word arguments to pass to print.
        :returns: Str: The control string.
        """
        control_string: str = '\033[s'
        if do_print:
            print(control_string, end=end, **print_kwargs)
        return control_string

    @staticmethod
    def load_position(do_print: bool = True, end: str = '', **print_kwargs: dict) -> str:
        """
        Restore the position of the cursor that was previously saved. NOTE: Not supported by all terminals.
        :param do_print: Bool: Actually print the control string, defaults to True.
        :param end: Str: The value to pass as print's end key word, defaults to an empty string.
        :param print_kwargs: Dict: Any other key word args to pass to print.
        :returns: Str: The control string.
        """
        control_string: str = '\033[u'
        if do_print:
            print(control_string, end=end, **print_kwargs)
        return control_string


class ColourError(Exception):
    """Class for all colour errors."""
    _errorMessages = {
        0: 'No Error.',
        1: 'TypeError: value must be an int between 0 and 255, inclusive.',
        2: 'TypeError: red must be an int between 0 and 255, inclusive.',
        3: 'TypeError: green must be an int between 0 and 255, inclusive.',
        4: 'TypeError: blue must be an int between 0 and 255, inclusive.',
        5: 'TypeError: value must be a str.',
        6: 'ValueError: value must be an int between 0 and 255, inclusive.',
        7: 'ValueError: red value must be an int between 0 and 255, inclusive.',
        8: 'ValueError: green value must be an int between 0 and 255, inclusive.',
        9: 'ValueError: blue value must be an int between 0 and 255, inclusive.',
        10: 'Value is not valid control string.',
        11: 'Value is not valid colour string.',
        12: 'Value is not valid four bit colour string.',
        13: 'Value is not valid eight bit colour string.',
        14: 'Value is not valid sixteen bit colour string.',
        15: 'Value is not valid foreground colour string.',
        16: 'Value is not valid background colour string.',
    }

    def __init__(self,
                 error_number: int,
                 *args: object
                 ) -> None:
        """
        Initialize the error.
        :param error_number: Int, The error message number.
        :param args: Object, Additional arguments to pass to Exception.
        """
        Exception.__init__(self, *args)
        self.error_number: int = error_number
        self.error_message: str = self._errorMessages[error_number]
        return


class Colours(object):
    """
    Classes and methods to store and generate, and validate colour / control strings.
        Class: Colours(object), Stores control strings by name, and validation methods.
            Class: Colours.ColourError(Exception)
            Method: Colours.is_control(value, raiseOnError), Return True if value is valid 4-Bit control string.
            Method: Colours.is_colour(value, raiseOnError), Return True if value is valid colour string, regardless of
                                                                bit length.
            Method: Colours.is_four_bit(value, raiseOnError), Return True if value is valid 4-Bit colour string.
            Method: Colours.is_eight_bit(value, raiseOnError), Return True if value is valid 8-Bit colour string.
            Method: Colours.is_sixteen_bit(value, raiseOnError), Return True if value is valid 16-Bit colour string.
            Method: Colours.is_foreground(value, raiseOnError), Return True if value is valid foreground colour string.
            Method: Colours.is_background(value, raiseOnError), Return True if value is valid background colour string.
            Class: Colours.fg(object), Stores 4-Bit foreground colour values by name.
                Method: Colours.fg.colour(value), Generate an 8-Bit foreground colour string, given colour value.
                Method: Colours.fg.rgb(red, green, blue), Generate a 16-Bit foreground colour string, given red, green,
                                                            and blue values.
            Class: Colours.bg(object), Stores 4-Bit background colour values by name.
                Method: Colours.bg.colour(value), Generate an 8-Bit background colour string, given colour value.
                Method: Colours.bg.rgb(red, green, blue), Generate a 16-Bit background colour string, given red, green,
                                                            and blue values.
    """
    # Control strings:
    reset: Final[str] = '\033[0m'
    """Reset all colours and styles to default."""
    bold: Final[str] = '\033[01m'
    """Apply bold intensity."""
    faint: Final[str] = '\033[02m'
    """Apply faint intensity."""
    italic: Final[str] = '\033[03m'
    """Apply italics. Not widely supported, usually results in reversed colours."""
    underline: Final[str] = '\033[04m'
    """Single underlining."""
    slow_blink: Final[str] = '\033[05m'
    """Blink font slowly. Not widely supported, usually results in a single blink rate."""
    fast_blink: Final[str] = '\033[06m'
    """Blink font fast. Not widely supported, usually results in a single blink rate."""
    reverse: Final[str] = '\033[07m'
    """Reverse the colours."""
    invisible: Final[str] = '\033[08m'
    """Don't show characters."""
    strike_through: Final[str] = '\033[09m'
    """Use strike through font."""
    default_font: Final[str] = '\033[10m'  # Font selection is not widely supported.
    """Switch to default font. Font selection is not widely supported, and usually results in no font change."""
    font_1: Final[str] = '\033[11m'
    """Switch to font #1. Font selection is not widely supported, and usually results in no font change."""
    font_2: Final[str] = '\033[12m'
    """Switch to font #2. Font selection is not widely supported, and usually results in no font change."""
    font_3: Final[str] = '\033[13m'
    """Switch to font #3. Font selection is not widely supported, and usually results in no font change."""
    font_4: Final[str] = '\033[14m'
    """Switch to font #4. Font selection is not widely supported, and usually results in no font change."""
    font_5: Final[str] = '\033[15m'
    """Switch to font #5. Font selection is not widely supported, and usually results in no font change."""
    font_6: Final[str] = '\033[16m'
    """Switch to font #6. Font selection is not widely supported, and usually results in no font change."""
    font_7: Final[str] = '\033[17m'
    """Switch to font #7. Font selection is not widely supported, and usually results in no font change."""
    font_8: Final[str] = '\033[18m'
    """Switch to font #8. Font selection is not widely supported, and usually results in no font change."""
    font_9: Final[str] = '\033[19m'
    """Switch to font #9.  Font selection is not widely supported, and usually results in no font change."""
    gothic_font: Final[str] = '\033[20m'
    """Switch to Gothic / Fraktur font. Font selection is not widely supported, usually results in no font change."""
    double_underline: Final[str] = '\033[21m'
    """Use double underlining. Not widely supported, usually results in single underlining."""
    reset_intensity: Final[str] = '\033[22m'
    """Reset the font intensity."""
    reset_italic: Final[str] = '\033[23m'
    """Reset italics."""
    reset_underline: Final[str] = '\033[24m'
    """Reset underlining, resets both single and double underlining."""
    reset_blinking: Final[str] = '\033[25m'
    """Reset the blink rate, resets both slow and fast blink."""
    proportional_spacing: Final[str] = '\033[26m'
    """Set proportional spacing. Not usually implemented."""
    reset_reverse: Final[str] = '\033[27m'
    """Resets the reverse colours."""
    reset_invisible: Final[str] = '\033[28m'
    """Resets the invisible font."""
    reset_strike_through: Final[str] = '\033[29m'
    """Reset strike through font."""
    # 30 -> 37: 4-bit fg colours.
    # 38: 8-bit / 16-bit fg colours.
    # 39: Default foreground colour.
    # 40 -> 47: 4-bit bg colours.
    # 48: 8-bit / 16-bit bg colours.
    # 49: Default background colour.
    reset_proportional_spacing: Final[str] = '\033[50m'
    """Reset proportional spacing. Rarely implemented."""

    def __init__(self) -> None:
        object.__init__(self)
        return

    @staticmethod
    def is_control(value: object, raise_on_false: bool = False) -> bool:
        """
        Return True if value is a valid 4-bit control string.
        :param value: Str, The value to check.
        :param raise_on_false: Raise ColourError instead of returning False
        :raises ColourError: If raise_on_false is True, and would return False.
        :return: bool: True if value is a valid 4-bit colour value.
        """
        if not isinstance(value, str):
            if raise_on_false:
                raise ColourError(10)
            else:
                return False
        four_bit_match: Match = _is_four_bit_regex.match(value)
        if four_bit_match is not None:
            if four_bit_match['value'] in _control_values:
                return True
        if raise_on_false:
            raise ColourError(10)
        else:
            return False

    @staticmethod
    def is_four_bit(value: object, raise_on_false: bool = False) -> bool:
        """
        Return True if value is a valid 4-bit colour string.
        :param value: Str, The value to check.
        :param raise_on_false: Bool, If true, raises ColourError instead of returning False.
        :raises ColourError: If raise_on_false is true and would return False.
        :return: Bool, True if value is valid 4-bit colour string.
        """
        if not isinstance(value, str):
            if raise_on_false:
                raise ColourError(12)
            else:
                return False
        four_bit_match: Match = _is_four_bit_regex.match(value)
        four_bit_values: list[str] = _four_bit_fg_values + _four_bit_bg_values
        if four_bit_match is not None:
            if four_bit_match['value'] in four_bit_values:
                return True
        if raise_on_false:
            raise ColourError(12)
        else:
            return False

    @staticmethod
    def is_eight_bit(value: object, raise_on_false: bool = False) -> bool:
        """
        Returns True if value is valid 8-Bit colour string.
        :param value: Str, The value to check.
        :param raise_on_false: If true, raises ColourError instead of returning False.
        :raises ColourError: If raise_on_false is True and would return False.
        :return: Bool, True if valid 8-bit colour string.
        """
        if not isinstance(value, str):
            if raise_on_false:
                raise ColourError(13)
            else:
                return False
        eight_bit_match: Match = _is_eight_bit_regex.match(value)
        if eight_bit_match is not None:
            if __value_is_valid__(eight_bit_match['value']):
                return True
        if raise_on_false:
            raise ColourError(13)
        else:
            return False

    @staticmethod
    def is_sixteen_bit(value: object, raise_on_false=False) -> bool:
        """
        Return True if value is valid 16-bit colour string.
        :param value: Str, The value to check.
        :param raise_on_false: If True, raises ColourError instead of returning False.
        :raises ColourError: If raise_on_false is True and would return False.
        :return: Bool, True if value is a valid 16-bit colour string.
        """
        if not isinstance(value, str):
            if raise_on_false:
                raise ColourError(14)
            else:
                return False
        sixteen_bit_match: Match = _is_sixteen_bit_regex.match(value)
        if sixteen_bit_match is not None:
            red_good = __value_is_valid__(sixteen_bit_match['red'])
            green_good = __value_is_valid__(sixteen_bit_match['green'])
            blue_good = __value_is_valid__(sixteen_bit_match['blue'])
            if red_good is True and green_good is True and blue_good is True:
                return True
        if raise_on_false:
            raise ColourError(14)
        else:
            return False

    @classmethod
    def is_colour(cls, value: object, raise_on_false: bool = False) -> bool:
        """
        Return True if value is a valid colour string of any bit length.
        :param value: The value to check.
        :param raise_on_false: If True, raises ColourError instead of returning False.
        :raises ColourError: If raise_on_false is True and would return False.
        :return: Bool, True if valid colour string.
        """
        if not isinstance(value, str):
            if raise_on_false:
                raise ColourError(11)
            else:
                return False
        if cls.is_four_bit(value) is True or cls.is_eight_bit(value) is True or cls.is_sixteen_bit(value) is True:
            return True
        if raise_on_false:
            raise ColourError(11)
        else:
            return False

    @classmethod
    def is_foreground(cls, value: object, raise_on_false: bool = False) -> bool:
        """
        Return True if value is valid foreground colour of any bit length.
        :param value: The value to check.
        :param raise_on_false: If True, raises ColourError instead of returning False.
        :raises ColourError: If raise_on_false is True and would return False.
        :return: Bool, True if value is valid foreground colour string.
        """
        if not isinstance(value, str):
            if raise_on_false:
                raise ColourError(15)
            else:
                return False
        if not cls.is_colour(value):
            if raise_on_false:
                raise ColourError(15)
            else:
                return False
        four_bit_match: Match = _is_four_bit_regex.match(value)
        eight_bit_match: Match = _is_eight_bit_regex.match(value)
        sixteen_bit_match: Match = _is_sixteen_bit_regex.match(value)
        if four_bit_match is not None:
            if four_bit_match['value'] in _four_bit_fg_values:
                return True
        elif eight_bit_match is not None:
            if eight_bit_match['fgBg'] == _eight_bit_fg_value:
                return True
        elif sixteen_bit_match is not None:
            if sixteen_bit_match['fgBg'] == _sixteen_bit_fg_value:
                return True
        if raise_on_false:
            raise ColourError(15)
        else:
            return False

    @classmethod
    def is_background(cls, value: object, raise_on_false: bool = False) -> bool:
        """
        Return True if value is valid background colour of any bit length.
        :param value: The value to check.
        :param raise_on_false: If True, raises ColourError instead of returning False.
        :raises ColourError: If raise_on_false is True and would return False.
        :return: Bool, True f valid background colour.
        """
        if not isinstance(value, str):
            if raise_on_false:
                raise ColourError(16)
            else:
                return False
        if not cls.is_colour(value):
            if raise_on_false:
                raise ColourError(16)
            else:
                return False
        four_bit_match: Match = _is_four_bit_regex.match(value)
        eight_bit_match: Match = _is_eight_bit_regex.match(value)
        sixteen_bit_match: Match = _is_sixteen_bit_regex.match(value)
        if four_bit_match is not None:
            if four_bit_match['value'] in _four_bit_bg_values:
                return True
        elif eight_bit_match is not None:
            if eight_bit_match['fgBg'] == _eight_bit_bg_value:
                return True
        elif sixteen_bit_match is not None:
            if sixteen_bit_match['fgBg'] == _sixten_bit_bg_value:
                return True
        if raise_on_false:
            raise ColourError(16)
        else:
            return False

    # Foreground
    class FG(object):
        """Foreground Colours."""
        # 4 bit colour (16 Colours)
        default: Final[str] = '\033[39m'
        """Default foreground colour."""
        black: Final[str] = '\033[30m'
        """Foreground black."""
        red: Final[str] = '\033[31m'
        """Foreground red."""
        green: Final[str] = '\033[32m'
        """Foreground green."""
        orange: Final[str] = '\033[33m'
        """Foreground orange."""
        blue: Final[str] = '\033[34m'
        """Foreground blue."""
        purple: Final[str] = '\033[35m'
        """Foreground purple."""
        cyan: Final[str] = '\033[36m'
        """Foreground cyan."""
        light_grey: Final[str] = '\033[37m'
        """Foreground light grey."""
        dark_grey: Final[str] = '\033[90m'
        """Foreground dark grey."""
        light_red: Final[str] = '\033[91m'
        """Foreground light red."""
        light_green: Final[str] = '\033[92m'
        """Foreground light green."""
        yellow: Final[str] = '\033[93m'
        """Foreground yellow."""
        light_blue: Final[str] = '\033[94m'
        """Foreground light blue."""
        pink: Final[str] = '\033[95m'
        """Foreground pink."""
        light_cyan: Final[str] = '\033[96m'
        """Foreground light cyan."""
        white: Final[str] = '\033[97m'
        """Foreground white."""

        # 8-bit foreground colour (256 Colours):
        @staticmethod
        def colour(value: int) -> str:
            """
            Get an 8-Bit foreground colour:
            :param value: int, The colour value (0-255).
            :raises ColourError: On type error, or value error.
            :return: Str, The 8-bit colour string.
            """
            # Type check:
            if not isinstance(value, int):
                raise ColourError(1)
            # Value check:
            if value < 0 or value > 255:
                raise ColourError(6)
            return '\033[38;5;%im' % value

        # 16-bit foreground colour (65,536 Colours)
        @staticmethod
        def rgb(red: int, green: int, blue: int) -> str:
            """
            Get a 16-Bit foreground colour.
            :param red: Int, The red value (0-255).
            :param green: Int, The green value (0-255).
            :param blue: Int, The blue value (0-255).
            :return: Str, The 16-bit colour string.
            """
            # Type check:
            if not isinstance(red, int):
                raise ColourError(2)
            if not isinstance(green, int):
                raise ColourError(3)
            if not isinstance(blue, int):
                raise ColourError(4)
            # Value check:
            if red < 0 or red > 255:
                raise ColourError(7)
            if green < 0 or green > 255:
                raise ColourError(8)
            if blue < 0 or blue > 255:
                raise ColourError(9)
            return '\033[38;2;%i;%i;%im' % (red, green, blue)

    # Background:
    class BG(object):
        """Background Colours."""
        # 4 bit colour (16 Colours)
        default: Final[str] = '\033[49m'
        """Default background colour."""
        black: Final[str] = '\033[40m'
        """Background black."""
        red: Final[str] = '\033[41m'
        """Background red."""
        green: Final[str] = '\033[42m'
        """Background green."""
        orange: Final[str] = '\033[43m'
        """Background orange."""
        blue: Final[str] = '\033[44m'
        """Background blue."""
        purple: Final[str] = '\033[45m'
        """Background purple."""
        cyan: Final[str] = '\033[46m'
        """Background cyan."""
        light_grey: Final[str] = '\033[47m'
        """Background light grey."""
        dark_grey: Final[str] = '\033[100m'
        """Background dark grey."""
        light_red: Final[str] = '\033[101m'
        """Background light red."""
        light_green: Final[str] = '\033[102m'
        """Background light green."""
        yellow: Final[str] = '\033[103m'
        """Background yellow."""
        lightblue: Final[str] = '\033[104m'
        """Background light blue."""
        pink: Final[str] = '\033[105m'
        """Background pink."""
        light_cyan: Final[str] = '\033[106m'
        """Background light cyan."""
        white: Final[str] = '\033[107m'
        """Background white."""

        # 8-bit background colour (255 Colours):
        @staticmethod
        def colour(value: int) -> str:
            """
            Get an 8-bit background colour.
            :param value : Int, The colour number, valid values are: 0-255.
            :raises ColourError : On type error or value error
            :returns: Str, The colour string.
            """
            if not isinstance(value, int):
                raise ColourError(1)
            if value < 0 or value > 255:
                raise ColourError(6)
            return '\033[48;5;%im' % value

        # 16-bit background colour (65,536 Colours)
        @staticmethod
        def rgb(red: int, green: int, blue: int):
            """
            Get a 16-bit background colour.
            :param red: Int, The red value (0-255).
            :param green: Int, The green value (0-255).
            :param blue: Int, The blue value (0-255).
            :raises ColourError: On type error or value error.
            :return: Str, The 16-bit colour string.
            """
            # Type check:
            if not isinstance(red, int):
                raise ColourError(2)
            if not isinstance(green, int):
                raise ColourError(3)
            if not isinstance(blue, int):
                raise ColourError(4)
            # Value check:
            if red < 0 or red > 255:
                raise ColourError(7)
            if green < 0 or green > 255:
                raise ColourError(8)
            if blue < 0 or blue > 255:
                raise ColourError(9)
            return '\033[48;2;%i;%i;%im' % (red, green, blue)
