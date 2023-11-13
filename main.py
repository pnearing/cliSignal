#!/usr/bin/env python3
import time
from typing import Final, Optional, Callable, Any
import argparse
import os.path
import curses
from enum import IntEnum
from SignalCliApi.signalCli import SignalCli
from configFile import ConfigFile, ConfigFileError
import common
from themes import load_theme, init_colours
from mainWindow import MainWindow
from contactsWindow import ContactsWindow
from messagesWindow import MessagesWindow
from typingWindow import TypingWindow
from linkWindow import LinkWindow, LinkMessageSelections
from menuBar import MenuBar
from quitWindow import QuitWindow
from qrcodeWindow import QRCodeWindow
import prettyPrint
from prettyPrint import print_coloured, print_info, print_error, print_debug
from terminal import Colours
import logging


#########################################
# Enums:
#########################################
class Focus(IntEnum):
    """
    Focused windows / elements. Indexes focus_windows list.
    """
    MAIN = 0
    CONTACTS = 1
    MESSAGES = 2
    TYPING = 3
    MENU_BAR = 4


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

#########################################
# Vars:
#########################################
# _CURRENT_FOCUS: Focus = Focus.MAIN
_CURRENT_FOCUS: Focus = Focus.MENU_BAR
"""The currently focused window."""
_FOCUS_WINDOWS: tuple[MainWindow, ContactsWindow, MessagesWindow, TypingWindow, MenuBar] = ()
"""The list of windows that switch focus with tab / shift tab."""
_MAIN_WINDOW: MainWindow = None
"""The main window object."""
_EXIT_ERROR: Optional[curses.error] = None
"""If we're exiting due to a curses error, This is the error."""
_DEBUG: bool = False
"""True if we should produce debug output."""
_VERBOSE: bool = False
"""True if we should produce verbose output."""
_RESIZING: bool = False
"""True if we are currently resizing the window."""
_LOGGER: logging.Logger = None
"""The logger for this module."""
_CURSES_STARTED: bool = False


#########################################
# My menu callbacks:
#########################################
def main_menu_file_cb(status: str, window: curses.window, *args: list[Any]) -> None:
    """
    Main menu file callback.
    :param status: str: The current status, either 'activated' or 'deactivated'.
    :param window: curses.window: The std_screen object.
    :return: None
    """
    return


def main_menu_accounts_cb(status: str, window: curses.window, *args: tuple[Any]) -> None:
    """
    Main menu accounts callback.
    :return: None
    """
    return


def main_menu_help_cb(status: str, window: curses.window, *args: tuple[Any]) -> None:
    """
    Main menu help callback.
    :return:
    """
    return


def file_menu_settings_cb(status: str, window: curses.window, *args: tuple[Any]) -> None:
    """
    File menu settings callback.
    :return: None
    """
    return


def file_menu_quit_cb(status: str, window: curses.window, *args: tuple[Any]) -> None:
    """
    File menu quit callback.
    :return: None
    """
    raise KeyboardInterrupt


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
    global _CURRENT_FOCUS, _FOCUS_WINDOWS, _MAIN_WINDOW
    link_window: LinkWindow = _MAIN_WINDOW.link_window
    qr_window: QRCodeWindow = _MAIN_WINDOW.qr_window

    # Unfocus currently focused window:
    _FOCUS_WINDOWS[_CURRENT_FOCUS].is_focused = False
    # Focus, and make visible the link message window.
    link_window.is_focused = True
    link_window.is_visible = True
    _MAIN_WINDOW.redraw()
    # std_screen.refresh()

    link, qr_code, _ = signal_cli.start_link_account()
    # remove extra lines on qr-code:
    qr_list: list[str] = qr_code.splitlines(keepends=False)[1:-2]
    for i, line in enumerate(qr_list):
        qr_list[i] = line[3:-3]
    qr_window.qrcode = qr_list
    link_window.is_focused = False
    link_window.is_visible = False
    qr_window.is_focused = True
    qr_window.is_visible = True
    _MAIN_WINDOW.redraw()
    time.sleep(5)
    response = signal_cli.finish_link()
    if response[0]:  # Link successful.
        link_window.current_message = LinkMessageSelections.SUCCESS
    else:
        link_window.current_message = LinkMessageSelections.FAILURE
    qr_window.is_visible = False
    qr_window.is_focused = False
    link_window.is_focused = True
    link_window.is_visible = True
    _MAIN_WINDOW.redraw()
    while True:
        char_code: int = _MAIN_WINDOW.std_screen.getch()
        if char_code in common.KEYS_ENTER or char_code in (common.KEY_ESC, common.KEY_BACKSPACE):
            break
    _FOCUS_WINDOWS[_CURRENT_FOCUS].is_focused = True
    _MAIN_WINDOW.redraw()
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


