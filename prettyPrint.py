#!/usr/bin/env python3
"""
    Pretty print methods and error_number class.
        Class PrettyPrintError(Exception), error_number messages.
        Methods:
            print_coloured: Print a coloured message.
            print_time_stamp: Print a timestamp.
            print_date_stamp: Print a datestamp.
            print_date_time_stamp: Print a date / time stamp.
            print_debug: Print a debug message.
            print_error: Print an error_number message.
            print_info: Print an info message.
            print_warning: Print a warning message.
"""
from typing import Optional
from terminal import Colours
from datetime import datetime
VERSION: float = 1.02

DEBUG: bool = False
VERBOSE: bool = False


class PrettyPrintError(Exception):
    """Class for all pretty print errors."""
    _errorMessages: dict[int, str] = {
        0: 'No error_number.',
        1: 'TypeError: message must be a string.',
        2: 'TypeError: fg_colour must be a string or None.',
        3: 'ValueError: fg_colour must be a valid foreground colour string.',
        4: 'TypeError: bg_colour must be a string or None.',
        5: 'ValueError: bg_colour must be a valid colour string.',
        6: 'TypeError: bold must be a bool.',
        7: 'TypeError: underline must be a bool.',
        8: 'TypeError: reverse must be a bool.',
        9: 'TypeError: strike_through must be a bool.',
        10: 'TypeError: blink must be a bool.',
        11: 'TypeError: add_micros must be a bool.',
        12: 'TypeError: open_bracket must be a str.',
        13: 'ValueError: open_bracket must be a single character.',
        14: 'TypeError: close_bracket must be a str.',
        15: 'ValueError: close_bracket must be a single character.',
        16: 'TypeError: seperator must be a str.',
        17: 'ValueError: seperator must be a single character.',
        18: 'TypeError: micros_seperator must be a str.',
        19: 'ValueError: micros_seperator must be a single character.',
        20: 'TypeError: end must be a str.',
        21: 'TypeError: date_seperator must be a str.',
        22: 'ValueError: date_seperator must be a single character.',
        23: 'TypeError: time_seperator must be a str.',
        24: 'ValueError: time_seperator must be a single character.',
        25: 'TypeError: append must be a bool.',
        26: 'TypeError: restart must be a bool.',
        27: 'TypeError: force must be a bool.',
        28: 'ArgumentConflict: Cannot append and restart at the same time.',
        29: 'TypeError: do_print must be a bool.',
        30: 'TypeError: flush must be a bool.',
    }

    def __init__(self, error_number: int, *args: object) -> None:
        super().__init__(*args)
        self.error_number: int = error_number
        self.error_message: str = self._errorMessages[error_number]
        return


def print_coloured(
        message: str,
        fg_colour: Optional[str] = None,
        bg_colour: Optional[str] = None,
        bold: bool = False,
        underline: bool = False,
        reverse: bool = False,
        strike_through: bool = False,
        blink: bool = False,
        **kw_args,
) -> None:
    """
        Pretty print a message.
        :param message : Str, Message to print.
        :param fg_colour : Str, Foreground colour.
        :param bg_colour : Optional[str], Background colour. Defaults to None.
        :param bold : Bool, Use bold font. Defaults to False.
        :param underline : Bool, Use underlining. Defaults to False.
        :param reverse : Bool, Reverse the Colours. Defaults to False.
        :param strike_through : Bool, Use strike through. Defaults to False.
        :param blink : Bool, Use blinking font (not supported on all terminals.).
        :param kw_args : Dict[str, object], Keyword arguments are passed directly to print.
        :raises PrettyPrintError : On type error or value error.
        :returns: None
    """
    # Argument checks:
    # Message:
    if not isinstance(message, str):
        raise PrettyPrintError(1)
    # Foreground colour:
    if fg_colour is not None and isinstance(fg_colour, str) is False:
        raise PrettyPrintError(2)
    elif fg_colour is not None and Colours.is_foreground(fg_colour) is False:
        raise PrettyPrintError(3)
    # Background colour:
    if bg_colour is not None and isinstance(bg_colour, str) is False:
        raise PrettyPrintError(4)
    elif bg_colour is not None and Colours.is_background(bg_colour) is False:
        raise PrettyPrintError(5)
    # Bold:
    if isinstance(bold, bool) is False:
        raise PrettyPrintError(6)
    # Underline:
    if isinstance(underline, bool) is False:
        raise PrettyPrintError(7)
    # Reverse:
    if isinstance(reverse, bool) is False:
        raise PrettyPrintError(8)
    # Strike through:
    if isinstance(strike_through, bool) is False:
        raise PrettyPrintError(9)
    # Blink:
    if isinstance(blink, bool) is False:
        raise PrettyPrintError(10)
    line = ''
    if fg_colour is not None:
        line += fg_colour
    if bg_colour is not None:
        line += bg_colour
    if bold:
        line += Colours.bold
    if underline:
        line += Colours.underline
    if reverse:
        line += Colours.reverse
    if strike_through:
        line += Colours.strike_through
    if blink:
        line += Colours.slow_blink
    line += message + Colours.reset
    print(line, **kw_args)
    return


