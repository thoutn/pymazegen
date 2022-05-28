from __future__ import annotations


import math
import numpy as np
from PIL import Image, ImageDraw

from src.pymazegen.maze import Grid, CircGrid
import src.pymazegen.presenter.config as cfg
import src.pymazegen.algos.config as config


def img_config(*, cell_size: int = 20, wall_thickness: int = 2) -> None:
    """
    Configures the graphical representation of the generated maze.

    :param int cell_size: the area (a x a) of the cell used for the maze visualisation;
    :param int wall_thickness: the line thickness the wall is drawn with.
    :return: None.
    """
    cfg.cell_size = cell_size
    cfg.wall_thickness = wall_thickness
    cfg.size = (cell_size + wall_thickness)


def _set_size(size: int) -> int:
    return size * cfg.cell_size + (size + 1) * cfg.wall_thickness


def _render_rect_grid_img() -> Image:
    w = _set_size(config.grid.width)
    h = _set_size(config.grid.height)

    img = Image.new("RGB", size=(w, h), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)

    for cell in config.grid.get_next_cell():
        x1 = cell.column * cfg.size
        y1 = cell.row * cfg.size
        x2 = (cell.column + 1) * cfg.size
        y2 = (cell.row + 1) * cfg.size

        if cfg.wall_thickness % 2 != 0:
            offset1 = cfg.wall_thickness // 2
            offset2 = 0
        else:
            offset1 = cfg.wall_thickness // 2 - 1  # 0-2 1-4 2-6 3-8 4-10
            offset2 = 1

        def draw_line(a, b, c, d):
            draw.line((a, b, c, d), fill=(0, 0, 0), width=cfg.wall_thickness)

        if not cell.top: draw_line(x1, y1 + offset1, x2 + 2*offset1 + offset2, y1 + offset1)
        if not cell.left: draw_line(x1 + offset1, y1, x1 + offset1, y2 + 2*offset1)

        if not cell.is_linked_to(cell.bottom): draw_line(x1, y2 + offset1, x2 + 2*offset1 + offset2, y2 + offset1)
        if not cell.is_linked_to(cell.right): draw_line(x2 + offset1, y1, x2 + offset1, y2 + 2*offset1)

    return img


def _render_circ_grid_img() -> Image:
    wall_width = cfg.wall_thickness * cfg.ANTIALIAS_
    offset = wall_width // 2

    w = h = 2 * _set_size(config.grid.height) * cfg.ANTIALIAS_

    # Initialises the image with alpha layer - only circ maze visible.
    img = Image.new("RGBA", size=(w, h), color=(255, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draws the maze background
    radius = (config.grid.height - 1 + 0.75) * cfg.size * cfg.ANTIALIAS_
    shape = [(w // 2 - radius, h // 2 - radius), (w // 2 + radius, h // 2 + radius)]
    draw.ellipse(shape, fill=cfg.COLOUR_WHITE2, width=0)

    for row in range(1, config.grid.height):
        radius1 = (row + 0.75) * cfg.size * cfg.ANTIALIAS_
        radius0 = radius1 - cfg.size * cfg.ANTIALIAS_
        shape = [(w//2 - radius0, h//2 - radius0), (w//2 + radius0, h//2 + radius0)]

        theta = 360 / len(config.grid.cells[row])

        for col in range(len(config.grid.cells[row])):
            cell = config.grid.cells[row][col]

            if not cell.is_linked_to(cell.top):
                draw.arc(shape, start=(col * theta), end=((col + 1) * theta), fill=(0, 0, 0), width=wall_width)

            if not cell.is_linked_to(cell.left):
                c = np.cos(math.radians(theta) * col)
                s = np.sin(math.radians(theta) * col)
                rot_matrix = np.array(((c, -s), (s, c)))

                x0, y0 = np.dot(rot_matrix, (radius0 - 2*offset, 0))
                x1, y1 = np.dot(rot_matrix, (radius1, 0))

                draw.line((x0 + w//2, y0 + h//2, x1 + w//2, y1 + h//2), fill=(0, 0, 0), width=wall_width)

        if row == config.grid.height - 1:
            shape = [(w // 2 - radius1, h // 2 - radius1), (w // 2 + radius1, h // 2 + radius1)]
            draw.arc(shape, start=0, end=360, fill=(0, 0, 0), width=wall_width)

    img = img.resize((w // cfg.ANTIALIAS_, h // cfg.ANTIALIAS_), resample=Image.ANTIALIAS)

    return img


def _render_img() -> Image:
    """Calls the correct method depending on the type of the maze (Rect / Circ)."""
    if type(config.grid) == Grid:
        return _render_rect_grid_img()
    elif type(config.grid) == CircGrid:
        return _render_circ_grid_img()


def show_img() -> None:
    """
    Renders and shows the generated image of the maze in a pop-up window.

    **Note:**
        - To change the graphical representation of the maze use 'img_config()'.

    :return: None.
    """
    img = _render_img()
    img.show()


def save_img(filename: str) -> None:
    """
    Saves the generated image of the maze.

    **Note:**
        - The output file format is PNG by default.
        - To change the graphical representation of the maze use 'img_config()'.

    :param str filename: the name of the file (without extension) the generated image is saved to.
    :return: None.
    """
    img = _render_img()
    img.save("./" + filename + ".png", "PNG")
