from typing import Optional


class Piece:
    """
    This class represents a single playing piece in a checkers-like game. It holds
    essential information such as the piece's unique ID, color, position, and king status.
    """

    def __init__(self, id: int, color: bool, position: Optional[tuple[int, int]] = None, king: bool = False):
        """
        Initializes a new checkers piece.

        Args:
            id (int): A non-negative integer that uniquely identifies the piece.
            color (bool): The color of the piece. True typically represents a dark piece, and False represents a light piece.
            position (Optional[tuple[int, int]]): The (row, column) coordinates of the piece on the board.
                                                  Defaults to None if the piece is not yet on the board.
            king (bool): A boolean flag indicating whether the piece is a king. King pieces have different movement rules.
                         Defaults to False.
        """
        if not isinstance(id, int) or id < 0:
            raise ValueError("ID must be a non-negative integer.")
        if not isinstance(color, bool):
            raise ValueError("Color must be a boolean (True for dark, False for light).")
        if not isinstance(position, tuple | None) or (position is not None and (len(position) != 2 or not all(isinstance(i, int) for i in position))):
            raise ValueError("Position must be a 2-tuple of ints or None.")

        self.id = id
        self.color = color
        self.position = position
        self.king = king

    def __repr__(self) -> str:
        """Returns a developer-friendly string representation of the piece."""
        return f'{self.id}_{"dark" if self.color else "light"}'

    def __str__(self) -> str:
        """Returns a user-friendly string representation of the piece."""
        return self.__repr__()

    def __lt__(self, other) -> bool:
        """Compares two Piece objects based on their ID."""
        if not isinstance(other, Piece):
            return NotImplemented
        return self.id < other.id

    def __eq__(self, other) -> bool:
        """Checks for equality based on ID and color."""
        if not isinstance(other, Piece):
            return NotImplemented
        return self.id == other.id and self.color == other.color

    def __hash__(self) -> int:
        """
        Makes the object hashable. The hash is based on the immutable attributes: id and color.
        """
        return hash((self.id, self.color))