def print_time_stamp(
        fg_colour: Optional[str] = Colours.FG.green,
        bg_colour: Optional[str] = None,
        bold: bool = False,
        underline: bool = False,
        strike_through: bool = False,
        reverse: bool = False,
        add_micros: bool = False,
        open_bracket: Optional[str] = '[',
        close_bracket: Optional[str] = ']',
        seperator: str = ':',
        micros_seperator: str = '.',
        end: str = '',
        flush: bool = True,
        do_print: bool = True,
        **kw_args: dict,
) -> str:
    """
        Pretty print a time stamp.
        :param fg_colour : Str: Foreground colour, defaults to Colours.fg.green
        :param bg_colour : Optional[str], Background colour. Defaults to None.
        :param bold : Bool, Use bold font. Default False.
        :param underline : Bool, Use underlining. Defaults to False.
        :param strike_through : Bool, Use strike through. Defaults to False.
        :param reverse : Bool, Use reverse colouring. Defaults to False.
        :param add_micros : Bool, Add microseconds to the timestamp. Defaults to False.
        :param open_bracket : Optional[str], What to use as an open bracket. Defaults to '['.
        :param close_bracket : Optional[str], What to use as a close bracket. Defaults to ']'.
        :param seperator : Str, What to use to separate the time elements. Defaults to ':'.
        :param micros_seperator : Str, What to use to separate microseconds from seconds. Defaults to '.'.
        :param end : Str, What to pass to print as the end argument, defaults to ''.
        :param flush: Bool, What to pass to print as the flush argument, defaults to True.
        :param do_print : Bool, Print the time stamp, set to false if just collecting the str. Defaults to True.
        :param kw_args : Dict[str, object], Keyword arguments are passed directly to print.
        :raises PrettyPrintError : On type error or value error.
        :returns: Str: The timestamp without any colours.
    """
    # Argument Checks:
    # Foreground colour:
    if fg_colour is not None and isinstance(fg_colour, str) is False:
        raise PrettyPrintError(2)
    elif fg_colour is not None and Colours.is_foreground(fg_colour) is False:
        raise PrettyPrintError(3)
    # Background colour:
    if bg_colour is not None and isinstance(bg_colour, str) is False:
        raise PrettyPrintError(4)
    elif bg_colour is not None and Colours.is_background(bg_colour) is False:
        raise PrettyPrintError(5)
    # Bold:
    if not isinstance(bold, bool):
        raise PrettyPrintError(6)
    # Underline:
    if not isinstance(underline, bool):
        raise PrettyPrintError(7)
    # Reverse:
    if not isinstance(reverse, bool):
        raise PrettyPrintError(8)
    # Strikethrough:
    if not isinstance(strike_through, bool):
        raise PrettyPrintError(9)
    # Add Micros
    if not isinstance(add_micros, bool):
        raise PrettyPrintError(11)
    # Open bracket:
    if not isinstance(open_bracket, str):
        raise PrettyPrintError(12)
    elif len(open_bracket) != 1:
        raise PrettyPrintError(13)
    # Close bracket:
    if not isinstance(close_bracket, str):
        raise PrettyPrintError(14)
    elif len(close_bracket) != 1:
        raise PrettyPrintError(15)
    # Seperator:
    if not isinstance(seperator, str):
        raise PrettyPrintError(16)
    elif len(seperator) != 1:
        raise PrettyPrintError(17)
    # Micros seperator:
    if not isinstance(micros_seperator, str):
        raise PrettyPrintError(18)
    elif len(micros_seperator) != 1:
        raise PrettyPrintError(19)
    # end:
    if not isinstance(end, str):
        raise PrettyPrintError(20)
    # Do print:
    if not isinstance(do_print, bool):
        raise PrettyPrintError(29)
    # Flush:
    if not isinstance(flush, bool):
        raise PrettyPrintError(30)
    # Get date / time:
    now: datetime = datetime.now()
    # Build the timestamp:
    time_stamp = ''
    if open_bracket is not None:
        time_stamp += open_bracket
    time_stamp += "%02i%s%02i%s%02i" % (now.hour, seperator, now.minute, seperator, now.second)
    if add_micros:
        time_stamp += "%s%05i" % (micros_seperator, now.microsecond)
    if close_bracket is not None:
        time_stamp += close_bracket
    # Print to screen:
    if do_print:
        print_coloured(time_stamp, fg_colour=fg_colour, bg_colour=bg_colour, bold=bold, underline=underline,
                       strike_through=strike_through, reverse=reverse, end=end, flush=flush, **kw_args)
    return time_stamp


