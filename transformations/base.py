from abc import ABC, abstractmethod


class Transformation(ABC):
    """Base class for every scramble step.

    Subclasses must implement apply() and undo(), so Board can treat all
    transformations the same way (polymorphism).
    """

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def apply(self, tiles: list):
        """Apply the transformation to some of `tiles` and return what was changed."""

    @abstractmethod
    def undo(self):
        """Reverse the transformation."""