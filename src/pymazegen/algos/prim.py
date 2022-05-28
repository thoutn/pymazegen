import random

import src.pymazegen.algos.config as config
from src.pymazegen.maze import Cell


def build_maze(anim: bool = False) -> None:
    frontier_cells: set[Cell] = set()
    frontier_cells.add(config.grid.get_random_cell())

    while frontier_cells:
        current_cell = random.choice(list(frontier_cells))
        frontier_cells.remove(current_cell)

        if neighbours := {cell for cell in current_cell.neighbours() if not cell.has_linked_cells()}:
            frontier_cells = frontier_cells | neighbours

        if in_cells := [cell for cell in current_cell.neighbours() if cell.has_linked_cells()]:
            in_cell = random.choice(in_cells)
            in_cell.link_to(current_cell)
        else:
            current_cell.link_to(current_cell)

