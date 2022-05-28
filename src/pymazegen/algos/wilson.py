import random

import src.pymazegen.algos.config as config
from src.pymazegen.maze import Cell


def _do_random_walk(current_cell: Cell) -> dict:
    walked_path = {}

    while True:
        neighbour = random.choice(current_cell.neighbours())
        walked_path[current_cell] = neighbour
        if not neighbour.has_linked_cells():
            current_cell = neighbour
        else:
            return walked_path


def build_maze(anim: bool = False) -> None:
    cell = config.grid.get_random_cell()
    cell.link_to(cell)
    unvisited_count = config.grid.size - 1

    while unvisited_count > 0:
        while True:
            start_cell = config.grid.get_random_cell()
            if not start_cell.has_linked_cells():
                break

        path = _do_random_walk(start_cell)

        current_cell = start_cell
        while path:
            unvisited_count -= 1
            if not path[current_cell].has_linked_cells():
                current_cell.link_to(path[current_cell])
                current_cell = path[current_cell]
            else:
                current_cell.link_to(path[current_cell])
                break

