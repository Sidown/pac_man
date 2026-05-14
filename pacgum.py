class Pacgum:
    def __init__(self, points: int, coord: tuple[int], skin: str):
        self.points: int = points
        self.visible: bool = True
        self.coord: tuple[int] = coord
        self.skin = skin
        self.pixel_x = float(coord[0])
        self.pixel_y = float(coord[1])


class SuperPacgum:
    def __init__(self, points: int, coord: tuple[int], skin: str):
        self.points: int = points
        self.visible: bool = True
        self.coord: tuple[int] = coord
        self.skin = skin
        self.pixel_x = float(coord[0])
        self.pixel_y = float(coord[1])