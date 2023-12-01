#!/usr/bin/env python3
"""
File: main.py
"""
import time
from typing import Final, Optional, Callable, Any
import argparse
import os.path
import curses
from enum import IntEnum
import logging
import socket


from configFile import ConfigFile, ConfigFileError
import prettyPrint
from cursesFunctions import get_mouse, get_left_click
from prettyPrint import print_coloured, print_info, print_error, print_debug, print_warning
from terminal import Colours

from SignalCliApi.signalLinkThread import LinkThread
from SignalCliApi.signalCommon import LinkAccountCallbackStates
from SignalCliApi.signalAccount import Account
from SignalCliApi.signalCli import SignalCli
from SignalCliApi.signalExceptions import SignalError
from SignalCliApi.signalErrors import LinkError

import common
from common import Focus
from cliExceptions import Quit
from themes import load_theme, init_colours
from mainWindow import MainWindow
from contactsWindow import ContactsWindow
from messagesWindow import MessagesWindow
from typingWindow import TypingWindow
from linkWindow import LinkWindow, LinkMessages
from menuBar import MenuBar
from window import Window
from quitWindow import QuitWindow
from qrcodeWindow import QRCodeWindow
from versionWindow import VersionWindow
import runCallback
import typeError
from typeError import __type_error__

runCallback.set_suppress_error(True)  # Supress errors calling callbacks.
typeError.set_use_syslog(False)  # Dont' log to syslog.
typeError.set_use_logging(True)  # Use Logging.

#########################################
# Constants:
#########################################
_WORKING_DIR_NAME: Final[str] = '.cliSignal'
"""Name of the working directory under $HOME."""
_CONFIG_NAME: Final[str] = 'cliSignal'
"""Name to give our config file configuration."""
_CONFIG_FILE_NAME: Final[str] = 'cliSignal.config'
"""Name of the cliSignal config file."""
_SIGNAL_CONFIG_DIR_NAME: Final[str] = 'signal-cli'
"""Name to give the signal-cli config directory. (where signal-cli stores it's files)."""
_SIGNAL_LOG_FILE_NAME: Final[str] = 'signal-cli.log'
"""Name of the signal-cli log file."""
_CLI_SIGNAL_LOG_FILE_NAME: Final[str] = 'cliSignal.log'
"""Name of the cliSignal log file."""
_WORKING_DIR: Final[str] = os.path.join(os.environ.get("HOME"), _WORKING_DIR_NAME)
"""The full path to the working directory."""
_SIGNAL_LOG_PATH: Final[str] = os.path.join(_WORKING_DIR, _SIGNAL_LOG_FILE_NAME)
"""The full path to the log file."""
_SIGNAL_CONFIG_DIR: Final[str] = os.path.join(_WORKING_DIR, _SIGNAL_CONFIG_DIR_NAME)
"""The full path to the default signal-cli config directory."""
_CLI_SIGNAL_CONFIG_FILE_PATH: Final[str] = os.path.join(_WORKING_DIR, _CONFIG_FILE_NAME)
"""The full path to the cliSignal config file."""
_CLI_SIGNAL_LOG_PATH: Final[str] = os.path.join(_WORKING_DIR, _CLI_SIGNAL_LOG_FILE_NAME)
"""The full path to the cliSignal log file."""
_HOST_NAME: Final[str] = socket.gethostname().split('.')[0]
"""The host name of the computer running cliSignal."""
_DEVICE_NAME: Final[str] = _HOST_NAME + '-cliSignal'


#########################################
# Enums:
#########################################

#########################################
# Vars:
#########################################
_CURRENT_FOCUS: Focus = Focus.CONTACTS
"""The currently focused window."""
_LAST_FOCUS: Focus = Focus.MENU_BAR
"""The last focused window."""
_FOCUS_WINDOWS: Optional[tuple[Window | MenuBar]] = None
"""The list of windows that switch focus with tab / shift tab."""
_MAIN_WINDOW: Optional[MainWindow] = None
"""The main window object."""
_EXIT_ERROR: Optional[curses.error] = None
"""If we're exiting due to a curses error, This is the error."""
_DEBUG: bool = False
"""True if we should produce debug output."""
_VERBOSE: bool = False
"""True if we should produce verbose output."""
_RESIZING: bool = False
"""True if we are currently resizing the window."""
_LOGGER: Optional[logging.Logger] = None
"""The logger for this module."""
_IS_CURSES_STARTED: bool = False
"""Is curses started?"""
_MOUSE_RESET_MASK: Optional[int] = None
"""The reset mouse mask."""
_SIGNAL_LINK_THREAD: Optional[LinkThread] = None
"""The signal link thread."""
_RECEIVE_STARTED: bool = False
"""Has receive started?"""