def help_menu_version_cb(status: str, window: curses.window, *args: tuple[Any]) -> None:
    """
    The help menu, version callback.
    :return: None
    """
    return


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
    global _CURSES_STARTED, _LOGGER, _VERBOSE
    if _VERBOSE or force:
        if not _CURSES_STARTED:
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
    global _CURSES_STARTED, _LOGGER
    if not _CURSES_STARTED:
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
    global _CURSES_STARTED, _LOGGER, _DEBUG
    if _DEBUG:
        if not _CURSES_STARTED:
            print_debug(message)
        if _LOGGER is not None:
            _LOGGER.debug(message)
    return


def confirm_quit(main_window: MainWindow, quit_window: QuitWindow) -> bool:
    """
    Show an "are you sure message", and return users' input.
    :return: bool: True, the user quits; False, the user doesn't quit.
    """
    quit_window.is_visible = True
    quit_window.is_focused = True
    while True:
        quit_window.redraw()
        curses.doupdate()
        char_code: int = main_window.std_screen.getch()
        if char_code == curses.KEY_RESIZE:
            main_window.resize()
            main_window.redraw()
            continue
        response: Optional[bool] = quit_window.process_key(char_code)
        if isinstance(response, bool):
            quit_window.is_focused = False
            quit_window.is_visible = False
            return response


def do_resize(main_window: MainWindow) -> None:
    """
    Do the resize of the windows:
    :param main_window: MainWindow: The main window object.
    :return: None
    """
    global _RESIZING
    _RESIZING = True
    main_window.resize()
    main_window.redraw()
    _RESIZING = False
    return


def parse_mouse(mouse_pos: tuple[int, int], button_state: int) -> None:
    """
    Parse the mouse actions.
    :param mouse_pos: tuple[int, int]: The position of the mouse.
    :param button_state: int: The current button state.
    :return: None
    """
    global _CURRENT_FOCUS, _FOCUS_WINDOWS
    # Set the window focus:
    _FOCUS_WINDOWS[_CURRENT_FOCUS].is_focused = False
    if _FOCUS_WINDOWS[Focus.CONTACTS].is_mouse_over(mouse_pos):
        _CURRENT_FOCUS = Focus.CONTACTS
    elif _FOCUS_WINDOWS[Focus.MESSAGES].is_mouse_over(mouse_pos):
        _CURRENT_FOCUS = Focus.MESSAGES
    elif _FOCUS_WINDOWS[Focus.TYPING].is_mouse_over(mouse_pos):
        _CURRENT_FOCUS = Focus.TYPING
    elif _FOCUS_WINDOWS[Focus.MENU_BAR].is_mouse_over(mouse_pos):
        _CURRENT_FOCUS = Focus.MENU_BAR
    _FOCUS_WINDOWS[_CURRENT_FOCUS].is_focused = True
    # TODO: Process button state.
    return


