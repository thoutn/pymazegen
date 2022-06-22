from __future__ import annotations


from enum import Enum

import src.pymazegen.algos as algos
import src.pymazegen.algos.config as config
from src.pymazegen.maze import Grid, CircGrid
from .presenter import *


class Algo(Enum):
    """The parameter taken by build_maze() function. It defines the algorithm to be used
    for maze generation."""
    BINARY_TREE = 0
    SIDEWINDER = 1
    RECURSIVE_BACKTRACKING = 2
    PRIM = 3
    KRUSKAL = 4
    ELLER = 5
    HUNT_AND_KILL = 6
    ALDOUS_BRODER = 7
    WILSON = 8
    RECURSIVE_DIVISION = 9
    GROWING_TREE = 10


algo_str: list = [
    "binary_tree",
    "sidewinder",
    "recursive_backtracking",
    "prim",
    "kruskal",
    "eller",
    "hunt_and_kill",
    "aldous_broder",
    "wilson",
    "recursive_division",
    "growing_tree",
]


class Mode(Enum):
    """The parameter taken by the init_maze() function. It defines the maze type
    (RECTANGULAR or CIRCULAR) that will be generated."""
    RECT = 0
    RECTANGULAR = 1
    CIRC = 2
    CIRCULAR = 3


def get_maze() -> Grid:
    """Returns the maze in its raw format = a python object representing the maze
    internally in the 'pymazegen' package."""
    return config.grid


def init_maze(height: int, width: int = 0, *, mode: str | Mode = Mode.RECT) -> None:
    """
    Initialises the maze geometry.

    :param int height: the height of a rectangular maze or the radius of the circular maze;
    :param int width: the width of a rectangular maze. In case the maze is of size (a x a),
        this parameter is not mandatory.
        For a circular maze this parameter is irrelevant; the length of each row
        (number of cells per row) is defined by a ratio factor -> cell width ~ cell height.
    :param str | Mode mode: a switch to build rectangular or circular mazes.
    :return: None. The initialised maze can be accessed through other functions, such as
        'get_maze()'.
    """
    if any(mode == m for m in [Mode.RECT, Mode.RECTANGULAR, 'rect', 'rectangular']):
        if width == 0: width = height
        config.grid = Grid(width, height)
    elif any(mode == m for m in [Mode.CIRC, Mode.CIRCULAR, 'circ', 'circular']):
        config.grid = CircGrid(height)

    config.height = height
    config.width = width
    config.mode = mode


def _validate_param(algo: str | Algo) -> None:
    """
    Checks if parameter 'algo' of 'build_maze()' is a valid string or 'Algo'.

    :param algo: the algorithm selected by the user.
    :return: None.
    :raises ValueError: if the 'algo' is not one of the defined ones.
    """
    global algo_str
    if not any(algo == Algo[a.name] for a in Algo) and not any(algo == a for a in algo_str):
        lst = ['Algo[\'' + a.name + '\']' for a in Algo]
        raise ValueError(f"""param 'algo' should be one of the following:
                {lst}
                {algo_str}""")


def _reinit_maze() -> None:
    """Resets the maze, if maze is already initialised. """
    if config.grid is not None:
        init_maze(config.height, config.width, mode=config.mode)
    else:
        init_maze(20)


def build_maze(*, algo: str | Algo = Algo.RECURSIVE_BACKTRACKING, anim: bool = False) -> None:
    """
    Generates a random maze using one of the selected algorithms.
    If option 'anim' is ticked it logs the build steps - can produce animation using
    'save_anim()'.

    .. note::
        - When used repeatedly it rewrites the previous maze.
        - To use the previously generated maze, use an assignment with 'get_maze()'.

    :param str | Algo algo: the algorithm to generate the maze. List of built-in algos: [
        BINARY_TREE,
        SIDEWINDER,
        RECURSIVE_BACKTRACKING,
        PRIM,
        KRUSKAL,
        ELLER,
        HUNT_AND_KILL,
        ALDOUS_BRODER,
        WILSON,
        RECURSIVE_DIVISION,
        GROWING_TREE - Not yet implemented
        ]
    :param bool anim: if set to 'True' the build steps are logged.
        Set to 'False' by default.
    :return: None. The final maze can be accessed through other functions,
        such as 'get_maze()'.
    """
    _validate_param(algo)
    _reinit_maze()

    build_fnc = {
        Algo.BINARY_TREE: algos.binary_tree_,
        "binary_tree": algos.binary_tree_,
        Algo.SIDEWINDER: algos.sidewinder_,
        "sidewinder": algos.sidewinder_,
        Algo.RECURSIVE_BACKTRACKING: algos.recursive_backtracking_,
        "recursive_backtracking": algos.recursive_backtracking_,
        Algo.PRIM: algos.prim_,
        "prim": algos.prim_,
        Algo.KRUSKAL: algos.kruskal_,
        "kruskal": algos.kruskal_,
        Algo.ELLER: algos.eller_,
        "eller": algos.eller_,
        Algo.HUNT_AND_KILL: algos.hunt_kill_,
        "hunt_and_kill": algos.hunt_kill_,
        Algo.ALDOUS_BRODER: algos.aldous_broder_,
        "aldous_broder": algos.aldous_broder_,
        Algo.WILSON: algos.wilson_,
        "wilson": algos.wilson_,
        Algo.RECURSIVE_DIVISION: algos.recursive_division_,
        "recursive_division": algos.recursive_division_,
        }[algo]

    build_fnc(anim)
