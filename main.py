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

# --- Initialize mixer for music ---
pygame.mixer.init()
pygame.mixer.music.load("assets/sounds/Survivor - Eye Of The Tiger (Lyrics).mp3")
pygame.mixer.music.set_volume(0.7)  # adjust volume 0.0 - 1.0


# --- Fonts ---
font = pygame.font.SysFont("Consolas", 28)
big_font = pygame.font.SysFont("Consolas", 50, bold=True)
title_font = pygame.font.SysFont("Arial Black", 60, bold=True)

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
    {"time": 4.5, "key": "B"},
    {"time": 5.0, "key": "Y"},
    {"time": 5.5, "key": "P"},
    {"time": 6.0, "key": "R"},
    {"time": 6.3, "key": "G"},
    {"time": 6.6, "key": "B"},
    {"time": 7.0, "key": "Y"},
    {"time": 7.3, "key": "P"},
    {"time": 7.6, "key": "R"},
    {"time": 8.0, "key": "G"},
    {"time": 8.4, "key": "B"},
    {"time": 8.8, "key": "Y"},
    {"time": 9.2, "key": "P"},
    {"time": 9.6, "key": "R"},
    {"time": 10.0, "key": "G"},
    {"time": 10.5, "key": "B"},
    {"time": 11.0, "key": "Y"},
    {"time": 11.5, "key": "P"},
    {"time": 12.0, "key": "R"},
    {"time": 12.5, "key": "G"},
    {"time": 13.0, "key": "B"},
    {"time": 13.5, "key": "Y"},
    {"time": 14.0, "key": "P"},
    {"time": 14.5, "key": "R"},
    {"time": 15.0, "key": "G"},
    {"time": 15.5, "key": "B"},
    {"time": 16.0, "key": "Y"},
    {"time": 16.5, "key": "P"},
    {"time": 17.0, "key": "R"},
    {"time": 17.5, "key": "G"},
    {"time": 18.0, "key": "B"},
    {"time": 18.5, "key": "Y"},
    {"time": 19.0, "key": "P"},
    {"time": 19.5, "key": "R"},
    {"time": 20.0, "key": "G"},
]
game.load_notes(note_chart)

# --- Game states ---
STATE_START = "start_screen"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "end_screen"
game_state = STATE_START
hit_feedback = ""
feedback_timer = 0
feedback_y_offset = 0

# --- Draw start screen ---
def draw_start_screen():
    screen.fill((20, 20, 20))
    title = title_font.render("Guitar Hero", True, WHITE)
    song = big_font.render("Eye of the Tiger", True, WHITE)
    info = font.render("Press ENTER to Start", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//2 - 100))
    screen.blit(song, (SCREEN_WIDTH//2 - song.get_width()//2, SCREEN_HEIGHT//2 - 20))
    screen.blit(info, (SCREEN_WIDTH//2 - info.get_width()//2, SCREEN_HEIGHT//2 + 60))
    pygame.display.flip()

# --- Draw hollow hit zones with glow ---
def draw_hit_zone():
    for lane_index, x in LANE_X.items():
        # Glow circle
        pygame.draw.circle(screen, (*LANE_COLORS[lane_index], 80), (x, HIT_Y), NOTE_RADIUS+12, 6)
        # Hollow circle
        pygame.draw.circle(screen, LANE_COLORS[lane_index], (x, HIT_Y), NOTE_RADIUS, 4)

# --- Draw end screen ---
def draw_end_screen():
    screen.fill((20, 20, 20))
    title = title_font.render("Song Complete!", True, WHITE)
    score_text = big_font.render(f"Score: {game.score}", True, WHITE)
    combo_text = font.render(f"Max Combo: {game.max_combo}", True, WHITE)
    hits_text = font.render(f"Total Hits: {game.total_hits}", True, WHITE)
    misses_text = font.render(f"Total Misses: {game.total_misses}", True, WHITE)
    restart_text = font.render("Press ENTER to Restart", True, WHITE)

    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 60))
    screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 180))
    screen.blit(combo_text, (SCREEN_WIDTH//2 - combo_text.get_width()//2, 260))
    screen.blit(hits_text, (SCREEN_WIDTH//2 - hits_text.get_width()//2, 320))
    screen.blit(misses_text, (SCREEN_WIDTH//2 - misses_text.get_width()//2, 360))
    screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 440))
    pygame.display.flip()

# --- Animate feedback ---
def draw_feedback():
    global feedback_y_offset
    if feedback_timer > 0:
        feedback_surface = big_font.render(hit_feedback, True, WHITE)
        y_pos = HIT_Y - 60 - feedback_y_offset
        screen.blit(feedback_surface, (SCREEN_WIDTH//2 - feedback_surface.get_width()//2, y_pos))
        feedback_y_offset += 60 * (1/FPS)  # float upward

# --- Main loop ---
running = True
while running:
    delta_time = clock.tick(FPS) / 1.0

    # --- Event handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            # Start screen
            if game_state == STATE_START and event.key == pygame.K_RETURN:
                game.start()
                game_state = STATE_PLAYING
                pygame.mixer.music.play()

            # Playing screen
            elif game_state == STATE_PLAYING:
                if event.key == pygame.K_p:
                    game.toggle_pause()
                else:
                    result = game.handle_input(event.unicode)
                    if result:
                        hit_feedback = result
                        feedback_timer = 0.5
                        feedback_y_offset = 0

            # Game over screen
            elif game_state == STATE_GAME_OVER and event.key == pygame.K_RETURN:
                pygame.mixer.music.stop()
                game.restart()
                hit_feedback = ""
                feedback_timer = 0
                feedback_y_offset = 0
                game_state = STATE_PLAYING
                pygame.mixer.music.play()

    # --- Update game ---
    if game_state == STATE_PLAYING:
        game.update()
        # End the song if all notes are hit
        if all(note.hit for note in game.notes):
            game_state = STATE_GAME_OVER
            pygame.mixer.music.stop()

    # --- Draw ---
    screen.fill((20, 20, 20))
    if game_state == STATE_START:
        draw_start_screen()
    elif game_state == STATE_PLAYING:
        draw_hit_zone()
        game.draw(screen)
        draw_feedback()
        # Scoreboard
        score_text = font.render(f"Score: {game.score}", True, WHITE)
        combo_text = font.render(f"Combo: {game.combo}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(combo_text, (10, 50))
    elif game_state == STATE_GAME_OVER:
        draw_end_screen()

    pygame.display.flip()

pygame.quit()
sys.exit()
