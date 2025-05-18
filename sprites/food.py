import arcade
import math
from constants import FOOD_TYPES, SPRITE_SCALING

class Food(arcade.Sprite):
    def __init__(self, x, y, food_type, direction):
        """
        Initialize food projectile
        :param x: Starting x position
        :param y: Starting y position
        :param food_type: Type of food (tomato, watermelon, pie)
        :param direction: Direction to throw (up, down, left, right) or "custom" for direct velocity setting
        """
        # Set the appropriate image based on food type
        if food_type == "tomato":
            image = ":resources:images/items/star.png"  # Placeholder image
        elif food_type == "watermelon":
            image = ":resources:images/items/gemRed.png"  # Placeholder image
        else:  # pie
            image = ":resources:images/items/gemBlue.png"  # Placeholder image

        super().__init__(image, scale=SPRITE_SCALING)
        
        self.center_x = x
        self.center_y = y
        self.food_type = food_type
        self.properties = FOOD_TYPES[food_type]
        self.start_x = x
        self.start_y = y
        
        # Set velocity based on direction
        if direction == "custom":
            # Velocity will be set directly by the caller
            self.change_x = 0
            self.change_y = 0
        elif direction == "up":
            self.change_x = 0
            self.change_y = self.properties["speed"]
        elif direction == "down":
            self.change_x = 0
            self.change_y = -self.properties["speed"]
        elif direction == "left":
            self.change_x = -self.properties["speed"]
            self.change_y = 0
        elif direction == "right":
            self.change_x = self.properties["speed"]
            self.change_y = 0

    def update(self, delta_time: float = 1/60):
        """Update the food's position and check if it's exceeded its range."""
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Calculate distance traveled
        dx = self.center_x - self.start_x
        dy = self.center_y - self.start_y
        distance = math.sqrt(dx * dx + dy * dy)

        # Remove if exceeded maximum distance
        if distance > self.properties["distance"]:
            self.remove_from_sprite_lists()

        # Remove if out of bounds
        if (self.left < 0 or self.right > arcade.get_window().width or
            self.bottom < 0 or self.top > arcade.get_window().height):
            self.remove_from_sprite_lists() 