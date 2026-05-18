from pygame import image, transform


class Pacgum:
    """class for pacgum"""

    def __init__(self, points: int, coord: tuple[int, int], skin: str, cell_width, cell_height):
        self.points: int = points
        self.visible: bool = True
        self.coord: tuple[int, int] = coord
        self.skin = transform.scale(
            image.load(skin),
            (cell_width, cell_height))
        self.pixel_x = float(coord[0])
        self.pixel_y = float(coord[1])


class SuperPacgum:
    """class for super pacgum"""

    def __init__(self, points: int, coord: tuple[int, int], skin: str, cell_width, cell_height):
        self.points: int = points
        self.visible: bool = True
        self.coord: tuple[int, int] = coord
        self.skin = transform.scale(
            image.load(skin),
            (cell_width, cell_height),
        )
        self.pixel_x = float(coord[0])
        self.pixel_y = float(coord[1])
