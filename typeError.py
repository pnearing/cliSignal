#!/usr/bin/env python3
from typing import Any, NoReturn
# Version:
VERSION: float = 1.0


def __type_error__(argument_name: str, desired_types: str, received_obj: Any) -> NoReturn:
    """
    Raise a TypeError with a good message.
    :param argument_name: Str: String of the variable name.
    :param desired_types: Str: String of desired type(s).
    :param received_obj: The var which was received, note: type() will be called on it.
    :return: NoReturn
    """
    error: str = "TypeError: argument:%s, got %s type, expected: %s" % (argument_name,
                                                                        str(type(received_obj)), desired_types)
    raise TypeError(error)
