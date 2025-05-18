import arcade
from constants import PLAYER_SPEED, SPRITE_SCALING

class Player(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(":resources:images/animated_characters/robot/robot_idle.png", 
                        scale=SPRITE_SCALING)
        self.center_x = x
        self.center_y = y
        self.speed = PLAYER_SPEED
        self.change_x = 0
        self.change_y = 0
        self.health = 100

    def update(self, delta_time: float = 1/60):
        # Move the player
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Keep player in bounds
        if self.left < 0:
            self.left = 0
        elif self.right > arcade.get_window().width:
            self.right = arcade.get_window().width

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > arcade.get_window().height:
            self.top = arcade.get_window().height 