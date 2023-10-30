#!/usr/bin/env python3
from typing import Optional
import argparse
import os.path
import curses
from SignalCliApi import SignalCli
from configFile import ConfigFile, ConfigFileError
import common
from mainWindow import MainWindow


def main(std_screen: curses.window) -> None:

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    main_window = MainWindow(std_screen)
    main_window.redraw()
    try:
        while True:
            char_code: int = std_screen.getch()
            if char_code == curses.KEY_RESIZE:
                main_window.redraw()
    except KeyboardInterrupt:
        pass

    # _signal_cli: SignalCli = SignalCli(signal_config_path=common.SETTINGS['signalConfigDir'],
    #                                    signal_exec_path=common.SETTINGS['signalExecPath'],
    #                                    log_file_path=common.SETTINGS['signalLogFile'],
    #                                    server_address=common.SETTINGS['signalSocketFile'],
    #                                    start_signal=common.SETTINGS['startSignal']
    #                                    )
    # curses.napms(10000)
    return


if __name__ == '__main__':
    # Setup command line arguments:
    parser = argparse.ArgumentParser(description="Command line Signal client.",
                                     epilog="Written by Peter Nearing."
                                     )
    parser.add_argument('--config',
                        help="The full path to the config file, default is $HOME/.config/cliSignal.config",
                        type=str
                        )
    parser.add_argument('--store',
                        help="Save the command line options to the config.",
                        action='store_true',
                        default=False
                        )
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
    parser.add_argument('--signalLogPath',
                        help="The full path to the signal log file, by default logging is turned off.",
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
    # Parse args:
    args: argparse.Namespace = parser.parse_args()

    # load config:
    try:
        config_file: ConfigFile = ConfigFile("cliSignal",
                                             file_path=args.config,
                                             set_permissions=0o600,
                                             enforce_permissions=True
                                             )
    except ConfigFileError as e:
        if e.error_number == 21:
            print("ERROR: Permissions of config file must be 600.")
        else:
            print("ERROR:", e.error_message)
        exit(2)
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
        exit(3)

    # --signalSocketPath:
    if args.signalSocketPath is not None:
        common.SETTINGS['signalSocketPath'] = args.signalSocketFile
    if common.SETTINGS['signalSocketPath'] is not None:
        if (not os.path.exists(common.SETTINGS['signalSocketPath']) or
                not os.path.isfile(common.SETTINGS['signalSocketPath'])):
            print("ERROR: --signalSocketPath must point to an existing socket file.")
            exit(4)
    if args.noStartSignal and common.SETTINGS['signalSocketPath'] is None:
        print("ERROR: --signalSocketPath must point to an existing file if using --noStartSignal.")
        exit(5)

    # --signalLogPath:
    if args.signalLogPath is not None:
        common.SETTINGS['signalLogPath'] = args.signalLogPath
    # Check that the log file containing directory exists:
    if common.SETTINGS['signalLogPath'] is not None:
        log_dir: str = os.path.join(*os.path.split(common.SETTINGS['signalLogPath'])[:-1])
        if not os.path.exists(log_dir) or not os.path.isdir(log_dir):
            print("ERROR: Directory containing the log file doesn't exist.")
            exit(6)

    # --signalExecPath:
    if args.signalExecPath is not None:
        common.SETTINGS['signalExecPath'] = args.signalExecPath
    if common.SETTINGS['signalExecPath'] is not None and (not os.path.exists(common.SETTINGS['signalExecPath']) or
                                                          not os.path.isfile(common.SETTINGS['signalExecPath'])):
        print("ERROR: --signalExecPath must point to an existing signal-cli executable file.")
        exit(7)

    curses.wrapper(main)
    exit(0)
