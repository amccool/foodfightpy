# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import arcade
import random
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE,
    ENEMY_COUNT, PLAYER_CONTROLS, FOOD_TYPES,
    KITCHEN_WIDTH
)
from sprites.player import Player
from sprites.enemy import Enemy
from sprites.food import Food
from sprites.table import Table

class FoodFight(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
        
        # Initialize the window
        arcade.set_background_color(arcade.color.LIGHT_GRAY)  # Cafeteria floor color
        
        # Sprite lists
        self.player_list = None
        self.enemy_list = None
        self.food_list = None
        self.table_list = None
        self.wall_list = None  # For kitchen walls
        
        # Set up the player
        self.player = None
        
        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        
        # Track throw keys
        self.throw_up_pressed = False
        self.throw_down_pressed = False
        self.throw_left_pressed = False
        self.throw_right_pressed = False
        
        # Throw cooldown tracking
        self.throw_cooldown = 0
        self.THROW_COOLDOWN_TIME = 0.2  # Time between throws in seconds
        
        # Current food type
        self.current_food = "tomato"

    def setup(self):
        """ Set up the game and initialize the variables. """
        # Create the sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.food_list = arcade.SpriteList()
        self.table_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Create kitchen area (right side of screen)
        self.create_kitchen()
        
        # Create cafeteria tables
        self.create_tables()

        # Set up the player (start in dining area)
        self.player = Player(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.player_list.append(self.player)

        # Create the enemies (start in kitchen area)
        self.create_enemies()

    def create_kitchen(self):
        """Create the kitchen area with walls."""
        # Create kitchen counter (vertical wall separating kitchen from dining area)
        for y in range(0, SCREEN_HEIGHT, 32):
            wall = arcade.Sprite(":resources:images/tiles/stoneCenter.png", 0.5)
            wall.center_x = SCREEN_WIDTH - KITCHEN_WIDTH
            wall.center_y = y
            self.wall_list.append(wall)
            
        # Add serving windows (gaps in the wall)
        serving_windows = [SCREEN_HEIGHT // 4, SCREEN_HEIGHT * 3 // 4]
        for window_y in serving_windows:
            for i in range(3):  # Remove 3 wall segments for each window
                for wall in self.wall_list:
                    if (abs(wall.center_y - (window_y + (i-1)*32)) < 16 and 
                        abs(wall.center_x - (SCREEN_WIDTH - KITCHEN_WIDTH)) < 16):
                        wall.remove_from_sprite_lists()

    def create_tables(self):
        """Create the cafeteria table layout."""
        # Create 3 rows of tables
        for row in range(3):
            y = (row + 1) * (SCREEN_HEIGHT // 4)
            # Create 3 tables per row
            for col in range(3):
                x = (col + 1) * ((SCREEN_WIDTH - KITCHEN_WIDTH) // 4)
                table = Table(x, y)
                self.table_list.append(table)

    def create_enemies(self):
        """Create enemies in the kitchen area."""
        for i in range(ENEMY_COUNT):
            # Position enemies in the kitchen area
            x = random.randrange(SCREEN_WIDTH - KITCHEN_WIDTH + 50, SCREEN_WIDTH - 50)
            y = random.randrange(50, SCREEN_HEIGHT - 50)
            enemy = Enemy(x, y)
            self.enemy_list.append(enemy)

    def on_draw(self):
        """ Render the screen. """
        self.clear()
        
        # Draw all the sprites
        self.wall_list.draw()
        self.table_list.draw()
        self.player_list.draw()
        self.enemy_list.draw()
        self.food_list.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        # Movement
        if key == PLAYER_CONTROLS["up"]:
            self.up_pressed = True
            self.update_player_velocity()
        elif key == PLAYER_CONTROLS["down"]:
            self.down_pressed = True
            self.update_player_velocity()
        elif key == PLAYER_CONTROLS["left"]:
            self.left_pressed = True
            self.update_player_velocity()
        elif key == PLAYER_CONTROLS["right"]:
            self.right_pressed = True
            self.update_player_velocity()
        
        # Throwing food
        elif key == PLAYER_CONTROLS["throw_up"]:
            self.throw_up_pressed = True
        elif key == PLAYER_CONTROLS["throw_down"]:
            self.throw_down_pressed = True
        elif key == PLAYER_CONTROLS["throw_left"]:
            self.throw_left_pressed = True
        elif key == PLAYER_CONTROLS["throw_right"]:
            self.throw_right_pressed = True
        
        # Switch food types (1, 2, 3 keys)
        elif key == arcade.key.KEY_1:
            self.current_food = "tomato"
        elif key == arcade.key.KEY_2:
            self.current_food = "watermelon"
        elif key == arcade.key.KEY_3:
            self.current_food = "pie"

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == PLAYER_CONTROLS["up"]:
            self.up_pressed = False
            self.update_player_velocity()
        elif key == PLAYER_CONTROLS["down"]:
            self.down_pressed = False
            self.update_player_velocity()
        elif key == PLAYER_CONTROLS["left"]:
            self.left_pressed = False
            self.update_player_velocity()
        elif key == PLAYER_CONTROLS["right"]:
            self.right_pressed = False
            self.update_player_velocity()
        elif key == PLAYER_CONTROLS["throw_up"]:
            self.throw_up_pressed = False
        elif key == PLAYER_CONTROLS["throw_down"]:
            self.throw_down_pressed = False
        elif key == PLAYER_CONTROLS["throw_left"]:
            self.throw_left_pressed = False
        elif key == PLAYER_CONTROLS["throw_right"]:
            self.throw_right_pressed = False

    def update_player_velocity(self):
        """Calculate speed based on the keys pressed."""
        self.player.change_x = 0
        self.player.change_y = 0

        # Calculate the base movement vector
        dx = 0
        dy = 0
        
        if self.up_pressed and not self.down_pressed:
            dy = 1
        elif self.down_pressed and not self.up_pressed:
            dy = -1

        if self.left_pressed and not self.right_pressed:
            dx = -1
        elif self.right_pressed and not self.left_pressed:
            dx = 1

        # If moving diagonally, normalize the speed
        if dx != 0 and dy != 0:
            # Normalize diagonal movement (multiply by approximately 0.707)
            dx *= 0.7071067811865476
            dy *= 0.7071067811865476

        # Apply the speed
        self.player.change_x = dx * self.player.speed
        self.player.change_y = dy * self.player.speed

    def throw_food(self, dx, dy):
        """Create and throw a food projectile with a direction vector."""
        if dx == 0 and dy == 0:
            return
            
        # Normalize the direction vector
        length = (dx * dx + dy * dy) ** 0.5
        dx = dx / length
        dy = dy / length
        
        food = Food(
            self.player.center_x,
            self.player.center_y,
            self.current_food,
            "custom"  # We'll need to update the Food class to handle custom directions
        )
        
        # Set the food's velocity directly
        food_speed = FOOD_TYPES[self.current_food]["speed"]
        food.change_x = dx * food_speed
        food.change_y = dy * food_speed
        
        self.food_list.append(food)

    def on_update(self, delta_time):
        """ Movement and game logic """
        # Update throw cooldown
        self.throw_cooldown = max(0, self.throw_cooldown - delta_time)
        
        # Handle continuous throwing if any throw keys are pressed
        if self.throw_cooldown <= 0:
            # Calculate throw direction vector
            throw_dx = 0
            throw_dy = 0
            
            if self.throw_up_pressed and not self.throw_down_pressed:
                throw_dy = 1
            elif self.throw_down_pressed and not self.throw_up_pressed:
                throw_dy = -1
                
            if self.throw_left_pressed and not self.throw_right_pressed:
                throw_dx = -1
            elif self.throw_right_pressed and not self.throw_left_pressed:
                throw_dx = 1
            
            # If any throw keys are pressed, throw food
            if throw_dx != 0 or throw_dy != 0:
                self.throw_food(throw_dx, throw_dy)
                self.throw_cooldown = self.THROW_COOLDOWN_TIME

        # Update all sprites
        self.player_list.update()
        self.enemy_list.update()
        self.food_list.update()

        # Check for collisions between player and walls/tables
        if arcade.check_for_collision_with_list(self.player, self.wall_list):
            # Move player back to previous position
            self.player.center_x -= self.player.change_x
            self.player.center_y -= self.player.change_y

        if arcade.check_for_collision_with_list(self.player, self.table_list):
            # Move player back to previous position
            self.player.center_x -= self.player.change_x
            self.player.center_y -= self.player.change_y

        # Update enemies to chase player
        for enemy in self.enemy_list:
            prev_x = enemy.center_x
            prev_y = enemy.center_y
            enemy.chase_player(self.player)
            enemy.update()
            
            # Check for collisions with tables and walls
            if (arcade.check_for_collision_with_list(enemy, self.wall_list) or
                arcade.check_for_collision_with_list(enemy, self.table_list)):
                # Move enemy back to previous position
                enemy.center_x = prev_x
                enemy.center_y = prev_y

        # Check for collisions between food and enemies/tables
        for food in self.food_list:
            # Check collision with tables
            if arcade.check_for_collision_with_list(food, self.table_list):
                food.remove_from_sprite_lists()
                continue
                
            # Check collision with walls
            if arcade.check_for_collision_with_list(food, self.wall_list):
                food.remove_from_sprite_lists()
                continue
                
            # Check collision with enemies
            hit_list = arcade.check_for_collision_with_list(food, self.enemy_list)
            for enemy in hit_list:
                enemy.health -= FOOD_TYPES[food.food_type]["damage"]
                food.remove_from_sprite_lists()
                
                if enemy.health <= 0:
                    enemy.remove_from_sprite_lists()

        # Check for collisions between player and enemies
        hit_list = arcade.check_for_collision_with_list(self.player, self.enemy_list)
        if len(hit_list) > 0:
            self.player.health -= 1
            if self.player.health <= 0:
                # Game over logic would go here
                pass

def main():
    """ Main function """
    window = FoodFight()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
