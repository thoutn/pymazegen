import random

import src.pymazegen.algos.config as config
from src.pymazegen.maze import Cell


def _save_step(c: Cell, n: Cell, stack: list = tuple(), col: str = 'r') -> None:
    """Saves the build steps that are used ot generate an animation."""
    if col == 'w':
        if stack:
            n = stack[-1]
        else:
            n = c

    config.build_steps.append((c.row, c.column, n.row, n.column, col))


def build_maze(anim: bool = False) -> None:
    stack: list[Cell] = [config.grid.get_random_cell()]

    while stack:
        current_cell = stack[-1]

        if neighbours := [cell for cell in current_cell.neighbours()
                          if not cell.has_linked_cells()]:
            random.shuffle(neighbours)
            neighbour = neighbours.pop()

            stack.append(neighbour)
            current_cell.link_to(neighbour)

            if anim:
                _save_step(current_cell, neighbour)
        else:
            visited = stack.pop()

            if anim:
                _save_step(visited, visited, stack, 'w')
