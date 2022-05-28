from __future__ import annotations


class Cell:
    """
    The Cell class used to represent a cell in the maze.
    """
    def __init__(self, row: int, column: int):
        self.row = row
        self.column = column

        self.links = {}

        self.top = None
        self.bottom = None
        self.right = None
        self.left = None

    def link_to(self, cell: Cell, bidirect=True) -> None:
        """Creates a link between the current and specified cell given as a parameter."""
        self.links[cell] = True
        if bidirect:
            cell.link_to(self, False)

    def unlink_from(self, cell: Cell, bidirect=True) -> None:
        del self.links[cell]
        if bidirect:
            cell.unlink_from(self, False)

    def has_linked_cells(self):
        """Check if it is linked to any cell in the maze."""
        return self.links.keys()

    def is_linked_to(self, cell: Cell) -> bool:
        """Checks if it is linked to the specified cell given as a parameter."""
        if cell in self.links.keys():
            return True
        return False

    def neighbours(self) -> list[Cell | None]:
        """Returns a list of all adjacent neighbours to cell.
        """
        lst = []
        if self.top: lst.append(self.top)
        if self.bottom: lst.append(self.bottom)
        if self.right: lst.append(self.right)
        if self.left: lst.append(self.left)
        return lst


class CircCell(Cell):
    """
    Modified Cell class for usage in the CircGrid (mazes represented in polar coordinates).
    """

    def __init__(self, row: int, column: int):
        """
        Calls the superclass initialiser and modifies the bottom neighbour from type 'Cell' to type 'list[Cell]'.

        :param int row: the ID of row, which contains the Cell
        :param int column: the ID of column, which contains the Cell
        """
        super().__init__(row, column)
        self.bottom: list[Cell] = []

    def neighbours(self) -> list[Cell | None]:
        """
        Almost identical to the superclass implementation, except of the way the bottom neighbours are added
        to the list of all neighbours.

        :return: a list of all neighbours or None if the cell has no neighbours.
        """
        lst = []
        if self.bottom: lst.extend(self.bottom)

        if self.top: lst.append(self.top)
        if self.right: lst.append(self.right)
        if self.left: lst.append(self.left)

        return lst

