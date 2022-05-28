import random

import src.pymazegen.algos.config as config


def build_maze(anim: bool = False) -> None:
    for row in config.grid.get_next_row():
        run = []

        for cell in row:
            run.append(cell)

            is_place_to_close_run = cell.right is None or cell.top is not None and random.randrange(0, 2) == 0

            if is_place_to_close_run:
                cell_ = random.choice(run)
                if cell_.top: cell_.link_to(cell_.top)
                run.clear()
            else:
                cell.link_to(cell.right)