#########################################
# My menu callbacks:
#########################################
def file_menu_settings_cb(status: str, window: curses.window, *args: tuple[Any]) -> None:
    """
    File menu settings callback.
    :return: None
    """
    return


def file_menu_quit_cb(status: str, std_screen: curses.window) -> None:
    """
    File menu quit callback.
    :return: None
    """
    global _MAIN_WINDOW
    if not common.SETTINGS['quitConfirm']:
        raise Quit()
    _MAIN_WINDOW.hide_sub_windows()
    _MAIN_WINDOW.quit_window.is_visible = True
    set_current_focus(Focus.QUIT)
    return


def accounts_menu_switch_cb(status: str, window: curses.window, *args: tuple[Any]) -> None:
    """
    Accounts menu, switch callback.
    :return: None
    """
    return


def accounts_menu_link_cb(status: str,
                          std_screen: curses.window,
                          signal_cli: SignalCli
                          ) -> None:
    """
    Accounts menu, link callback.
    :param status: str: The call back status.
    :param std_screen: curses.window: The std screen
    :param signal_cli: SignalCli: The signal cli object.
    :return: None
    """
    # Set vars:
    global _CURRENT_FOCUS, _FOCUS_WINDOWS, _MAIN_WINDOW, _DEVICE_NAME, _LOGGER, _LAST_FOCUS, _SIGNAL_LINK_THREAD
    link_window: LinkWindow = _MAIN_WINDOW.link_window
    qr_window: QRCodeWindow = _MAIN_WINDOW.qr_window

    # Set the generating message, and hide the button:
    link_window.current_message = LinkMessages.GENERATE
    link_window.show_button = False

    # Set the window as visible, and set the focus:
    link_window.is_visible = True
    set_current_focus(Focus.LINK)
    # Redraw:
    _MAIN_WINDOW.redraw()
    # Start the link thread.
    signal_cli.start_link_thread(
        callback=(signal_link_cb, [signal_cli]),
        gen_text_qr=True,
        png_qr_file_path=None,
        device_name=_DEVICE_NAME,
        wait_time=0.1
    )
    # _SIGNAL_LINK_THREAD = signal_cli.generate_link_thread(callback, True, None, _DEVICE_NAME)
    # _SIGNAL_LINK_THREAD.start()
    return


def accounts_menu_register_cb(status: str, window: curses.window, *args: tuple[Any]) -> None:
    """
    Accounts menu, register callback.
    :return: None
    """
    return


def help_menu_shortcuts_cb(status: str, window: curses.window, *args: tuple[Any]) -> None:
    """
    The help menu, Keyboard shortcuts callback.
    :return: None
    """
    return


def help_menu_about_cb(status: str, window: curses.window, *args: tuple[Any]) -> None:
    """
    The help menu, about callback.
    :return: None
    """
    return


def help_menu_version_cb(status: str, std_screen: curses.window, *args: tuple[Any, ...]) -> None:
    """
    The help menu, version callback.
    :return: None
    """
    global _MAIN_WINDOW
    set_current_focus(Focus.VERSION)
    _MAIN_WINDOW.ver_window.is_visible = True
    return


#########################################
# Button callbacks:
#########################################


#########################################
# Signal callbacks:
#########################################
def signal_start_up_cb(state: str) -> None:
    """
    Signal start up callback.
    :param state: str, the current state of the startup process.
    :return: None
    """
    global _VERBOSE
    if _VERBOSE:
        print_coloured("SIGNAL:", fg_colour=Colours.FG.blue, bold=True, end='')
        print(state)
    return


