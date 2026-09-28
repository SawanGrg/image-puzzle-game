from abc import ABC, abstractmethod


class Transformation(ABC):

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def apply(self, tiles: list):
        pass

    @abstractmethod
    def undo(self):
        pass
