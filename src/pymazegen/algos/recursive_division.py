from enum import IntEnum
import random

import src.pymazegen.algos.config as config
from src.pymazegen.maze import Grid, CircGrid


class Orientation(IntEnum):
    HORIZONTAL = 0
    VERTICAL = 1


def _choose_orientation(width, height) -> int:
    if width < height:
        return 0
    elif width > height:
        return 1
    else:
        return random.randint(0, 1)


def _get_coord(start: int, end: int, with_last: bool) -> int:
    """
    A 'helper function' (following the DRY concept) to return a coordinate of either
    the line bisecting the field or of the passage through this bisection.

    :param int start: the initial coordinate of the field in x or y direction;
    :param int end: the terminal coordinate of the field in x or y direction;
    :param bool with_last: a switch between random.randrange and random.randint.
        Note: while the terminal value for the bisecting line is exclusive,
        it is inclusive for the passage terminal value.
    :return: the integer value of the x or y coordinate of the bisecting line or passage.
    """
    if end - start + 1 > 1:
        return random.randrange(start, end + int(with_last))
    else:
        return start


def _gen_sub_field(queue: list, coords: tuple[int, int, int, int], dir_: int) -> None:
    """
    A 'helper function' to enqueue the new child field created by bisecting
    the parent field of the maze.

    :param list queue: the queue of all fields to bisect;
    :param tuple coords: the child field coordinates;
    :param int dir_: an integer value corresponding to the Orientation enum entries.
    :return: None
    """
    u1, u2, v1, v2 = coords

    if v2 - v1 + 1 >= 2 or u2 - u1 > 0:
        if dir_ == 0:
            queue.append((v1, u1, v2, u2))
        else:
            queue.append((u1, v1, u2, v2))


def _bisect_rect(queue: list, field: tuple[int, int, int, int], dir_: int) -> tuple[int, int]:
    """
    A specific implementation of the 'bisect' 'helper function' valid for rectangular
    mazes, represented in cartesian coordinates.

    :param list queue: the queue of all fields to bisect;
    :param tuple field: the current field the function divides;
    :param int dir_: an integer value corresponding to the Orientation enum entries.
    :return: a tuple of x, y coordinates of the passage through the bisecting line.
    """
    u1, u2, v1, v2 = field
    bisect = _get_coord(u1, u2, False)
    passage = _get_coord(v1, v2, True)

    _gen_sub_field(queue, (u1, bisect, v1, v2), dir_)
    _gen_sub_field(queue, (bisect + 1, u2, v1, v2), dir_)

    return bisect, passage


def _bisect_circ(queue: list, field: tuple[int, int, int, int], dir_: int) -> tuple[int, int]:
    """
    A specific implementation of the 'bisect' 'helper function' valid for circular mazes,
    represented in polar coordinates.

    :param list queue: the queue of all fields to bisect;
    :param tuple field: the current field the function divides;
    :param int dir_: an integer value corresponding to the Orientation enum entries.
    :return: a tuple of x, y coordinates of the passage through the bisecting line.
    """
    u1, u2, v1, v2 = field
    bisect = _get_coord(u1, u2, False)

    _gen_sub_field(queue, (u1, bisect, v1, v2), dir_)

    # For correct sizing of the 2nd child field after bisecting the parent field.
    # This child field is on larger radius, thus may have higher
    # column count / row length then the 1st child field.
    # This portion of the code corrects the column coordinate to ensure the
    # 2nd child field includes all cells.
    if dir_ == Orientation.HORIZONTAL:
        ratio = len(config.grid.cells[bisect + 1]) // len(config.grid.cells[u1])
        v1 = v1 * ratio
        v2 = (v2 + 1) * ratio - 1

    _gen_sub_field(queue, (bisect + 1, u2, v1, v2), dir_)

    # For correct placement of vertical passage through a horizontal bisection.
    # In case the rows in the field have different column / length ratio,
    # this portion of the code corrects the column coordinate of the passage -
    # needed due to the previous modification above.
    if dir_ == Orientation.HORIZONTAL:
        ratio = len(config.grid.cells[bisect + 1]) // len(config.grid.cells[bisect])
        v1 = v1 // ratio
        v2 = v2 // ratio

    passage = _get_coord(v1, v2, True)

    # For correct placement of horizontal passage through a vertical bisection.
    # In case the rows in the field have different column / length ratio,
    # this portion of the code corrects the column coordinate of the passage.
    if dir_ == Orientation.VERTICAL:
        ratio = len(config.grid.cells[passage]) // len(config.grid.cells[v1])
        bisect = (bisect + 1) * ratio - 1

    return bisect, passage


def _bisect_field(queue: list, field: tuple[int, int, int, int], dir_: int) -> tuple[int, int]:
    """The main 'bisect' function. It calls the specific implementation
    corresponding to the maze type (rectangular or circular). """
    if type(config.grid) == Grid:
        return _bisect_rect(queue, field, dir_)
    elif type(config.grid) == CircGrid:
        return _bisect_circ(queue, field, dir_)


def build_maze(anim: bool = False) -> None:
    x1 = 0
    y1 = 0
    x2 = len(config.grid.cells[y1]) - 1
    y2 = config.grid._height - 1
    queue: list[tuple[int, int, int, int]] = [(x1, y1, x2, y2)]

    while queue:
        x1, y1, x2, y2 = queue.pop(0)

        if _choose_orientation(x2 - x1, y2 - y1) == Orientation.HORIZONTAL:
            bisect, col = _bisect_field(queue, (y1, y2, x1, x2), Orientation.HORIZONTAL)

            cell = config.grid.cells[bisect][col]
            if cell.bottom:
                if type(config.grid) == Grid:
                    cell.link_to(cell.bottom)
                elif type(config.grid) == CircGrid:
                    cell.link_to(random.choice(cell.bottom))
        else:
            bisect, row = _bisect_field(queue, (x1, x2, y1, y2), Orientation.VERTICAL)

            cell = config.grid.cells[row][bisect]
            if cell.right:
                cell.link_to(cell.right)

