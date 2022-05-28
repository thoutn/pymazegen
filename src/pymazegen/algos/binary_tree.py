from __future__ import annotations

import random

import src.pymazegen.algos.config as config
from src.pymazegen.maze import Cell, Grid, CircGrid


def _choose_neighbour_of(cell: Cell) -> Cell | None:
    neighbours = []
    if cell.bottom:
        if type(config.grid) == Grid: neighbours.append(cell.bottom)
        elif type(config.grid) == CircGrid: neighbours.extend(cell.bottom)
    # if cell.top: neighbours.extend([cell.top]*3)
    if cell.right: neighbours.append(cell.right)
    # if cell.right: neighbours.extend([cell.right]*3)

    if neighbours:
        neighbour = random.choice(neighbours)
        return neighbour
    return None


def build_maze(anim: bool = False) -> None:
    for cell in config.grid.get_next_cell():
        # neighbour = self._choose_neighbour_of(cell)
        if neighbour := _choose_neighbour_of(cell):
            cell.link_to(neighbour)

