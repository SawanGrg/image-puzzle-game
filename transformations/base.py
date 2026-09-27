from abc import ABC, abstractmethod


class Transformation(ABC):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @abstractmethod
    def apply(self, tiles):
        pass