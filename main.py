#!/usr/bin/env python3
from typing import Optional, TextIO
import argparse
import os.path
import curses
import json
from SignalCliApi import SignalCli
from configFile import ConfigFile, ConfigFileError
import common
from themes import load_theme, init_colours
from mainWindow import MainWindow
from contactsWindow import ContactsWindow

_WORKING_DIR_NAME: str = '.cliSignal'
"""Name of the working directory under $HOME."""
_CONFIG_NAME: str = 'cliSignal'
"""Name to give our config file configuration."""
_CONFIG_FILE_NAME: str = 'cliSignal.config'
"""Name of the cliSignal config file."""
_SIGNAL_CONFIG_DIR_NAME: str = 'signal-cli'
"""Name to give the signal-cli config directory. (where signal-cli stores it's files)."""
_SIGNAL_LOG_FILE_NAME: str = 'signal-cli.log'
"""Name of the signal-cli log file."""
_CLI_SIGNAL_LOG_FILE_NAME: str = 'cliSignal.log'
"""Name of the cliSignal log file."""


def main(std_screen: curses.window) -> None:
    # Setup extended key codes, including mouse move events:
    std_screen.keypad(True)
    # Ask for mouse move events, and position change event:
    # curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)

    # Setup colour pairs according to theme:
    if not curses.has_extended_color_support():
        raise RuntimeError("Terminal capable of 256 colours required.")
    theme: dict[str, dict[str, int | bool | str]] = load_theme()
    init_colours(theme)

    # Create the windows:
    main_window = MainWindow(std_screen, theme)
    main_window.redraw()

    # signal_cli: SignalCli = SignalCli(signal_config_path=common.SETTINGS['signalConfigDir'],
    #                                    signal_exec_path=common.SETTINGS['signalExecPath'],
    #                                    log_file_path=common.SETTINGS['signalLogFile'],
    #                                    server_address=common.SETTINGS['signalSocketFile'],
    #                                    start_signal=common.SETTINGS['startSignal']
    #                                    )

    # Main loop:
    try:
        while True:
            char_code: int = std_screen.getch()
            if char_code == curses.KEY_RESIZE:
                main_window.resize()
                main_window.redraw()
                pass
    except KeyboardInterrupt:
        pass

    return


if __name__ == '__main__':

    # Setup command line arguments:
    parser = argparse.ArgumentParser(description="Command line Signal client.",
                                     epilog="Written by Peter Nearing."
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
    # Parse args:
    args: argparse.Namespace = parser.parse_args()

    # Setup .cliSignal directory, and change to it:
    home_dir: str = os.environ.get('HOME')
    working_dir: str = os.path.join(home_dir, _WORKING_DIR_NAME)
    if not os.path.exists(working_dir):
        try:
            os.mkdir(working_dir, 0o700)
        except (OSError, PermissionError, FileNotFoundError):
            print("ERROR: Failed to create '%s' directory." % working_dir)
            exit(2)
    os.chdir(working_dir)

    # Make signal-cli config dir if required:
    signal_config_dir: str = os.path.join(working_dir, _SIGNAL_CONFIG_DIR_NAME)
    if not os.path.exists(signal_config_dir):
        try:
            os.mkdir(signal_config_dir, 0o700)
        except (OSError, FileNotFoundError, PermissionError):
            print("ERROR: Failed to create '%s' directory.")
            exit(3)

    # Parse --config option:
    cli_signal_config_path: str = os.path.join(working_dir, _CONFIG_FILE_NAME)
    if args.config is not None:
        cli_signal_config_path: str = args.config

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
            print("ERROR: Permissions of config file must be 600.")
        else:
            print("ERROR:", e.error_message)
        exit(4)

    # Validate / act on arguments:

    # --noStartSignal:
    if args.noStartSignal:
        common.SETTINGS['startSignal'] = False

    # --signalConfigDir:
    if args.signalConfigDir is not None:
        common.SETTINGS['signalConfigDir'] = args.signalConfigPath

    if common.SETTINGS['signalConfigDir'] is not None and (not os.path.exists(common.SETTINGS['signalConfigDir']) or
                                                           not os.path.isdir(common.SETTINGS['signalConfigDir'])):
        print("ERROR: --signalConfigPath must be an existing directory.")
        exit(5)

    # --signalSocketPath:
    if args.signalSocketPath is not None:
        common.SETTINGS['signalSocketPath'] = args.signalSocketFile
    if common.SETTINGS['signalSocketPath'] is not None:
        if (not os.path.exists(common.SETTINGS['signalSocketPath']) or
                not os.path.isfile(common.SETTINGS['signalSocketPath'])):
            print("ERROR: --signalSocketPath must point to an existing socket file.")
            exit(6)

    # --signalExecPath:
    if args.signalExecPath is not None:
        common.SETTINGS['signalExecPath'] = args.signalExecPath
    if common.SETTINGS['signalExecPath'] is not None and (not os.path.exists(common.SETTINGS['signalExecPath']) or
                                                          not os.path.isfile(common.SETTINGS['signalExecPath'])):
        print("ERROR: --signalExecPath must point to an existing signal-cli executable file.")
        exit(7)

    # Verify arguments; If --noStartSignal, --signalSocketPath must be defined:
    if args.noStartSignal and common.SETTINGS['signalSocketPath'] is None:
        print("ERROR: --signalSocketPath must point to an existing file if using --noStartSignal.")
        exit(8)

    # Verify theme:
    if args.theme is not None:
        if args.theme not in ('light', 'dark', 'custom'):
            print("ERROR: --theme must be either: 'light', 'dark', or 'custom'.")
            exit(9)
        common.SETTINGS['theme'] = args.theme
    # Verify theme is correct:
    if common.SETTINGS['theme'] not in ('light', 'dark', 'custom'):
        print("ERROR: 'theme' must be one of: 'light', 'dark', or 'custom'")
        exit(10)
    if common.SETTINGS['theme'] == 'custom':
        # If there is no theme path, throw an error.
        if args.themePath is None and common.SETTINGS['themePath'] is None:
            print("ERROR: If --theme is 'custom', either --themePath must be supplied, or 'themePath' must be "
                  "defined in your configuration file.")
            exit(11)
        # Override settings theme path with the args theme path:
        elif args.themePath is not None:
            common.SETTINGS['themePath'] = args.themePath
        # Check that the theme path exists:
        if not os.path.exists(common.SETTINGS['themePath']) or not os.path.isfile(common.SETTINGS['themePath']):
            print("ERROR: 'themePath' must point to an existing file.")
            exit(12)

    # Parse: --store
    if args.store:
        try:
            config_file.save()
        except ConfigFileError as e:
            print("ERROR:", e.error_message)
            exit(9)

    curses.wrapper(main)
    exit(0)
