import arcade
import math
from constants import ENEMY_SPEED, SPRITE_SCALING

class Enemy(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(":resources:images/animated_characters/zombie/zombie_idle.png",
                        scale=SPRITE_SCALING)
        self.center_x = x
        self.center_y = y
        self.speed = ENEMY_SPEED
        self.health = 50

    def chase_player(self, player_sprite):
        """Move towards the player."""
        # Calculate direction vector
        dx = player_sprite.center_x - self.center_x
        dy = player_sprite.center_y - self.center_y
        
        # Normalize the direction vector
        distance = math.sqrt(dx * dx + dy * dy)
        if distance > 0:
            dx = dx / distance
            dy = dy / distance
            
            # Set movement speed
            self.change_x = dx * self.speed
            self.change_y = dy * self.speed
        else:
            self.change_x = 0
            self.change_y = 0

    def update(self, delta_time: float = 1/60):
        """Update the enemy's position."""
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Keep enemy in bounds
        if self.left < 0:
            self.left = 0
        elif self.right > arcade.get_window().width:
            self.right = arcade.get_window().width

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > arcade.get_window().height:
            self.top = arcade.get_window().height 