def print_date_stamp(
        fg_colour: Optional[str] = Colours.FG.green,
        bg_colour: Optional[str] = None,
        bold: bool = False,
        underline: bool = False,
        strike_through: bool = False,
        reverse: bool = False,
        open_bracket: Optional[str] = '[',
        close_bracket: Optional[str] = ']',
        seperator: str = '-',
        end: str = '',
        flush: bool = True,
        do_print: bool = True,
        **kw_args,
        ) -> str:
    """
        Pretty print a date stamp.
        :param fg_colour : Str, Foreground colour, defaults to Colours.fg.green.
        :param bg_colour : Optional[str], Background colour. Defaults to None.
        :param bold : Bool, Use bold font. Default False.
        :param underline : Bool, Use underlining. Defaults to False.
        :param strike_through : Bool, Use strike through. Defaults to False.
        :param reverse : Bool, Use reverse colouring. Defaults to False.
        :param open_bracket : Str, What to use as an open bracket. Defaults to '['.
        :param close_bracket : Str, What to use as a close bracket. Defaults to ']'.
        :param seperator : Str, What to use to separate the date elements. Defaults to '-'.
        :param end : Str, What to pass to print as the end argument. Defaults to ''.
        :param flush: Bool, What to pass to print as the flush argument. Defaults to True.
        :param do_print : Bool, True, call print, set to False if just collecting the str. Defaults to True.
        :param kw_args : Dict, Keyword arguments are passed directly to print.
        :raises PrettyPrintError : On type error or on value error.
        :returns: Str: The datestamp without colours.
    """
    # Argument Checks:
    # Foreground colour:
    if fg_colour is not None and isinstance(fg_colour, str) is False:
        raise PrettyPrintError(2)
    elif fg_colour is not None and Colours.is_foreground(fg_colour) is False:
        raise PrettyPrintError(3)
    # Background Colour:
    if bg_colour is not None and isinstance(bg_colour, str) is False:
        raise PrettyPrintError(4)
    elif bg_colour is not None and Colours.is_background(bg_colour) is False:
        raise PrettyPrintError(5)
    # Bold:
    if not isinstance(bold, bool):
        raise PrettyPrintError(6)
    # Underline:
    if not isinstance(underline, bool):
        raise PrettyPrintError(7)
    # Reverse:
    if not isinstance(reverse, bool):
        raise PrettyPrintError(8)
    # Strike through:
    if not isinstance(strike_through, bool):
        raise PrettyPrintError(9)
    # Open bracket:
    if not isinstance(open_bracket, str):
        raise PrettyPrintError(12)
    elif len(open_bracket) != 1:
        raise PrettyPrintError(13)
    # Close Bracket:
    if not isinstance(close_bracket, str):
        raise PrettyPrintError(14)
    elif len(close_bracket) != 1:
        raise PrettyPrintError(15)
    # Seperator:
    if not isinstance(seperator, str):
        raise PrettyPrintError(16)
    elif len(close_bracket) != 1:
        raise PrettyPrintError(17)
    # End:
    if not isinstance(end, str):
        raise PrettyPrintError(20)
    # Do Print:
    if not isinstance(do_print, bool):
        raise PrettyPrintError(29)
    # Flush:
    if not isinstance(flush, bool):
        raise PrettyPrintError(30)
    # Get the date / time:
    now: datetime = datetime.now()
    # Build the date stamp:
    date_stamp: str = ''
    if open_bracket is not None:
        date_stamp += open_bracket
    date_stamp += "%02i%s%02i%s%4i" % (now.day, seperator, now.month, seperator, now.year)
    if close_bracket is not None:
        date_stamp += close_bracket
    # Print the date stamp:
    if do_print:
        print_coloured(date_stamp, fg_colour=fg_colour, bg_colour=bg_colour, bold=bold, underline=underline,
                       strike_through=strike_through, reverse=reverse, end=end, flush=flush, **kw_args)
    return date_stamp


