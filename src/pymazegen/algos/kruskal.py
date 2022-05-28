import random

import src.pymazegen.algos.config as config
from src.pymazegen.maze import Cell, Grid, CircGrid


def build_maze(anim: bool = False) -> None:
    tree_sets: dict[Cell, set[Cell]] = {cell: {cell} for cell in config.grid.get_next_cell()}
    if type(config.grid) == Grid:
        walls = [(c_, n_) for c_ in config.grid.get_next_cell() for n_ in (c_.bottom, c_.right) if n_]
    elif type(config.grid) == CircGrid:
        walls = [(c_, n_) for c_ in config.grid.get_next_cell() for n_ in [c_.right] + [b for b in c_.bottom] if n_]

    set_count = config.grid.size
    random.shuffle(walls)
    while walls and set_count > 1:
        cell, neighbour = walls.pop()

        if neighbour not in tree_sets[cell]:
            cell.link_to(neighbour)

            tree_sets[neighbour].update(tree_sets[cell])
            temp = tree_sets[neighbour]

            for key in list(temp):
                tree_sets[key] = temp

            set_count -= 1