def signal_link_cb(state: str,
                   data: Optional[tuple[Optional[str], Optional[str]] | str | Account],
                   signal_cli: SignalCli
                   ) -> bool:
    """
    Link account signal callback.
    :param state: str: The current state.
    :param data: Optional[tuple[Optional[str], Optional[str]] | str | Account]
    :param signal_cli: SignalCli: The signal_cli object.
    :return: bool: If return True, cancel the link process.
    """
    global _SIGNAL_LINK_THREAD, _MAIN_WINDOW
    logger: logging.Logger = logging.getLogger(__name__ + '.' + signal_link_cb.__name__)
    if state == LinkAccountCallbackStates.LINK_WAITING.value:
        return False
    logger.debug("Called with state: %s" % state)
    link_window: LinkWindow = _MAIN_WINDOW.link_window
    qr_window: QRCodeWindow = _MAIN_WINDOW.qr_window
    if state == LinkAccountCallbackStates.GENERATE_QR_STOP.value:
        link_window.is_visible = False
        qr_window.qrcode = data[0].splitlines(keepends=False)
        qr_window.is_visible = True
        set_current_focus(Focus.QR_CODE)
        _MAIN_WINDOW.redraw()
        return False
    elif state == LinkAccountCallbackStates.LINK_SUCCESS.value:
        link_window.current_message = LinkMessages.SUCCESS
    elif state == LinkAccountCallbackStates.LINK_EXISTS_ERROR.value:
        link_window.current_message = LinkMessages.EXISTS
    elif state == LinkAccountCallbackStates.LINK_UNKNOWN_ERROR.value:
        link_window.current_message = LinkMessages.UNKNOWN
    elif state == LinkAccountCallbackStates.LINK_TIMEOUT_ERROR.value:
        link_window.current_message = LinkMessages.TIMEOUT
    else:
        return False
    qr_window.is_visible = False
    link_window.show_button = True
    link_window.is_visible = True
    set_current_focus(Focus.LINK)
    _MAIN_WINDOW.redraw()
    signal_cli.stop_link_thread()
    return False


def signal_received_message_cb():
    return


def signal_receipt_message_cb():
    return


def signal_sync_message_cb():
    return


def signal_typing_message_cb():
    return


def signal_story_message_cb():
    return


def signal_payment_message_cb():
    return


def signal_reaction_message_cb():
    return


def signal_call_message_cb():
    return


#########################################
# Functions:
#########################################

def out_info(message: str, force=False) -> None:
    """
    Output an info message to both the log file if logging started, and stdout if curses not started.
    :param message: The message to output
    :param force: Override _VERBOSE
    :return: None
    """
    global _IS_CURSES_STARTED, _LOGGER, _VERBOSE
    if _VERBOSE or force:
        if not _IS_CURSES_STARTED:
            print_info(message, force=True)
    if _LOGGER is not None:
        _LOGGER.info(message)
    return


def out_error(message) -> None:
    """
    Output an error message to both the log file if logging started and stdout if curses not started.
    :param message: The message to output.
    :return: None
    """
    global _IS_CURSES_STARTED, _LOGGER
    if not _IS_CURSES_STARTED:
        print_error(message)
    if _LOGGER is not None:
        _LOGGER.error(message)
    return


def out_debug(message) -> None:
    """
    Output a debug message to both the log file if logging started, and stdout if curses not started.
    :param message: The message to output.
    :return: None
    """
    global _IS_CURSES_STARTED, _LOGGER, _DEBUG
    if _DEBUG:
        if not _IS_CURSES_STARTED:
            print_debug(message)
        if _LOGGER is not None:
            _LOGGER.debug(message)
    return


def out_warning(message) -> None:
    """
    Output a warning message to both the log file if logging started and stdout if curses is not started.
    :param message: The message to output.
    :return: None
    """
    global _IS_CURSES_STARTED, _LOGGER
    if not _IS_CURSES_STARTED:
        print_warning(message)
    if _LOGGER is not None:
        _LOGGER.warning(message)
    return


def __do_resize__() -> None:
    """
    Do the resize of the windows:
    :return: None
    """
    global _RESIZING, _MAIN_WINDOW
    _RESIZING = True
    _MAIN_WINDOW.resize()
    # _MAIN_WINDOW.redraw()
    _RESIZING = False
    return


def __set_hover_focus__(mouse_pos: tuple[int, int]) -> None:
    """
    Set the focus based on mouse position.
    :param mouse_pos: tuple[int, int]: The mouse position: (ROW, COL).
    :return: None
    """
    global _FOCUS_WINDOWS, _CURRENT_FOCUS, _MAIN_WINDOW
    # Do not switch focus if we're focusing on the status bar:
    if _MAIN_WINDOW.status_bar.is_mouse_over(mouse_pos):
        return

    # Check that a menu is active, and if not, don't switch focus.
    if _MAIN_WINDOW.menu_bar.is_menu_activated:
        return

    # Check if the mouse is over one of the sub windows:
    if _MAIN_WINDOW.is_sub_window_visible:
        window = _MAIN_WINDOW.get_visible_sub_window()
        if window.is_mouse_over(mouse_pos):
            set_current_focus(window.focus_id)
        else:
            set_current_focus(Focus.MAIN)
        return

    # Check if the mouse is over the menu bar:
    if _MAIN_WINDOW.menu_bar.is_mouse_over(mouse_pos):
        set_current_focus(Focus.MENU_BAR)

    # Check if the mouse is over one of the primary windows:
    for window in _MAIN_WINDOW.primary_windows:
        if window.is_mouse_over(mouse_pos):
            set_current_focus(window.focus_id)
    return