def print_date_time_stamp(
        fg_colour: Optional[str] = Colours.FG.green,
        bg_colour: Optional[str] = None,
        bold: bool = False,
        underline: bool = False,
        strike_through: bool = False,
        reverse: bool = False,
        add_micros: bool = False,
        open_bracket: Optional[str] = '[',
        close_bracket: Optional[str] = ']',
        date_seperator: str = '-',
        time_seperator: str = ':',
        micros_seperator: str = '.',
        date_time_seperator: str = ' ',
        end: str = '',
        flush: bool = True,
        do_print: bool = True,
        **kw_args,
        ) -> str:
    """
        Pretty print a date and time stamp.
        :param fg_colour : Str, Foreground colour, defaults to Colours.fg.green.
        :param bg_colour : Optional[str], Background colour. Defaults to None.
        :param bold : Bool, Use bold font. Default False.
        :param underline : Bool, Use underlining. Defaults to False.
        :param strike_through : Bool, Use strike through. Defaults to False.
        :param reverse : Bool, Use reverse colouring. Defaults to False.
        :param add_micros : Bool, Add microseconds to the timestamp. Defaults to False.
        :param open_bracket : Str, What to use as an open bracket. Defaults to '['.
        :param close_bracket : Str, What to use as a close bracket. Defaults to ']'.
        :param date_seperator : Str, What to use to separate the date elements Defaults to '-'.
        :param time_seperator : Str, What to use to separate the time elements. Defaults to ':'.
        :param micros_seperator: Str, What to use to separate microseconds from seconds. Defaults to '.'.
        :param date_time_seperator: Str, what to use to separate the date from the time. Defaults to ' '.
        :param end: Str, What to pass to print as the end argument. Defaults to ''.
        :param flush: Bool, What to pass to print as the flush argument. Defaults to True.
        :param do_print: Bool, Do the print, set to False if just collecting the str. Defaults to True.
        :param kw_args: Dict[str, object], Keyword arguments are passed directly to print.
        :raises PrettyPrintError : On type error or on value error.
        :returns: Str: The date/time stamp without colours.
    """
    # Argument checks:
    # Foreground colour:
    if fg_colour is not None and isinstance(fg_colour, str) is False:
        raise PrettyPrintError(2)
    elif fg_colour is not None and Colours.is_foreground(fg_colour) is False:
        raise PrettyPrintError(3)
    # Background colour:
    if bg_colour is not None and isinstance(bg_colour, str) is False:
        raise PrettyPrintError(4)
    elif bg_colour is not None and Colours.is_background(bg_colour) is False:
        raise PrettyPrintError(5)
    # Bold:
    if not isinstance(bold, bool):
        raise PrettyPrintError(6)
    # Underline:
    if not isinstance(underline, bool):
        raise PrettyPrintError(7)
    # Reverse:
    if not isinstance(reverse, bool):
        raise PrettyPrintError(8)
    # Strike through:
    if not isinstance(strike_through, bool):
        raise PrettyPrintError(9)
    # Add Microseconds:
    if not isinstance(add_micros, bool):
        raise PrettyPrintError(11)
    # Open bracket:
    if not isinstance(open_bracket, str):
        raise PrettyPrintError(12)
    elif len(open_bracket) != 1:
        raise PrettyPrintError(13)
    # Close bracket:
    if not isinstance(close_bracket, str):
        raise PrettyPrintError(14)
    elif len(close_bracket) != 1:
        raise PrettyPrintError(15)
    # Date seperator:
    if not isinstance(date_seperator, str):
        raise PrettyPrintError(21)
    elif len(date_seperator) != 1:
        raise PrettyPrintError(22)
    # Time seperator:
    if not isinstance(time_seperator, str):
        raise PrettyPrintError(23)
    elif len(time_seperator) != 1:
        raise PrettyPrintError(24)
    # Micros seperator:
    if not isinstance(micros_seperator, str):
        raise PrettyPrintError(18)
    elif len(micros_seperator) != 1:
        raise PrettyPrintError(19)
    # End:
    if not isinstance(end, str):
        raise PrettyPrintError(20)
    # Do print:
    if not isinstance(do_print, bool):
        raise PrettyPrintError(29)
    # Flush:
    if not isinstance(flush, bool):
        raise PrettyPrintError(30)
    # Get the date and time:
    now: datetime = datetime.now()
    # Build the date time stamp:
    date_time_stamp = ''
    if open_bracket is not None:
        date_time_stamp += open_bracket
    date_time_stamp += "%02i%s%02i%s%4i" % (now.day, date_seperator, now.month, date_seperator, now.year)
    date_time_stamp += date_time_seperator
    date_time_stamp += "%02i%s%02i%s%02i" % (
        now.hour, time_seperator, now.minute, time_seperator, now.second)
    if add_micros:
        date_time_stamp += "%s%05i" % (micros_seperator, now.microsecond)
    if close_bracket is not None:
        date_time_stamp += close_bracket
    # Print the date time stamp:
    if do_print:
        print_coloured(date_time_stamp, fg_colour=fg_colour, bg_colour=bg_colour, bold=bold, underline=underline,
                       reverse=reverse, strike_through=strike_through, end=end, flush=flush, **kw_args)
    return date_time_stamp


