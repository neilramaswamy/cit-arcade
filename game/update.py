class Update():
    def __init__(self, dx = 0, dy = 0, stop: bool = False):
        self.dx = dx
        self.dy = dy
        self.stop = stop

    def __str__(self) -> str:
        return f"Update(dx={self.dx}, dy={self.dy}, stop={self.stop})"