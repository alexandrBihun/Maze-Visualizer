class Tile():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.isWall = False

    def __str__(self):
        return f"x:{self.x},y:{self.y},iW:{self.isWall}\n"