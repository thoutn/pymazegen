from __future__ import annotations


import math
import random
from typing import Generator

from .cell import Cell, CircCell


class Grid:
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self.cells: list[list[Cell]] = []

        self._prepare_grid()
        self._configure_cells()

    def _prepare_grid(self) -> None:
        for row in range(self._height):
            self.cells.append(list())
            for col in range(self._width):
                self.cells[row].append(Cell(row, col))

    def _configure_cells(self) -> None:
        for row in self.cells:
            for cell in row:
                row_, col_ = cell.row, cell.column

                cell.top = self._create_neighbours(row_ - 1, col_)
                cell.bottom = self._create_neighbours(row_ + 1, col_)
                cell.right = self._create_neighbours(row_, col_ + 1)
                cell.left = self._create_neighbours(row_, col_ - 1)

    def _create_neighbours(self, row, column) -> Cell | None:
        if 0 <= row <= self._width - 1 and 0 <= column <= self._height - 1:
            return self.cells[row][column]
        else:
            return None

    def get_random_cell(self) -> Cell:
        return self.cells[random.randrange(0, self._height)][random.randrange(0, self._width)]

    @property
    def size(self) -> int:
        return self._width * self._height

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    def get_next_row(self) -> Generator[list[Cell], None, None]:
        for row in self.cells:
            yield row

    def get_next_cell(self) -> Generator[Cell | None, None, None]:
        for row in self.cells:
            for cell in row:
                yield cell if cell else None


class CircGrid(Grid):
    def __init__(self, height: int):
        super().__init__(1, height)

    def _prepare_grid(self) -> None:
        self.cells.append(list())
        self.cells[0].append(CircCell(0, 0))
        self._size = 1

        for row in range(1, self._height):
            self.cells.append(list())

            previous_count = len(self.cells[row - 1])
            ratio = round((row * 2 * math.pi) / previous_count)
            cell_count = previous_count * ratio

            for col in range(cell_count):
                self.cells[row].append(CircCell(row, col))

            self._size += cell_count

    def _configure_cells(self) -> None:
        for row in self.cells:
            for cell in row:
                row_, col_ = cell.row, cell.column

                if row_ > 0:
                    if col_ != 0:
                        cell.left = self.cells[row_][col_ - 1]
                    else:
                        cell.left = self.cells[row_][-1]

                    if col_ != len(row) - 1:
                        cell.right = self.cells[row_][col_ + 1]
                    else:
                        cell.right = self.cells[row_][0]

                    ratio = len(self.cells[row_]) // len(self.cells[row_ - 1])
                    parent = self.cells[row_ - 1][col_ // ratio]
                    cell.top = parent
                    parent.bottom.append(cell)

    def get_random_cell(self) -> Cell:
        row = random.randrange(0, self._height)
        return self.cells[row][random.randrange(0, len(self.cells[row]))]

    @property
    def size(self) -> int:
        return self._size
