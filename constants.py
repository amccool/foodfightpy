import arcade

# Window constants
SCREEN_WIDTH = 1024  # Made wider for cafeteria
SCREEN_HEIGHT = 768  # Made taller for cafeteria
SCREEN_TITLE = "Food Fight"

# Scaling
SPRITE_SCALING = 0.5

# Player movement speed (pixels per frame)
PLAYER_SPEED = 5

# Enemy constants
ENEMY_COUNT = 3
ENEMY_SPEED = 2.25  # Reduced by 25% from original 3

# Food constants
FOOD_TYPES = {
    "tomato": {"speed": 16, "damage": 10, "distance": 300},
    "watermelon": {"speed": 10, "damage": 25, "distance": 200},
    "pie": {"speed": 12, "damage": 15, "distance": 250}
}

# Cafeteria layout constants
TABLE_SCALING = 0.75
KITCHEN_WIDTH = SCREEN_WIDTH // 4  # Kitchen area takes up 1/4 of the screen

# Player controls
PLAYER_CONTROLS = {
    "up": arcade.key.W,
    "down": arcade.key.S,
    "left": arcade.key.A,
    "right": arcade.key.D,
    "throw_up": arcade.key.I,
    "throw_down": arcade.key.K,
    "throw_left": arcade.key.J,
    "throw_right": arcade.key.L
} 