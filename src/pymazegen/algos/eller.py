import random

import src.pymazegen.algos.config as config
from src.pymazegen.maze import Cell, Grid, CircGrid


def _get_tree_index(cell: Cell, container: list) -> int:
    assert container is not None

    for i, set_ in enumerate(container):
        if cell in set_:
            return i


def _create_link_to_next_row(tree_set: set) -> set[Cell]:
    tree_set = list(tree_set)
    random.shuffle(tree_set)
    new_set = set()

    for i in range(0, random.randint(1, len(tree_set))):
        cell = tree_set[i]
        # new_set.add(cell.bottom)
        # cell.link_to(cell.bottom)
        if type(config.grid) == Grid:
            bottom_ = cell.bottom
        elif type(config.grid) == CircGrid:
            bottom_ = random.choice(cell.bottom)
        new_set.add(bottom_)
        cell.link_to(bottom_)

    assert len(new_set) > 0
    return new_set


def build_maze(anim: bool = False) -> None:
    tree_sets: list[set[Cell]] = []

    for row in config.grid.get_next_row():
        is_last_row = row == config.grid.cells[-1]

        for cell in row:
            if cell is not None:
                if not cell.has_linked_cells():
                    tree_sets.append(set())
                    tree_sets[-1].add(cell)
                    cell.link_to(cell)
                    i = -1
                else:
                    i = _get_tree_index(cell, tree_sets)
                    assert i is not None

                is_each_in_same_tree = cell.left and cell.left in tree_sets[i]

                if cell.left and not is_each_in_same_tree:
                    is_to_be_joined = bool(random.randrange(0, 2)) or is_last_row

                    if is_to_be_joined:
                        i_l = _get_tree_index(cell.left, tree_sets)

                        # In CircGrid the far left neighbour (left neighbour of first cell in the row)
                        # is the last cell in row - the rows are circular linked lists.
                        # Therefore, _get_tree_index() returns None, this would crash the code below
                        # at the set union, invoking:
                        # 'TypeError: list indices must be integers or slices, not NoneType'
                        if i_l is None:
                            continue

                        cell.link_to(cell.left)
                        tree_sets[i_l] = tree_sets[i_l] | tree_sets[i]
                        tree_sets.remove(tree_sets[i])

        if not is_last_row:
            for tree_set in tree_sets[:]:
                tree_sets.remove(tree_set)
                tree_sets.append(_create_link_to_next_row(tree_set))
            assert len(tree_sets) > 0