def __parse_mouse__() -> Optional[bool]:
    """
    Parse the mouse actions.
    :return: Optional[bool]: Return None: Char wasn't handled, processing should continue; Return True: char was
        handled, and processing shouldn't continue; Return False: char wasn't handled, processing shouldn't continue.
    """
    global _CURRENT_FOCUS, _FOCUS_WINDOWS, _MAIN_WINDOW
    # Get the mouse position and button state:
    mouse_pos, button_state = get_mouse()
    # Update the status bar:
    _MAIN_WINDOW.status_bar.mouse_pos = mouse_pos
    _MAIN_WINDOW.status_bar.mouse_button_state = button_state

    # Pass the mouse to the currently visible sub-window:
    return_value: Optional[bool] = None
    if _MAIN_WINDOW.is_sub_window_visible:
        window = _MAIN_WINDOW.get_visible_sub_window()
        return_value = window.process_mouse(mouse_pos, button_state)
        if return_value is not None:
            if return_value is False:
                window.is_visible = False
            return return_value

    # Pass the mouse to the menu bar:
    if _MAIN_WINDOW.menu_bar.is_mouse_over(mouse_pos):
        return_value = _MAIN_WINDOW.menu_bar.process_mouse(mouse_pos, button_state)
        if return_value is not None:
            return return_value

    # Pass the mouse to a main window if the mouse is over it:
    for window in _MAIN_WINDOW.primary_windows:
        if window.is_mouse_over(mouse_pos):
            return_value = window.process_mouse(mouse_pos, button_state)
            if return_value is not None:
                return return_value

    # Mouse move focus:
    if common.SETTINGS['mouseMoveFocus']:
        __set_hover_focus__(mouse_pos)
    return False


def set_current_focus(value: Focus) -> None:
    """
    Set the _CURRENT_FOCUS variable.
    :param value: Focus: The focus enum value for the window.
    :return: None
    """
    global _CURRENT_FOCUS, _LAST_FOCUS, _FOCUS_WINDOWS
    if not isinstance(value, Focus):
        __type_error__("value", "Focus", value)
    if value != _CURRENT_FOCUS:
        _FOCUS_WINDOWS[_CURRENT_FOCUS].is_focused = False
        _LAST_FOCUS = _CURRENT_FOCUS
        _CURRENT_FOCUS = value
        _FOCUS_WINDOWS[_CURRENT_FOCUS].is_focused = True
    return


def inc_focus() -> None:
    """
    Increment the window focus.
    :return: None
    """
    global _CURRENT_FOCUS, _FOCUS_WINDOWS, _MAIN_WINDOW
    # Increment focus:
    next_focus: int = _CURRENT_FOCUS + 1
    # Wrap focus if needed:
    if next_focus > Focus.MENU_BAR:
        next_focus = Focus.CONTACTS
    # Set new focus
    set_current_focus(Focus(next_focus))
    return


def dec_focus() -> None:
    """
    Decrement the focus.
    :return: None
    """
    global _CURRENT_FOCUS, _FOCUS_WINDOWS, _MAIN_WINDOW
    # Decrement focus:
    next_focus: int = _CURRENT_FOCUS - 1
    # Wrap focus if necessary:
    if next_focus < Focus.CONTACTS:
        next_focus = Focus.MENU_BAR
    # Set the new focus:
    set_current_focus(Focus(next_focus))
    return


def __preprocess_key__(char_code: int) -> Optional[bool]:
    """
    Pre-process a key, catches resize.
    :param char_code: int: The char code received.
    :return: Optional[bool]: True if char handled and processing shouldn't continue. False if not handled and processing
        shouldn't continue, return None key wasn't handled and processing should continue.
    """
    if char_code == curses.KEY_RESIZE:
        __do_resize__()
        return True
    elif char_code == curses.KEY_MOUSE:
        return __parse_mouse__()
    return None