def inc_focus() -> None:
    """
    Increment the window focus.
    :return: None
    """
    global _CURRENT_FOCUS, _FOCUS_WINDOWS, _MAIN_WINDOW
    # Un-focus current focus, and increment focus:
    _FOCUS_WINDOWS[_CURRENT_FOCUS].is_focused = False
    _CURRENT_FOCUS += 1
    # Wrap focus if needed:
    if _CURRENT_FOCUS > Focus.MENU_BAR:
        _CURRENT_FOCUS = Focus.CONTACTS
    # Set the new focus and redraw:
    _FOCUS_WINDOWS[_CURRENT_FOCUS].is_focused = True
    _MAIN_WINDOW.redraw()
    return


def dec_focus() -> None:
    """
    Decrement the focus.
    :return: None
    """
    global _CURRENT_FOCUS, _FOCUS_WINDOWS, _MAIN_WINDOW
    # Un-focus current focus, and decrement focus:
    _FOCUS_WINDOWS[_CURRENT_FOCUS].is_focused = False
    _CURRENT_FOCUS -= 1
    # Wrap focus if necessary:
    if _CURRENT_FOCUS < Focus.CONTACTS:
        _CURRENT_FOCUS = Focus.MENU_BAR
    # Set the focus and redraw:
    _FOCUS_WINDOWS[_CURRENT_FOCUS].is_focused = True
    _MAIN_WINDOW.redraw()
    return