def print_debug(
        message: object,
        append: bool = False,
        restart: bool = False,
        force: bool = False,
        fg_colour: Optional[str] = None,
        bg_colour: Optional[str] = None,
        end: str = '\n',
        flush: bool = True,
        **kw_args,
        ) -> None:
    """
        Pretty print a debug message, only if DEBUG is true.
        :param message : Object, Message to print, note str(message) is called.
        :param append : Bool, Append to the message, skips printing title, defaults to False.
        :param restart : Bool, Restart a message, print a newline before printing the title., defaults to False.
        :param force : Bool, Force printing the message, ignores DEBUG, defaults to False.
        :param fg_colour : Str, Foreground colour, defaults to Colours.fg.purple.
        :param bg_colour : Optional[str], Background colour, defaults to None.
        :param end : Str, What to pass to print as the end parameter, defaults to '\\n'.
        :param flush : Bool, What to pass to print as the flush argument, defaults to True.
        :param kw_args : Dict[str, object], Keyword arguments are passed directly to print.
        :raises PrettyPrintError : On type error or value error.
        :returns: None
    """
    # Argument Checks:
    # Append:
    if not isinstance(append, bool):
        raise PrettyPrintError(25)
    # Restart:
    if not isinstance(restart, bool):
        raise PrettyPrintError(26)
    # Force:
    if not isinstance(force, bool):
        raise PrettyPrintError(27)
    # Foreground Colour:
    if fg_colour is not None and isinstance(fg_colour, str) is False:
        raise PrettyPrintError(2)
    elif fg_colour is not None and Colours.is_foreground(fg_colour) is False:
        raise PrettyPrintError(3)
    # Background colour:
    if bg_colour is not None and isinstance(bg_colour, str) is False:
        raise PrettyPrintError(4)
    elif bg_colour is not None and Colours.is_background(bg_colour) is False:
        raise PrettyPrintError(5)
    # End:
    if not isinstance(end, str):
        raise PrettyPrintError(20)
    # Flush:
    if not isinstance(flush, bool):
        raise PrettyPrintError(30)
    # Set fg_colour to default purple:
    if fg_colour is None:
        fg_colour = Colours.FG.purple

    message = str(message)
    if append is True and restart is True:
        raise PrettyPrintError(28)
    if DEBUG is False and force is False:
        return
    if restart:
        print('\n', end='', **kw_args)
    if not append:
        print_coloured("DEBUG:", fg_colour=fg_colour, bg_colour=bg_colour, bold=True, end=' ', flush=flush, **kw_args)
    print(message, end=end, flush=flush, **kw_args)
    return


