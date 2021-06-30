"""Maze visualizer.

This module provides a function ``visualize`` for visualizing maze traversal when given
a list of maze states. Each state is a 2D list of tile values.

Example:
    The ``visualize`` function can be used like this:
    ::
        states = [
            [
                [0.1, 0.2, 0.3],
                [0.6, 0.5, 0.4],
                [0.7, 0.8, 0.9],
            ],
            [
                ["W", "W", "W"],
                ["T", "T", "T"],
                ["N", "N", "N"],
            ],
        ]

        visualize(states, "path/to/file.gif")

"""

from pathlib import Path
from typing import Callable, Iterable, List, Union

import numpy as np
from PIL import Image


__all__ = ["visualize"]


def _map(value: Union[float, str]) -> List[int]:
    """Maps a value to a color.

    Args:
        value (Union[float, str]): A value to convert to a color.

    Raises:
        ValueError: If a value cannot be mapped to a color.

    Returns:
        List[int]: A color in [R, G, B] form.
    """
    colors = {"W": [255, 255, 255], "T": [255, 0, 0], "N": [0, 0, 255]}

    if isinstance(value, float) and 0 <= value <= 1:
        return [0, round(255 * value), 0]
    elif value in colors:
        return colors[value]

    raise ValueError('Tile state must be "W", "T", "N", or a float between 0 and 1.')


def visualize(
    matrices: Iterable[Iterable[Iterable[Union[float, str]]]],
    path: Path,
    color: Callable = _map,
    delay: float = 0.5,
):
    """Creates a GIF based on a list of maze states.

    Args:
        matrices (Iterable[Iterable[Iterable[Union[float, str]]]]): A list of 2D
            matrices representing maze states to render as a GIF.
        path (Path): The path to save the GIF to.
        color (Callable, optional): The function to use when mapping tiles values to
            colors.
        delay (float, optional): The number of seconds between each frame of the GIF.
            Defaults to 0.5.
    """
    frames = []

    for matrix in matrices:
        m = np.zeros((len(matrix), len(matrix[0]), 3), dtype=np.uint8)
        for i, row in enumerate(matrix):
            for j, tile in enumerate(row):
                m[i, j] = color(tile)
        frames.append(Image.fromarray(m, "RGB"))

    frames[0].save(
        fp=path,
        format="GIF",
        append_images=frames[1:],
        save_all=True,
        duration=delay * 1000,
        optimize=False,
    )
