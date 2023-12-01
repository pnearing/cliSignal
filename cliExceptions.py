#!/usr/bin/env python3
"""
File: cliExceptions.py
Store Exceptions to throw.
"""


class Error(Exception):
    """
    Base error class.
    """
    def __init__(self, message: str, *args) -> None:
        """
        Initialize an Error
        :param message: str: The error message.
        :param args: Any additional arguments to store in the exception.
        """
        super().__init__(message, *args)
        self._message: str = message
        return

    @property
    def message(self) -> str:
        """
        Return the message of the error.
        :return:
        """
        return self._message


class ParameterError(Error):
    """
    Exception to throw when there is a parameter error.
    """
    def __init__(self, param_name: str, conflict_message: str, *args) -> None:
        """
        Initialize a ParameterError.
        :param param_name: str: The name of the parameter.
        :param conflict_message: str: The error / conflict message.
        :param args: Any additional arguments to store in the exception.
        """
        error_message: str = "Error with parameter: '%s', Message: '%s'." % (param_name, conflict_message)
        super().__init__(error_message, *args)
        self._param_name: str = param_name
        self._conflict_message: str = conflict_message
        return

    @property
    def param_name(self) -> str:
        """
        Parameter name that caused the conflict.
        :return: str: The parameter name.
        """
        return self._param_name

    @property
    def conflict_message(self) -> str:
        """
        The message associated with the conflict.
        :return: str: The conflict message.
        """
        return self._conflict_message


class CallbackCausedException(Error):
    """
    Exception to throw when a callback causes an error.
    """
    def __init__(self, callback_name: str, error: Exception, *args: tuple) -> None:
        """
        Initialize a CallbackCausedException error.
        :param callback_name: str: The callback name.
        :param error: Exception: The Error the call back caused.
        :param args: tuple: Any additional arguments to add to the exception.
        """
        error_message: str = "Callback: '%s' caused an Exception of type '%s', with arguments: '%s'" \
                             % (callback_name, str(type(error)), str(error.args))
        super().__init__(error_message, *args)
        self._error: Exception = error
        return

    @property
    def error(self) -> Exception:
        """
        The Exception object that caused the error.
        :return: Exception: The Exception object.
        """
        return self._error


class Quit(Error):
    """
    While not actually an error, here is the quit error.
    """
    def __init__(self, *args) -> None:
        """
        Initialize the Quit object.
        :param args: Any additional arguments.
        """
        super().__init__("QUIT", *args)
        return




