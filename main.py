import pygame
import sys
import time
from constants import *
from game import Game
beat_recording = False
beat_times = []

song_start_time = None
SONG_LENGTH = 4 * 60 + 2   # 4:02


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
    # --- INTRO HEARTBEAT (8 beats) ---
    {"time": 1.515, "key": "R"},
    {"time": 2.062, "key": "R"},
    {"time": 2.666, "key": "R"},
    {"time": 3.176, "key": "R"},
    {"time": 3.715, "key": "R"},
    {"time": 4.259, "key": "R"},
    {"time": 4.784, "key": "R"},
    {"time": 5.361, "key": "R"},
    {"time": 5.884, "key": "R"},
    {"time": 6.423, "key": "R"},
    {"time": 6.997, "key": "R"},
    {"time": 7.503, "key": "R"},
    {"time": 8.029, "key": "R"},
    {"time": 8.029, "key": "B"},
    {"time": 8.029, "key": "P", "hold_duration": 1.0}, 

    {"time": 9.246, "key": "R"},
    {"time": 9.246, "key": "B"},
    {"time": 9.246, "key": "P"},

    {"time": 9.607, "key": "G"},
    {"time": 9.607, "key": "Y"},

    {"time": 9.992, "key": "R"},
    {"time": 9.992, "key": "B"},
    {"time": 9.992, "key": "P"},

    {"time": 11.236, "key": "R"},
    {"time": 11.236, "key": "P"},

    {"time": 11.708, "key": "G"}, #down
    {"time": 11.708, "key": "Y"},

    {"time": 12.166, "key": "R"},#UP
    {"time": 12.166, "key": "B"},
    {"time": 12.166, "key": "P"},

    {"time": 13.530, "key": "R"}, #up
    {"time": 13.530, "key": "B"},
    {"time": 13.530, "key": "P"},

    {"time": 13.970, "key": "G"}, #down
    {"time": 13.970, "key": "Y"},

    {"time": 14.409, "key": "B"}, #double down
    {"time": 14.409, "key": "Y"},
    {"time": 14.409, "key": "P"},

    {"time": 17.075, "key": "R"}, #up
    {"time": 17.075, "key": "B"},
    {"time": 17.075, "key": "P"},

    {"time": 18.014, "key": "R"}, #up
    {"time": 18.014, "key": "B"},
    {"time": 18.014, "key": "P"},

    {"time": 18.432, "key": "G"}, #down
    {"time": 18.432, "key": "Y"},

    {"time": 18.818, "key": "R"}, #up
    {"time": 18.818, "key": "B"},
    {"time": 18.818, "key": "P"},

    {"time": 20.306, "key": "R"}, #up
    {"time": 20.306, "key": "B"},
    {"time": 20.306, "key": "P"},

    {"time": 20.844, "key": "G"}, #down
    {"time": 20.844, "key": "Y"},

    {"time": 21.267, "key": "R"}, #up
    {"time": 21.267, "key": "B"},
    {"time": 21.267, "key": "P"},

    {"time": 22.589, "key": "R"}, #up
    {"time": 22.589, "key": "B"},
    {"time": 22.589, "key": "P"},

    {"time": 22.840, "key": "G"}, #down
    {"time": 22.840, "key": "Y"},

    {"time": 23.248, "key": "B"}, #double down
    {"time": 23.248, "key": "Y"},
    {"time": 23.248, "key": "P"},

    {"time": 25.855, "key": "P"}, 
    {"time": 26.270, "key": "Y"},
    {"time": 26.840, "key": "P"}, 
    {"time": 27.396, "key": "Y"}, 
    {"time": 27.517, "key": "P"},
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
                song_start_time = time.time()  # start timer

                beat_recording = True
                beat_times = []
                print("\nBeat Recording Started!\nPress SPACE on every note.\n")

            # Playing screen
            elif game_state == STATE_PLAYING:

                # === Adjustable fall time ===
                FALL_TIME = 1.8  # seconds for note to fall

                # --- Toggle beat recorder ---
                if event.key == pygame.K_b:
                    beat_recording = not beat_recording
                    print("\nBeat Recording:", "ON" if beat_recording else "OFF", "\n")

                # --- Record taps (AUTO-ADJUSTED!) ---
                elif event.key == pygame.K_SPACE and beat_recording:
                    raw_time = time.time() - song_start_time
                    adjusted = raw_time - FALL_TIME

                    if adjusted < 0:
                        adjusted = 0.0

                    beat_times.append(adjusted)
                    print(f"Recorded: {adjusted:.3f}")

                # --- End recording + print chart ---
                elif event.key == pygame.K_s and beat_recording:
                    print("\n=== FINAL NOTE CHART ===")
                    for t in beat_times:
                        print(f'{{"time": {t:.3f}, "key": "R"}},')
                    print("=========================\n")

                    beat_recording = False

                # --- Actual note-hit code ---
                elif event.key == pygame.K_p:
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
    # end when real song time hits 4:02
    if game_state == STATE_PLAYING and song_start_time is not None:
        if time.time() - song_start_time >= SONG_LENGTH:
            pygame.mixer.music.stop()
            game_state = STATE_GAME_OVER


        # End the song if all notes are hit
       # if all(note.hit for note in game.notes):
       #     game_state = STATE_GAME_OVER
        #    pygame.mixer.music.stop()

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