def __stop_mouse__() -> None:
    """
    Stop the mouse support:
    :return: None
    """
    # Pull in reset mouse mask:
    global _MOUSE_RESET_MASK
    out_info("Stopping mouse.")
    # If it's not None, reset the mouse mask.
    if _MOUSE_RESET_MASK is not None:
        out_debug("Resetting mouse mask.")
        curses.mousemask(_MOUSE_RESET_MASK)
    # Tell the terminal to stop processing mouse movements:
    out_debug("Sending terminal stop report characters.")
    print('\033[?1003l', end='', flush=True)
    return


def __start_mouse__() -> bool:
    """
    Start the mouse.
    :return: bool: True mouse was started, False it was not.
    """
    # Pull in reset mouse mask:
    global _MOUSE_RESET_MASK
    out_info("Starting mouse support.")
    # Set the curses mouse mask:
    out_debug('Setting mouse mask...')
    response = curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    if response == 0:  # Complete failure returns 0, no mask to reset to.
        _MOUSE_RESET_MASK = None
        out_warning("Error starting mouse, not using mouse.")
        return False
    else:  # Response is a tuple (avail_mask, old_mask)
        out_debug("Setting mouse mask success.")
        _MOUSE_RESET_MASK = response[1]
    # Tell the terminal to report mouse movement.
    out_debug("Sending terminal control characters...")
    print('\033[?1003h', end='', flush=True)
    return True


#########################################
# Main:
#########################################
def main(std_screen: curses.window, signal_cli: SignalCli) -> None:
    """
    Main.
    :param std_screen: curses.window: The std_screen main window.
    :param signal_cli: The SignalCli instance.
    :return: None
    """
    global _DEBUG, _VERBOSE, _CURRENT_FOCUS, _LAST_FOCUS, _FOCUS_WINDOWS, _MAIN_WINDOW, _RESIZING, _EXIT_ERROR

    # Set up extended key codes; And turn off the cursor:
    std_screen.keypad(True)
    std_screen.nodelay(True)
    curses.curs_set(False)

    # Set up colour pairs according to theme:
    if not curses.has_extended_color_support():
        message: str = "Terminal must have 256 colour support."
        out_error(message)
        _EXIT_ERROR = RuntimeError(message)
        return
    theme: dict[str, dict[str, int | bool | str]] = load_theme()
    init_colours(theme)

    # Set up the mouse:
    if common.SETTINGS['useMouse']:
        if not __start_mouse__():
            common.SETTINGS['useMouse'] = False

    # Create the callback dict:
    callbacks: dict[str, dict[str, tuple[Optional[Callable], Optional[list[Any]]]]] = {
        'file': {
            'settings': (file_menu_settings_cb, None),
            'quit': (file_menu_quit_cb, None),
        },
        'accounts': {
            'switch': (accounts_menu_switch_cb, None),
            'link': (accounts_menu_link_cb, [signal_cli]),
            'register': (accounts_menu_register_cb, None),
        },
        'help': {
            'shortcuts': (help_menu_shortcuts_cb, None),
            'about': (help_menu_about_cb, None),
            'version': (help_menu_version_cb, None),
        },
    }

    # Create the main windows:
    main_window = MainWindow(
        std_screen=std_screen,
        theme=theme,
        callbacks=callbacks,
    )

    # Store references to the windows for focus, and redrawing:
    _MAIN_WINDOW = main_window
    _FOCUS_WINDOWS = (
        main_window, main_window.contacts_window, main_window.messages_window, main_window.typing_window,
        main_window.menu_bar, main_window.status_bar, main_window.quit_window, main_window.link_window,
        main_window.qr_window, main_window.ver_window
    )
    # Call set_current_focus for the first time:
    set_current_focus(Focus.CONTACTS)
    main_window.contacts_window.is_focused = True
    # Set visible status items:
    if _DEBUG:
        main_window.status_bar.is_char_code_visible = True
        if common.SETTINGS['useMouse']:
            main_window.status_bar.is_mouse_visible = True
    # main_window.redraw()
    try:
        # Main loop:
        while True:
            try:
                # Input loop:
                while True:
                    # Draw the main window:
                    main_window.redraw()
                    # Get the character and update the status bar if required.
                    char_code: int = std_screen.getch()
                    if _DEBUG:
                        main_window.status_bar.char_code = char_code
                    # If no char, continue:
                    if char_code == -1:
                        continue
                    # Pre-process char code, catches mouse, and resize events:
                    char_handled = __preprocess_key__(char_code)
                    if char_handled is not None:
                        continue

                    # Check if a sub-window is visible, and if so, hand the key there:
                    #   If it returns False, hide the window.
                    if main_window.is_sub_window_visible:
                        sub_window: Window = main_window.get_visible_sub_window()
                        char_handled = sub_window.process_key(char_code)
                        if char_handled is False:
                            sub_window.is_visible = False
                            set_current_focus(Focus.MENU_BAR)
                            continue
                        elif char_handled is True:
                            continue

                    # Secondly, check the menu bar for the key press:
                    char_handled = main_window.menu_bar.process_key(char_code)
                    if char_handled is not None:
                        set_current_focus(Focus.MENU_BAR)
                        continue

                    # Finally, send the key to the focused primary window:
                    char_handled = _FOCUS_WINDOWS[_CURRENT_FOCUS].process_key(char_code)
                    if char_handled is not None:
                        continue

                    # Switch focus on Tab and Shift Tab.
                    if char_code == common.KEY_TAB:
                        inc_focus()
                    elif char_code == common.KEY_SHIFT_TAB:
                        dec_focus()
                    # main_window.redraw()

            except KeyboardInterrupt:
                if not common.SETTINGS['quitConfirm']:
                    raise Quit()
                else:
                    file_menu_quit_cb("", std_screen)
                    continue

            except (curses.error, SignalError) as e:
                _EXIT_ERROR = e
                raise Quit

    except Quit:
        pass
    # Fix mouse mask:
    __stop_mouse__()
    return


