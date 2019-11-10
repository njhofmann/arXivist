from typing import Any
import enum as e


class EqualEnum(e.Enum):
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)):
            return self is other
        elif isinstance(other, str):
            return other == self.value
        return False

    @classmethod
    def is_valid(cls: type, other: str) -> bool:
        return any([other == item.value for item in cls])


if __name__ == '__main__':
    class Foo(EqualEnum):
        A = 'A'
        B = 'B'
    assert Foo.is_valid('A')
    assert Foo.is_valid('B')