def print_error(
        message: object,
        append: bool = False,
        restart: bool = False,
        fg_colour: Optional[str] = None,
        bg_colour: Optional[str] = None,
        end: str = '\n',
        flush: bool = True,
        **kw_args,
) -> None:
    """
        Pretty print an error_number message.
        :param message : Object, Message to print, note str(message) is called.
        :param append : Bool, Append to the message, skips printing title, defaults to False.
        :param restart : Bool, Restart a message, print a newline before printing the title, defaults to False.
        :param fg_colour : Str, Foreground colour, defaults to Colours.fg.red.
        :param bg_colour : Optional[str], Background colour, defaults to None.
        :param end : Str, What to pass to print as the end parameter, defaults to '\\n'.
        :param flush : Bool, What to pas to print as the flush argument, defaults to True.
        :param kw_args: Dict, Keyword arguments are passed directly to print.
        :raises PrettyPrintError: On type error or value error.
        :returns: None
    """
    # Argument checks:
    # Append:
    if not isinstance(append, bool):
        raise PrettyPrintError(25)
    # Restart:
    if not isinstance(restart, bool):
        raise PrettyPrintError(26)
    # Foreground colour:
    if fg_colour is not None and isinstance(fg_colour, str) is False:
        raise PrettyPrintError(2)
    elif fg_colour is not None and Colours.is_foreground(fg_colour) is False:
        raise PrettyPrintError(3)
    # Background Colour:
    if bg_colour is not None and isinstance(bg_colour, str) is False:
        raise PrettyPrintError(4)
    elif bg_colour is not None and Colours.is_background(bg_colour) is False:
        raise PrettyPrintError(5)
    # End:
    if not isinstance(end, str):
        raise PrettyPrintError(20)
    # Flush:
    if not isinstance(flush, bool):
        raise PrettyPrintError(30)
    # Set default colour if None:
    if fg_colour is None:
        fg_colour = Colours.FG.red
    message = str(message)
    if append is True and restart is True:
        raise PrettyPrintError(28)
    if restart:
        print('\n', end='', **kw_args)
    if not append:
        print_coloured("ERROR:", fg_colour=fg_colour, bg_colour=bg_colour, bold=True, end=' ', flush=flush, **kw_args)
    print(message, end=end, flush=flush, **kw_args)
    return


def print_info(
        message: object,
        append: bool = False,
        restart: bool = False,
        force: bool = False,
        fg_colour: Optional[str] = None,
        bg_colour: Optional[str] = None,
        end: str = '\n',
        flush: bool = True,
        **kw_args,
        ) -> None:
    """
        Pretty print an info message, only if VERBOSE is true.
        :param message : Object, Message to print, note str(message) is called.
        :param append : Bool, Append to the message, skips printing title, defaults to False.
        :param restart : Bool, Restart a message, print a newline before printing the title, defaults to False.
        :param fg_colour : Str, Foreground colour, defaults to Colours.fg.green.
        :param bg_colour : Optional[str], Background colour, defaults to None.
        :param force : Bool, Force printing the message, ignores VERBOSE, defaults to False.
        :param end : Str, What to pass to print as the end parameter, defaults to '\\n'.
        :param flush : Bool, What to pass to print as the flush parameter, defaults to True.
        :param kw_args: Dict[str, object], Keyword arguments are passed directly to print.
        :raises PrettyPrintError: On type error or value error.
        :returns: None
    """
    # Argument Checks:
    # Append:
    if not isinstance(append, bool):
        raise PrettyPrintError(25)
    # Restart:
    if not isinstance(restart, bool):
        raise PrettyPrintError(26)
    # Force:
    if not isinstance(force, bool):
        raise PrettyPrintError(27)
    # Foreground Colour:
    if fg_colour is not None and not isinstance(fg_colour, str):
        raise PrettyPrintError(2)
    elif fg_colour is not None and not Colours.is_foreground(fg_colour):
        raise PrettyPrintError(3)
    # Background colour:
    if bg_colour is not None and not isinstance(bg_colour, str):
        raise PrettyPrintError(4)
    elif bg_colour is not None and not Colours.is_background(bg_colour):
        raise PrettyPrintError(5)
    # End:
    if not isinstance(end, str):
        raise PrettyPrintError(20)
    # Flush:
    if not isinstance(flush, bool):
        raise PrettyPrintError(30)
    # Set default colour:
    if fg_colour is None:
        fg_colour = Colours.FG.green
    message = str(message)
    if append is True and restart is True:
        error_message = "Can't restart and append at the same time."
        raise RuntimeError(error_message)
    if VERBOSE is False and force is False:
        return
    if restart:
        print('\n', end='', **kw_args)
    if not append:
        print_coloured("INFO:", fg_colour=fg_colour, bg_colour=bg_colour, bold=True, end=' ', flush=flush, **kw_args)
    print(message, end=end, flush=flush, **kw_args)
    return


