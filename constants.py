SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

NOTE_WIDTH = 60
NOTE_HEIGHT = 20
NOTE_SPEED = 300

HIT_Y = SCREEN_HEIGHT - 100
HIT_WINDOW = 30

# Keys for lanes 0..4
KEY_MAPPING = {
    0: "d",  # lane 0 (Red)
    1: "f",  # lane 1 (Green)
    2: "j",  # lane 2 (Blue)
    3: "k",  # lane 3 (Yellow)
    4: "l"   # lane 4 (Purple)
}

LANE_X = {
    0: 100,
    1: 200,
    2: 300,
    3: 400,
    4: 500
}

LANE_COLORS = {
    0: RED,
    1: GREEN,
    2: BLUE,
    3: YELLOW,
    4: PURPLE
}

HIT_SCORES = {
    "Perfect": 100,
    "Good": 50,
    "Miss": 0
}
