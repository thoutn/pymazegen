from __future__ import annotations


import random

import src.pymazegen.algos.config as config
from src.pymazegen.maze import Cell
from src.pymazegen.misc import Label


def _choose_neighbour_of(cell: Cell, neighbours: set) -> Cell | None:
    neighbour = random.choice(list(neighbours))
    cell.link_to(neighbour)
    return neighbour

#TODO check why it's not working as it should
def build_maze(anim: bool = False) -> None:
    current_cell = config.grid.get_random_cell()
    rows_with_unvisited: list[int] = [row_id for row_id in range(config.grid._height)]

    while True:
        if neighbours := {n for n in current_cell.neighbours() if not n.has_linked_cells()}:
            current_cell = _choose_neighbour_of(current_cell, neighbours)
        else:
            is_unvisited_found = False
            with Label() as search:
                for row in rows_with_unvisited[:]:
                    for cell in config.grid.cells[row]:
                        if not cell.has_linked_cells():
                            if neighbours := {n for n in cell.neighbours() if n.has_linked_cells()}:
                                current_cell = _choose_neighbour_of(current_cell, neighbours)
                                is_unvisited_found = True
                                search.break_()
                    rows_with_unvisited.remove(row)

            if not is_unvisited_found:
                break


def build_maze(anim: bool = False) -> None:
    current_cell = config.grid.get_random_cell()
    unvisited_cells: set[Cell] = {current_cell}

    while unvisited_cells:
        if neighbours := {n for n in current_cell.neighbours() if not n.has_linked_cells()}:
            neighbour = random.choice(list(neighbours))
            neighbours.remove(neighbour)
            unvisited_cells = unvisited_cells | neighbours

            current_cell.link_to(neighbour)
            current_cell = neighbour
        else:
            for cell in list(unvisited_cells):
                if cell.has_linked_cells():
                    unvisited_cells.remove(cell)

            if unvisited_cells:
                current_cell = random.choice(list(unvisited_cells))
                unvisited_cells.remove(current_cell)

                visited_cells = [v for v in current_cell.neighbours() if v.has_linked_cells()]
                assert len(visited_cells) > 0
                current_cell.link_to(random.choice(visited_cells))