def print_warning(
        message: object,
        append: bool = False,
        restart: bool = False,
        fg_colour: Optional[str] = None,
        bg_colour: Optional[str] = None,
        end: str = '\n',
        flush: bool = True,
        **kw_args,
) -> None:
    """
        Pretty print a warning message.
        :param message : Object, Message to print, note str(message) is called.
        :param append : Bool, Append to the message, skips printing title, defaults to False.
        :param restart : Bool, Restart a message, print a newline before printing the title, defaults to False.
        :param fg_colour : Str, Foreground colour, defaults to Colours.fg.orange.
        :param bg_colour : Optional[str], Background colour, defaults to None.
        :param end : Str, What to pass to print as the end parameter, defaults to '\\n'.
        :param flush: Bool: What to pass to print for flush parameter, defaults to True.
        :param kw_args: Keyword arguments are passed directly to print.
        :raises PrettyPrintError: On type error or value error.
"""
    # Argument checks:
    # Append:
    if not isinstance(append, bool):
        raise PrettyPrintError(25)
    # Restart:
    if not isinstance(restart, bool):
        raise PrettyPrintError(26)
    # Foreground colour:
    if fg_colour is not None and not isinstance(fg_colour, str):
        raise PrettyPrintError(2)
    elif fg_colour is not None and not Colours.is_foreground(fg_colour):
        raise PrettyPrintError(3)
    # Background Colour:
    if bg_colour is not None and not isinstance(bg_colour, str):
        raise PrettyPrintError(4)
    elif bg_colour is not None and not Colours.is_background(bg_colour):
        raise PrettyPrintError(5)
    # End:
    if not isinstance(end, str):
        raise PrettyPrintError(20)
    # Flush:
    if not isinstance(flush, bool):
        raise PrettyPrintError(30)
    # Set default colour:
    if fg_colour is None:
        fg_colour = Colours.FG.orange
    message = str(message)
    if append is True and restart is True:
        error_message = "Can't restart and append at the same time."
        raise RuntimeError(error_message)
    if restart:
        print('\n', end=end, **kw_args)
    if not append:
        print_coloured("WARNING:", fg_colour=fg_colour, bg_colour=bg_colour, bold=True, end=' ', flush=flush, **kw_args)
    print(message, end=end, flush=flush, **kw_args)
    return


if __name__ == '__main__':
    print("print_info: verbose = false... produces nothing, print info, verbose = true, produces output.")
    VERBOSE = False
    print_info("This produces nothing.")
    # noinspection PyRedeclaration
    VERBOSE = True
    print_info("This produces output.")
    print("print_debug: debug = False, produces no output, debug = true, produces output.")
    DEBUG = False
    print_debug("No output.")
    # noinspection PyRedeclaration
    DEBUG = True
    print_debug("this produces output.")
    print("print_warning, and print error_number print regardless.")
    print_warning("THis is a warning.")
    print_error("This is an error_number.")
    usage_message = "print_debug and print_info have the option force, which overrides the values of DEBUG and VERBOSE,"
    usage_message += "and prints anyway."
    print(usage_message)

    # noinspection PyRedeclaration
    DEBUG = False
    print_debug("This is a test", force=True)
    usage_message = "print_info, print_debug, print_error, and print_warning have the options end, append, and restart."
    usage_message += "\n\tend sends the string to the end option on print."
    usage_message += "\n\tflush sends the bool value to the flush option on print. Defaults to True"
    usage_message += "\n\tappend=True assumes previously called with end='' and skips printing the title error_number,"
    usage_message += ", info, or debug."
    usage_message += "\n\trestart=True assumes previously called with end='', and prints a newline before printing"
    usage_message += " title."
    print(usage_message)

    print_info("Start a message...", end='')
    print_info("End a message.", append=True)
    print_info("Start a message", end='')
    print_warning("Something happened.", restart=True)

    print("printTimestamp: prints a timestamp, by default sends end='' to print.")
    print("\tHas parameter flush, which sets the flush option, defaults to true, This is true for all the time")
    print("\trelated functions.")
    print_time_stamp(end=" : ")
    print("Message")
    print("print_date_stamp: prints a date stamp, by default sends end='' to print.")
    print_date_stamp(end=" : ")
    print("Message")
    print("print_date_time_stamp: prints a date / time stamp, by default send end='' to print.")
    print_date_time_stamp(end=": ")
    print("Message")
