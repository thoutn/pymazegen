import random

import src.pymazegen.algos.config as config


def build_maze(anim: bool = False) -> None:
    unvisited_count = config.grid.size - 1
    current_cell = config.grid.get_random_cell()

    while unvisited_count > 0:
        neighbour = random.choice(current_cell.neighbours())
        if not neighbour.has_linked_cells():
            current_cell.link_to(neighbour)
            current_cell = neighbour

            unvisited_count -= 1
        else:
            current_cell = neighbour

