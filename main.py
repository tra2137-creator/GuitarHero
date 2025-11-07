import pygame
import sys
import time
from constants import *
from game import Game

# --- Pygame setup ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Guitar Hero")
clock = pygame.time.Clock()

# --- Fonts ---
font = pygame.font.SysFont("Arial", 30)
big_font = pygame.font.SysFont("Arial", 50)
title_font = pygame.font.SysFont("Arial", 60, bold=True)

# --- Game object ---
game = Game()

# --- Notes chart example ---
note_chart = [
    {"time": 1.0, "key": "R"},
    {"time": 1.5, "key": "G"},
    {"time": 2.0, "key": "B"},
    {"time": 2.5, "key": "Y"},
    {"time": 3.0, "key": "P"},
    {"time": 3.5, "key": "R"},
    {"time": 4.0, "key": "G"},
]
game.load_notes(note_chart)

# --- Game states ---
STATE_START = "start_screen"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "end_screen"
game_state = STATE_START
hit_feedback = ""
feedback_timer = 0

# --- Draw start screen ---
def draw_start_screen():
    screen.fill(BLACK)
    title = title_font.render("Guitar Hero", True, WHITE)
    song = big_font.render("Eye of the Tiger", True, WHITE)
    info = font.render("Press ENTER to Start", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//2 - 100))
    screen.blit(song, (SCREEN_WIDTH//2 - song.get_width()//2, SCREEN_HEIGHT//2 - 40))
    screen.blit(info, (SCREEN_WIDTH//2 - info.get_width()//2, SCREEN_HEIGHT//2 + 40))
    pygame.display.flip()

# --- Draw hollow hit zones ---
def draw_hit_zone():
    for lane_index, x in LANE_X.items():
        pygame.draw.circle(
            screen,
            LANE_COLORS[lane_index],
            (x, HIT_Y),
            NOTE_RADIUS,
            4  # thickness makes it hollow
        )

# --- Draw end screen ---
def draw_end_screen():
    screen.fill(BLACK)
    title = title_font.render("Song Complete!", True, WHITE)
    score_text = big_font.render(f"Score: {game.score}", True, WHITE)
    combo_text = font.render(f"Max Combo: {game.max_combo}", True, WHITE)
    hits_text = font.render(f"Total Hits: {game.total_hits}", True, WHITE)
    misses_text = font.render(f"Total Misses: {game.total_misses}", True, WHITE)
    restart_text = font.render("Press ENTER to Restart", True, WHITE)

    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 80))
    screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 200))
    screen.blit(combo_text, (SCREEN_WIDTH//2 - combo_text.get_width()//2, 280))
    screen.blit(hits_text, (SCREEN_WIDTH//2 - hits_text.get_width()//2, 320))
    screen.blit(misses_text, (SCREEN_WIDTH//2 - misses_text.get_width()//2, 360))
    screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 480))
    pygame.display.flip()

# --- Main loop ---
running = True
while running:
    delta_time = clock.tick(FPS) / 1000

    # --- Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if game_state == STATE_START and event.key == pygame.K_RETURN:
                game.start()
                game_state = STATE_PLAYING

            elif game_state == STATE_PLAYING:
                if event.key == pygame.K_p:
                    game.toggle_pause()
                else:
                    result = game.handle_input(event.unicode)
                    if result:
                        hit_feedback = result
                        feedback_timer = 0.5

            elif game_state == STATE_GAME_OVER and event.key == pygame.K_RETURN:
                game.restart()
                game_state = STATE_START
                hit_feedback = ""
                feedback_timer = 0

    # --- Draw screens based on state ---
    if game_state == STATE_START:
        draw_start_screen()
        continue
    elif game_state == STATE_GAME_OVER:
        draw_end_screen()
        continue

    # --- Update game ---
    game.update()
    if all(note.hit for note in game.notes):
        game_state = STATE_GAME_OVER

    # --- Draw ---
    screen.fill(BLACK)
    draw_hit_zone()  # hollow circles
    game.draw(screen)

    # --- Scoreboard ---
    score_text = font.render(f"Score: {game.score}", True, WHITE)
    combo_text = font.render(f"Combo: {game.combo}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(combo_text, (10, 50))

    # --- Feedback ---
    if feedback_timer > 0:
        feedback_surface = big_font.render(hit_feedback, True, WHITE)
        screen.blit(feedback_surface, (SCREEN_WIDTH//2 - feedback_surface.get_width()//2, HIT_Y - 50))
        feedback_timer -= delta_time

    pygame.display.flip()

pygame.quit()
sys.exit()
