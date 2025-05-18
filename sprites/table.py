import arcade
from constants import TABLE_SCALING

class Table(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(":resources:images/tiles/boxCrate_double.png",  # Using crate as table for now
                        scale=TABLE_SCALING)
        self.center_x = x
        self.center_y = y
        self.health = 1000  # Tables are very durable 