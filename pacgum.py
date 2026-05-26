from pygame import image, transform, Surface


class Pacgum:
    """class for pacgum"""

    def __init__(self, points: int, coord: tuple[int, int],
                 skin: str, cell_width: float, cell_height: float) -> None:
        """
        initialise the pacgum at a given maze cell
        arguments:
        points -> points gained when pacgum eaten
        coord -> x,y coord of the pacgum in the maze
        skin -> path to the skin file
        cell_width -> cell width in pixels
        cell_heigth -> cell height in pixels
        """
        self.points: int = points
        self.visible: bool = True
        self.coord: tuple[int, int] = coord
        self.skin: Surface = transform.scale(
            image.load(skin),
            (cell_width, cell_height))
        self.pixel_x: float = float(coord[0])
        self.pixel_y: float = float(coord[1])


class SuperPacgum:
    """class for super pacgum"""

    def __init__(self, points: int, coord: tuple[int, int],
                 skin: str, cell_width: float, cell_height: float) -> None:
        """
        Initialise super pacgums at a given corner
        arguments:
        points -> points gained when super pacgums eaten
        coord -> x,y coord of the super pacgum in the maze
        skin -> path to the skin file
        cell_width -> width of the cell in pixels
        cell_height -> height of the cell in pixels
        """
        self.points: int = points
        self.visible: bool = True
        self.coord: tuple[int, int] = coord
        self.skin: Surface = transform.scale(
            image.load(skin),
            (cell_width, cell_height),
        )
        self.pixel_x: float = float(coord[0])
        self.pixel_y: float = float(coord[1])
