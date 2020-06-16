from __future__ import annotations
import abc
import enum as e
from typing import Any, List, Callable
import dataclasses as dc
import src.utility.save_query as sq


@dc.dataclass(frozen=True)
class Command:
    name: str  # str id
    func: Callable[[List[str]], None]  # method to call
    help: str  # what this cmd does


class CmdEnum(e.Enum):
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)):
            return self is other
        elif isinstance(other, str):
            return other == self.value.name
        return False

    @classmethod
    def is_valid(cls: type, other: str) -> bool:
        return any([other == item.value.name for item in cls])

    @classmethod
    def values_as_str(cls: e.Enum) -> str:
        return ', '.join(item.value.name for item in cls)

    @classmethod
    def display_available_options(cls: e.Enum) -> None:
        print('available modes are ' + cls.values_as_str())

    @classmethod
    def display_help_options(cls: e.Enum):
        print('options:\n' + '\n'.join([f'- {mode.value.name}: {mode.value.help}' for mode in cls]))

    @classmethod
    def execute_params(cls, args: List[str], save_query: sq.SaveQuery = None) -> CmdEnum:
        """Maps the relationship between each defined type of CommandEnum and associated operations. Given a list of
        parameters, a command and any relevant arguments, attempts to execute operations associated with command listed
        in the params, should be the first item in the list - ie "cmd arg1 ... argn". Throws ValueError if unsupported
        command is given or if incorrect args are given. Returns the type of CommandEnum that was executed.
        :param args: list of params to execute an operation associated with a type of CommandEnum
        :param save_query: optional param, used for storing any neccessary info related to previously retrieved info
        :return: type of CommandEnum executed
        """
        if not args:
            raise ValueError(f"not provided a response, must be one of {cls.values_as_str()}")

        cmd, params = args[0], args[1:]
        for mode in cls:
            if cmd == mode:
                mode.value.func(params)
                return mode
        raise ValueError(f'invalid response {cmd}, must be one of {cls.values_as_str()}')


def is_list_of_n_ints(to_parse: List[str], n: int = -1) -> List[int]:
    if not to_parse:
        return []
    elif -1 < n != len(to_parse):  # -1 means variable length
        raise ValueError(f'given list {to_parse} must have only {n} entries')
    return [int(item) for item in to_parse]
