from __future__ import annotations


import math
from PIL import Image, ImageDraw

from src.pymazegen.maze import Grid, CircGrid
import src.pymazegen.presenter.config as cfg
import src.pymazegen.algos.config as config


def _set_size(size: int) -> int:
    return size * cfg.cell_size + (size + 1) * cfg.wall_thickness


# TODO: wall_thickness not working properly for animation
def _render_rect_grid_anim() -> list[Image]:
    w = _set_size(config.grid.width)
    h = _set_size(config.grid.height)

    img = Image.new("RGB", size=(w, h), color=cfg.COLOUR_BLACK)
    draw = ImageDraw.Draw(img)

    imgs = []
    for coords in config.build_steps:
        crow, ccol, nrow, ncol, col = coords

        if col == 'w':
            draw.rectangle((ccol * cfg.size + cfg.wall_thickness + (-cfg.wall_thickness, 0)[ccol <= ncol],
                            crow * cfg.size + cfg.wall_thickness + (-cfg.wall_thickness, 0)[crow <= nrow],
                            (ccol + 1) * cfg.size - cfg.wall_thickness // 2 + (0, cfg.wall_thickness)[ccol < ncol],
                            (crow + 1) * cfg.size - cfg.wall_thickness // 2 + (0, cfg.wall_thickness)[crow < nrow]),
                           fill=cfg.COLOUR_WHITE2)
        else:
            draw.rectangle((min(ccol, ncol) * cfg.size + cfg.wall_thickness,
                            min(crow, nrow) * cfg.size + cfg.wall_thickness,
                            (max(ccol, ncol) + 1) * cfg.size - cfg.wall_thickness // 2,
                            (max(crow, nrow) + 1) * cfg.size - cfg.wall_thickness // 2), fill=cfg.COLOUR_RED)

        imgs.append(img.copy())
    return imgs


def _render_circ_grid_anim() -> list[Image]:
    imgs = []

    wall_width = cfg.wall_thickness * cfg.ANTIALIAS_

    w = h = 2 * _set_size(config.grid.height) * cfg.ANTIALIAS_

    # Initialises the image with alpha layer - only circ maze visible.
    img = Image.new("RGBA", size=(w, h), color=(255, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draws the maze background
    radius = (config.grid.height - 1 + 0.75) * cfg.size * cfg.ANTIALIAS_
    shape = [(w // 2 - radius, h // 2 - radius), (w // 2 + radius, h // 2 + radius)]
    draw.ellipse(shape, fill=cfg.COLOUR_BLACK, width=0)

    # Memorizes all possible geometry settings to draw the cells - computed once, used multiple times
    theta: list[float] = []
    alpha: list[int] = []
    shape_: list[tuple[int, int, int, int]] = []
    for row in range(config.grid.height):
        radius_ = (row + 0.75) * cfg.size * cfg.ANTIALIAS_
        theta.append(360 / len(config.grid.cells[row]))

        circumf_ = radius_ * 2 * math.pi
        alpha.append((360 * (wall_width / 2)) / circumf_)

        shape_.append((w // 2 - radius_ + wall_width, h // 2 - radius_ + wall_width,
                       w // 2 + radius_ - wall_width, h // 2 + radius_ - wall_width))

    #TODO BEGIN delete / rewrite
    for coords in config.build_steps:
        crow, ccol, nrow, ncol, col = coords

        # r = max(crow, nrow)
        #TODO get rid of red lines
        if col == 'w':
            if crow == 0:
                draw.ellipse(shape_[crow], fill=cfg.COLOUR_WHITE2, width=0)
            else:
                if crow < nrow:
                    shape_temp = (shape_[crow][0] - wall_width, shape_[crow][1] - wall_width,
                                  shape_[crow][2] + wall_width, shape_[crow][3] + wall_width)
                else:
                    shape_temp = shape_[crow]
                draw.arc(shape_temp, start=(ccol * theta[crow]) + (-1, alpha[crow])[crow != nrow or ncol > ccol],
                         end=((ccol + 1) * theta[crow]) + (1, -alpha[crow])[crow != nrow or ncol < ccol],
                         fill=cfg.COLOUR_WHITE2, width=cfg.size * cfg.ANTIALIAS_ - wall_width * (crow == nrow))
        elif crow == nrow:
            start_ = (min(ccol, ncol), max(ccol, ncol))[abs(ccol - ncol) > 1] * theta[crow] + alpha[crow]
            end_ = (max(ccol, ncol) + 1, min(ccol, ncol) + 1)[abs(ccol - ncol) > 1] * theta[crow] - alpha[crow]
            draw.arc(shape_[crow], start=start_, end=end_,
                     fill=cfg.COLOUR_RED, width=cfg.size * cfg.ANTIALIAS_ - wall_width)
        # elif ccol == ncol:
        else:
            for r, c in ((crow, ccol), (nrow, ncol)):
                if r == 0:
                    draw.ellipse(shape_[r], fill=cfg.COLOUR_RED, width=0)
                else:
                    width_ = cfg.size * cfg.ANTIALIAS_ - wall_width * (1, 0)[r - crow > 0 or r - nrow > 0]
                    draw.arc(shape_[r], start=(c * theta[r]) + alpha[r], end=((c + 1) * theta[r]) - alpha[r],
                             fill=cfg.COLOUR_RED, width=width_)

    # TODO END delete / rewrite

        img_rs = img.resize((w // cfg.ANTIALIAS_, h // cfg.ANTIALIAS_), resample=Image.ANTIALIAS)
        imgs.append(img_rs)

    img.save("./anim.png", "PNG")
    return imgs


def _render_anim() -> None:
    if type(config.grid) == Grid:
        cfg.imgs = _render_rect_grid_anim()
    elif type(config.grid) == CircGrid:
        cfg.imgs = _render_circ_grid_anim()


def save_anim(filename: str, mspf: int = 300) -> None:
    """
    Renders and saves an animation of the building process of the maze.
    Creates a visual representation of the selected mazegen algorithm.

    .. note::
        * The output file format is GIF by default.
        * To change the graphical representation of the maze use 'img_config()'.

    :param filename: the name of the file (without extension) the generated animation is saved to;
    :param mspf: milliseconds per frame; the duration of one frame in milliseconds.
    :return: None.
    """
    _render_anim()
    cfg.imgs[0].save("./" + filename + '.gif', save_all=True, append_images=cfg.imgs[1:], optimize=False, duration=mspf)