#########################################
# Start:
#########################################
if __name__ == '__main__':

    # Setup .cliSignal directory, and change to it:
    if not os.path.exists(_WORKING_DIR):
        try:
            os.mkdir(_WORKING_DIR, 0o700)
        except (OSError, PermissionError, FileNotFoundError):
            out_error("Failed to create '%s' directory." % _WORKING_DIR)
            exit(2)

    # Check working directory permissions, and if they are wrong, abort.
    if oct(os.stat(_WORKING_DIR).st_mode)[-3:] != oct(0o700)[-3:]:
        out_error("Working directory: '%s', permissions are not 700." % _WORKING_DIR)
        exit(3)
    common.SETTINGS['workingDir'] = _WORKING_DIR
    # Change to working directory:
    os.chdir(_WORKING_DIR)

    # Setup command line arguments:
    parser = argparse.ArgumentParser(description="Command line Signal client.",
                                     epilog="Written by Peter Nearing."
                                     )
    # DEBUG or verbose:
    debug_or_verbose = parser.add_mutually_exclusive_group()
    debug_or_verbose.add_argument('--debug',
                                  help="Debugging mode, be ware of the odd exception. Implies --verbose.",
                                  action='store_true',
                                  default=False
                                  )
    debug_or_verbose.add_argument('--verbose',
                                  help="Produce verbose output.",
                                  action='store_true',
                                  default=False
                                  )
    # Config options:
    parser.add_argument('--config',
                        help="The full path to the config file, default is $HOME/.cliSignal/cliSignal.config",
                        type=str
                        )
    parser.add_argument('--store',
                        help="Save the command line options to the config.",
                        action='store_true',
                        default=False
                        )
    # Signal options:
    parser.add_argument('--signalConfigDir',
                        help="The full path to the signal config directory.",
                        type=str
                        )
    parser.add_argument('--signalSocketPath',
                        help="The full path to the socket file. If you are starting signal (the default action, "
                             "this must be a directory. Otherwise if using --noStartSignal, this must be an existing "
                             "socket file.",
                        type=str
                        )
    parser.add_argument('--signalExecPath',
                        help="The full path to the signal-cli executable.",
                        type=str
                        )
    parser.add_argument('--noStartSignal',
                        help="Start the signal daemon.",
                        action='store_true',
                        default=False
                        )
    # Colour theme options:
    parser.add_argument('--theme',
                        help='The theme to use, either "light", "dark", or "custom".',
                        type=str
                        )
    parser.add_argument('--themePath',
                        help="The path to the custom theme json file, required if --theme=custom",
                        type=str
                        )
    # Settings:
    # Use mouse:
    use_mouse = parser.add_mutually_exclusive_group()
    use_mouse.add_argument('--useMouse',
                           help="Try and use the mouse, NOTE: Sometimes this leaves the terminal in an unstable state.",
                           action='store_true',
                           default=None
                           )
    use_mouse.add_argument('--noUseMouse',
                           help="Turn the mouse off.",
                           action='store_false',
                           dest='useMouse'
                           )
    # Confirm on quit:
    quit_confirm = parser.add_mutually_exclusive_group()
    quit_confirm.add_argument('--confirmQuit',
                              help="Confirm before exit.",
                              action='store_true',
                              default=None
                              )
    quit_confirm.add_argument('--noConfirmQuit',
                              help="Don't confirm before exit.",
                              action='store_false',
                              dest='confirmQuit',
                              )
    # Mouse movement focus:
    mouse_focus = parser.add_mutually_exclusive_group()
    mouse_focus.add_argument('--mouseFocus',
                             help="Focus window on mouse movement.",
                             action='store_true',
                             default=None,
                             )
    mouse_focus.add_argument('--noMouseFocus',
                             help="Don't focus on mouse movement.",
                             action='store_false',
                             dest='mouseFocus'
                             )

    # Account argument:
    parser.add_argument('--account',
                        help="The account to use.",
                        type=str
                        )

    # Parse args:
    _args: argparse.Namespace = parser.parse_args()

    # Parse --debug and --verbose options:
    log_level = logging.WARNING
    if _args.debug:
        _DEBUG = True
        _VERBOSE = True
        prettyPrint.DEBUG = True
        prettyPrint.VERBOSE = True
        log_level = logging.DEBUG
        runCallback.set_suppress_error(False)
    elif _args.verbose:
        _VERBOSE = True
        prettyPrint.VERBOSE = True
        log_level = logging.INFO

    # Set logging path:
    common.SETTINGS['logPath'] = _CLI_SIGNAL_LOG_PATH
    logging.basicConfig(filename=_CLI_SIGNAL_LOG_PATH, encoding='utf-8', level=log_level,
                        format='%(levelname)s : [%(asctime)s] : (%(name)s) : %(message)s')
    _LOGGER = logging.getLogger(__name__)
    _LOGGER.debug("Logging started.")

    # Parse --config option:
    cli_signal_config_path: str = _CLI_SIGNAL_CONFIG_FILE_PATH
    if _args.config is not None:
        cli_signal_config_path: str = _args.config

    # load config:
    try:
        config_file: ConfigFile = ConfigFile(config_name=_CONFIG_NAME,
                                             file_path=cli_signal_config_path,
                                             set_permissions=0o600,
                                             enforce_permissions=True,
                                             create_default=True,
                                             do_load=True
                                             )
    except ConfigFileError as _e:
        if _e.error_number == 21:
            out_error("Permissions of config file must be 600.")
        else:
            out_error("ConfigFileError: %s" % _e.error_message)
        exit(4)

    # Validate / act on arguments:
    # Signal arguments:
    # --noStartSignal:
    if _args.noStartSignal:
        common.SETTINGS['startSignal'] = False

    # --signalConfigDir:
    common.SETTINGS['signalConfigDir'] = _SIGNAL_CONFIG_DIR
    if _args.signalConfigDir is not None:
        common.SETTINGS['signalConfigDir'] = _args.signalConfigPath

    # --signalSocketPath:
    if _args.signalSocketPath is not None:
        common.SETTINGS['signalSocketPath'] = _args.signalSocketFile
    if common.SETTINGS['signalSocketPath'] is not None:
        if (not os.path.exists(common.SETTINGS['signalSocketPath']) or
                not os.path.isfile(common.SETTINGS['signalSocketPath'])):
            out_error("--signalSocketPath must point to an existing socket file.")
            exit(5)

    # --signalExecPath:
    if _args.signalExecPath is not None:
        common.SETTINGS['signalExecPath'] = _args.signalExecPath
    if common.SETTINGS['signalExecPath'] is not None and (not os.path.exists(common.SETTINGS['signalExecPath']) or
                                                          not os.path.isfile(common.SETTINGS['signalExecPath'])):
        out_error("--signalExecPath must point to an existing signal-cli executable file.")
        exit(6)

    # Verify arguments; If --noStartSignal, --signalSocketPath must be defined:
    if _args.noStartSignal and common.SETTINGS['signalSocketPath'] is None:
        out_error("--signalSocketPath must point to an existing file if using --noStartSignal.")
        exit(7)

    # Theme arguments:
    # --theme:
    if _args.theme is not None:
        if _args.theme not in ('light', 'dark', 'custom'):
            out_error("--theme must be either: 'light', 'dark', or 'custom'.")
            exit(8)
        common.SETTINGS['theme'] = _args.theme
    # Verify theme is correct:
    if common.SETTINGS['theme'] not in ('light', 'dark', 'custom'):
        out_error("--theme must be one of: 'light', 'dark', or 'custom'")
        exit(9)
    if common.SETTINGS['theme'] == 'custom':
        # If there is no theme path, throw an error.
        if _args.themePath is None and common.SETTINGS['themePath'] is None:
            out_error("If --theme is 'custom', either --themePath must be supplied, or 'themePath' must be "
                      "defined in your configuration file.")
            exit(10)
        # Override settings theme path with the args theme path:
        elif _args.themePath is not None:
            common.SETTINGS['themePath'] = _args.themePath
        # Check that the theme path exists:
        if not os.path.exists(common.SETTINGS['themePath']) or not os.path.isfile(common.SETTINGS['themePath']):
            out_error("'themePath' must point to an existing file.")
            exit(11)

    # Settings arguments:
    # cliSignal logging:

    # Use mouse:
    if _args.useMouse is not None:
        common.SETTINGS['useMouse'] = _args.useMouse
    out_debug("useMouse = %s" % str(common.SETTINGS['useMouse']))

    if _args.confirmQuit is not None:
        common.SETTINGS['quitConfirm'] = _args.confirmQuit
    out_debug("quitConfirm = %s" % str(common.SETTINGS['quitConfirm']))

    if _args.mouseFocus is not None:
        common.SETTINGS['mouseMoveFocus'] = _args.mouseFocus
    out_debug("mouseMoveFocus = %s" % str(common.SETTINGS['mouseMoveFocus']))

    # Parse --account:
    if _args.account is not None:
        common.SETTINGS['defaultAccount'] = _args.account

    # Parse: --store
    if _args.store:
        try:
            config_file.save()
        except ConfigFileError as e:
            out_error(e.error_message)
            exit(12)

    # Make signal-cli config dir if required:
    if not os.path.exists(common.SETTINGS['signalConfigDir']):
        try:
            os.mkdir(_SIGNAL_CONFIG_DIR, 0o700)
        except (OSError, FileNotFoundError, PermissionError):
            out_error("Failed to create '%s' directory." % common.SETTINGS['signalConfigDir'])
            exit(13)

    # Start signal:
    out_info("Starting signal-cli...", force=True)
    _signal_cli: SignalCli = SignalCli(
        signal_config_path=common.SETTINGS['signalConfigDir'],
        signal_exec_path=common.SETTINGS['signalExecPath'],
        log_file_path=_SIGNAL_LOG_PATH,
        server_address=common.SETTINGS['signalSocketPath'],
        start_signal=common.SETTINGS['startSignal'],
        callback=(signal_start_up_cb, None),
    )

    # Load the account:
    if common.SETTINGS['defaultAccount'] is not None:
        try:
            common.CURRENT_ACCOUNT = _signal_cli.accounts.get_by_number(common.SETTINGS['defaultAccount'])
        except ValueError as e:
            out_error("Invalid account, number not in right format.")
            _signal_cli.stop_signal()
            exit(14)
        if common.CURRENT_ACCOUNT is None:
            out_error("Account: %s not registered." % common.SETTINGS['defaultAccount'])
            _signal_cli.stop_signal()
            exit(15)
    if len(_signal_cli.accounts) > 0:
        common.CURRENT_ACCOUNT = _signal_cli.accounts[0]

    # Run main:
    _IS_CURSES_STARTED = True
    curses.wrapper(main, _signal_cli)
    _IS_CURSES_STARTED = False

    # Stop signal
    out_info("Stopping signal.", force=True)
    if _signal_cli.link_thread is not None:
        _signal_cli.stop_link_thread()
    _signal_cli.stop_signal()

    if _EXIT_ERROR is not None:
        if _RESIZING:
            out_error("Window size too small. Fatal.")
        out_error("EXITED DUE TO ERROR: %s" % str(_EXIT_ERROR.args))
        if isinstance(_EXIT_ERROR, SignalError):
            out_error("Signal error code: %i" % _EXIT_ERROR.code)
            out_error("Signal error message: %s" % _EXIT_ERROR.message)
            if _DEBUG:
                raise _EXIT_ERROR

        if _DEBUG:
            print(_EXIT_ERROR.__traceback__)
            raise _EXIT_ERROR
        exit(14)
    exit(0)