#########################################
# Main:
#########################################
def main(std_screen: curses.window, signal_cli: SignalCli) -> None:
    global _DEBUG, _VERBOSE, _CURRENT_FOCUS, _FOCUS_WINDOWS, _MAIN_WINDOW, _RESIZING, _EXIT_ERROR
    # Setup extended key codes, and turn off the cursor:
    std_screen.keypad(True)
    curses.curs_set(False)

    # Setup the mouse:
    reset_mouse_mask: Optional[int] = None
    if common.SETTINGS['useMouse']:
        out_info("Starting mouse support.")
        # Tell the terminal to report mouse movement.
        out_debug("Sending terminal control characters...")
        print('\033[?1003h', end='', flush=True)
        if _DEBUG:
            curses.beep()
        # Set the curses mouse mask:
        out_debug('Setting mouse mask...')
        response = curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
        if response == 0:  # Complete failure returns 0, no mask to reset to.
            out_debug("Setting mouse mask failed.")
            out_info("Error starting mouse, not using mouse.")
            common.SETTINGS['useMouse'] = False
        else:  # Response is a tuple (avail_mask, old_mask)
            out_debug("Setting mouse mask success.")
            reset_mouse_mask = response[1]

    # Setup colour pairs according to theme:
    if not curses.has_extended_color_support():
        message: str = "Terminal must have 256 colour support."
        out_error(message)
        _EXIT_ERROR = RuntimeError(message)
        return
    theme: dict[str, dict[str, int | bool | str]] = load_theme()
    init_colours(theme)

    # Create sub-windows:
    link_window: LinkWindow = LinkWindow(std_screen, theme)
    quit_window: QuitWindow = QuitWindow(std_screen, theme)
    qr_window: QRCodeWindow = QRCodeWindow(std_screen, theme)

    # Create the callback dict:
    callbacks: dict[str, dict[str, tuple[Optional[Callable], Optional[list[Any]]]]] = {
        'main': {
            'file': (main_menu_file_cb, None),
            'accounts': (main_menu_accounts_cb, None),
            'help': (main_menu_help_cb, None),
        },
        'file': {
            'settings': (file_menu_settings_cb, None),
            'quit': (file_menu_quit_cb, [quit_window]),
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
        quit_window=quit_window,
        link_window=link_window,
        qr_window=qr_window
    )

    # Store references to the windows for focus, and redrawing:
    _MAIN_WINDOW = main_window
    _FOCUS_WINDOWS = (
        main_window, main_window.contacts_window, main_window.messages_window, main_window.typing_window,
        main_window.menu_bar
    )

    # Set initial focus
    _FOCUS_WINDOWS[_CURRENT_FOCUS].is_focused = True

    # Set visible status items:
    if _DEBUG:
        main_window.status_bar.is_char_code_visible = True

    # Draw the window for the first time:
    main_window.redraw()

    # Main loop:
    while True:
        try:
            while True:
                char_code: int = std_screen.getch()
                main_window.status_bar.char_code = char_code

                # Pre-process char code:
                if char_code == curses.KEY_RESIZE:  # Resize the windows:
                    do_resize(main_window)
                    continue
                elif char_code == curses.KEY_MOUSE:  # Mouse move / button hit:
                    _, mouse_col, mouse_row, _, button_state = curses.getmouse()
                    mouse_pos: tuple[int, int] = (mouse_row, mouse_col)
                    if common.SETTINGS['useMouse']:
                        parse_mouse(mouse_pos, button_state)
                    continue

                # Hand the char code to the appropriate window for handling.
                char_handled: bool
                if _CURRENT_FOCUS == Focus.MENU_BAR:
                    char_handled = _FOCUS_WINDOWS[Focus.MENU_BAR].process_key(char_code)
                    if char_handled:
                        main_window.redraw()
                        curses.doupdate()
                        continue
                elif _CURRENT_FOCUS == Focus.CONTACTS:
                    char_handled = _FOCUS_WINDOWS[Focus.CONTACTS].process_key(char_code)
                    if char_handled:
                        main_window.redraw()
                        curses.doupdate()
                        continue
                elif _CURRENT_FOCUS == Focus.MESSAGES:
                    char_handled = _FOCUS_WINDOWS[Focus.MESSAGES].process_key(char_code)
                    if char_handled:
                        main_window.redraw()
                        curses.doupdate()
                        continue
                elif _CURRENT_FOCUS == Focus.TYPING:
                    char_handled = _FOCUS_WINDOWS[Focus.TYPING].process_key(char_code)
                    if char_handled:
                        main_window.redraw()
                        curses.doupdate()
                        continue

                # If the window didn't handle the character, we want to handle it:
                if char_code == common.KEY_TAB:  # Tab hit switch focus.
                    inc_focus()
                    continue
                elif char_code == common.KEY_SHIFT_TAB:  # Shift-Tab hit, switch focus backwards.
                    dec_focus()
                    continue
                elif char_code == curses.KEY_F1:
                    # Shift the focus to the menu bar:
                    _FOCUS_WINDOWS[_CURRENT_FOCUS].is_focused = False
                    _CURRENT_FOCUS = Focus.MENU_BAR
                    _FOCUS_WINDOWS[_CURRENT_FOCUS].is_focused = True
                    # Activate the file menu:
                    menu_bar = main_window.menu_bar
                    # If there is a menu currently active, deactivate it.
                    if menu_bar.is_menu_activated:
                        menu_bar.menu_bar_items[menu_bar.selection].deactivate()
                    # Set the selection to the file menu, set the active menu and activate the file menu.:
                    menu_bar.selection = common.MenuBarSelections.FILE
                    menu_bar._active_menu = menu_bar.menus[menu_bar.selection]
                    menu_bar.menu_bar_items[menu_bar.selection].activate()
                    # Redraw the window:
                    main_window.redraw()
                    continue
                elif char_code == curses.KEY_F2:
                    # Shift the focus to the menu bar:
                    _FOCUS_WINDOWS[_CURRENT_FOCUS].is_focused = False
                    _CURRENT_FOCUS = Focus.MENU_BAR
                    _FOCUS_WINDOWS[_CURRENT_FOCUS].is_focused = True
                    # Activate the accounts menu:
                    menu_bar = main_window.menu_bar
                    # If there is an active menu, deactivate it.
                    if menu_bar.is_menu_activated:
                        menu_bar.menu_bar_items[menu_bar.selection].deactivate()
                    # Set the selection to the accounts menu:
                    menu_bar.selection = common.MenuBarSelections.ACCOUNTS
                    menu_bar._active_menu = menu_bar.menus[menu_bar.selection]
                    menu_bar.menu_bar_items[menu_bar.selection].activate()
                    # Redraw the window:
                    main_window.redraw()
                    curses.doupdate()
                    continue
                elif char_code == curses.KEY_F3:
                    # Shift focus to menu bar:
                    _FOCUS_WINDOWS[_CURRENT_FOCUS].is_focused = False
                    _CURRENT_FOCUS = Focus.MENU_BAR
                    _FOCUS_WINDOWS[_CURRENT_FOCUS].is_focused = True
                    # Activate the help menu:
                    menu_bar = main_window.menu_bar
                    # If there is an active menu, deactivate it:
                    if menu_bar.is_menu_activated:
                        menu_bar.menu_bar_items[menu_bar.selection].deactivate()
                    menu_bar.selection = common.MenuBarSelections.HELP
                    menu_bar._active_menu = menu_bar.menus[menu_bar.selection]
                    menu_bar.menu_bar_items[menu_bar.selection].activate()
                    # Redraw the window:
                    main_window.redraw()
                    curses.doupdate()
                    continue

        except KeyboardInterrupt:
            # Do quit confirmation if setting allows:
            if common.SETTINGS['quitConfirm']:
                # Remove current focus:
                _FOCUS_WINDOWS[_CURRENT_FOCUS].is_focused = False
                main_window.redraw()
                # Run quit window:
                user_response: bool = confirm_quit(main_window, quit_window)
                if not user_response:  # False, user doesn't quit.
                    # Restore focus on the window:
                    _FOCUS_WINDOWS[_CURRENT_FOCUS].is_focused = True
                    main_window.redraw()
                    # Don't quit:
                    continue
            # Do Quit            # self._window.refresh()
            # time.sleep(.5):
            break
        except curses.error as e:
            _EXIT_ERROR = e
            break

    # Fix mouse mask:
    if reset_mouse_mask is not None:
        curses.mousemask(reset_mouse_mask)
        print('\033[?1003l', end='', flush=True)

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

    # Set logging path:
    common.SETTINGS['logPath'] = _CLI_SIGNAL_LOG_PATH
    logging.basicConfig(filename=_CLI_SIGNAL_LOG_PATH, encoding='utf-8', level=logging.DEBUG)
    _LOGGER = logging.getLogger(__name__)
    _LOGGER.debug("Logging started.")

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
    # cliSignal logging:
    do_log = parser.add_mutually_exclusive_group()
    do_log.add_argument('--logging',
                        help="Enable cliSignal logging.",
                        action='store_true',
                        default=None
                        )
    do_log.add_argument('--noLogging',
                        help="Disable cliSignal logging.",
                        action='store_false',
                        dest='logging'
                        )
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
    # Parse args:
    _args: argparse.Namespace = parser.parse_args()

    # Parse --debug and --verbose options:
    if _args.debug:
        _DEBUG = True
        _VERBOSE = True
        prettyPrint.DEBUG = True
        prettyPrint.VERBOSE = True
    elif _args.verbose:
        _VERBOSE = True
        prettyPrint.VERBOSE = True

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
    except ConfigFileError as e:
        if e.error_number == 21:
            out_error("Permissions of config file must be 600.")
        else:
            out_error("ConfigFileError: %s" % e.error_message)
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

    # Tell the terminal to report mouse movements:

    # Run main:
    _CURSES_STARTED = True
    curses.wrapper(main, _signal_cli)
    _CURSES_STARTED = False



    # Stop signal
    out_info("Stopping signal.", force=True)
    _signal_cli.stop_signal()

    if _EXIT_ERROR is not None:
        if _RESIZING:
            out_error("Window size too small. Fatal.")
        out_error("EXITED DUE TO ERROR: %s" % str(_EXIT_ERROR.args))
        if _DEBUG:
            print(_EXIT_ERROR.__traceback__)
            raise _EXIT_ERROR
        exit(14)
    exit(0)
