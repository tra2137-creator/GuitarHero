import pygame
import sys
import time
from constants import *
from game import Game
import serial
import threading

beat_recording = False
beat_times = []

song_start_time = None
SONG_LENGTH = 4 * 60 + 2   # 4:02


arduino_input = None
current_fret = None
strum_triggered = False


def read_arduino():
    global arduino_input
    ser = serial.Serial("/dev/tty.usbmodem*", 9600)  # macOS auto-detect RMR PUT OWN
    while True:
        try:
            line = ser.readline().decode().strip()
            if line:
                arduino_input = line  # set last key
        except:
            pass

# Start the thread
threading.Thread(target=read_arduino, daemon=True).start()

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

# --- Notes chart ---
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
    {"time": 8.029, "key": "P"}, 

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
    {"time": 27.986, "key": "P"},
    {"time": 28.544, "key": "Y"},
    {"time": 29.109, "key": "P"},
    {"time": 29.647, "key": "Y"},
    {"time": 30.204, "key": "P"},
    {"time": 30.760, "key": "Y"},
    {"time": 31.313, "key": "P"},
    {"time": 31.820, "key": "Y"},
    {"time": 32.361, "key": "P"},
    {"time": 32.912, "key": "Y"},
    {"time": 33.450, "key": "P"},
    {"time": 33.023, "key": "Y"},

    #Back to guitar notes
    {"time": 25.818, "key": "B"},

    {"time": 26.872, "key": "R"},
    {"time": 26.872, "key": "G"},

    {"time": 27.292, "key": "B"},

    {"time": 27.697, "key": "R"},
    {"time": 27.697, "key": "G"},

    {"time": 29.081, "key": "R"},
    {"time": 29.081, "key": "G"},

    {"time": 29.486, "key": "B"},

    {"time": 29.875, "key": "R"},
    {"time": 29.875, "key": "G"},

    {"time": 31.255, "key": "G"},
    {"time": 31.678, "key": "B"},
    {"time": 32.084, "key": "R"},

##
    {"time": 34.565, "key": "B"},

    {"time": 35.712, "key": "R"},
    {"time": 35.712, "key": "G"},

    {"time": 36.120, "key": "B"},

    {"time": 36.479, "key": "R"},
    {"time": 36.479, "key": "G"},

    {"time": 37.865, "key": "R"},
    {"time": 37.865, "key": "G"},

    {"time": 38.302, "key": "B"},

    {"time": 38.706, "key": "R"},
    {"time": 38.706, "key": "G"},

    {"time": 40.137, "key": "G"},
    {"time": 40.561, "key": "B"},
    {"time": 40.967, "key": "R"},


    #Chord before start
    {"time": 43.400, "key": "R"},
    {"time": 43.400, "key": "B"},
    {"time": 43.400, "key": "P"},
    #down time
    {"time": 43.990, "key": "R"},
    {"time": 44.521, "key": "R"},
    {"time": 45.086, "key": "R"},
    {"time": 45.609, "key": "R"},
    {"time": 46.178, "key": "R"},
    {"time": 46.701, "key": "R"},
    {"time": 47.188, "key": "B"},
    {"time": 47.298, "key": "R"},
    {"time": 47.497, "key": "G"},
    {"time": 47.823, "key": "R"},

    #Chill song part
    {"time": 48.444, "key": "R"},
    {"time": 48.941, "key": "B"},
    {"time": 49.555, "key": "R"},
    {"time": 50.052, "key": "B"},
    {"time": 50.052, "key": "Y"},
    {"time": 50.629, "key": "R"},
    {"time": 51.141, "key": "B"},
    {"time": 51.723, "key": "R"},
    {"time": 52.239, "key": "B"},
    {"time": 52.239, "key": "Y"},
    {"time": 52.847, "key": "R"},
    {"time": 53.339, "key": "B"},
    {"time": 53.914, "key": "R"},
    {"time": 54.422, "key": "B"},
    {"time": 54.422, "key": "Y"},
    {"time": 54.961, "key": "R"},
    {"time": 55.493, "key": "B"},
    {"time": 56.076, "key": "R"},
    {"time": 56.633, "key": "B"},
    {"time": 56.633, "key": "Y"},
    {"time": 57.188, "key": "R"},
    {"time": 57.763, "key": "B"},
    {"time": 58.312, "key": "R"},
    {"time": 58.858, "key": "B"},
    {"time": 58.858, "key": "Y"},
    {"time": 59.437, "key": "R"},
    {"time": 59.957, "key": "B"},
    {"time": 60.569, "key": "R"},
    {"time": 61.072, "key": "B"},
    {"time": 61.072, "key": "Y"},
    {"time": 61.631, "key": "R"},
    {"time": 62.138, "key": "B"},
    {"time": 62.709, "key": "R"},
    {"time": 63.253, "key": "B"},
    {"time": 63.253, "key": "Y"},
    {"time": 64.658, "key": "R"},
    {"time": 65.026, "key": "B"},
    {"time": 65.414, "key": "R"},
    {"time": 65.414, "key": "Y"},
    {"time": 65.987, "key": "B"},
    {"time": 66.543, "key": "R"},
    {"time": 67.114, "key": "B"},
    {"time": 67.655, "key": "R"},
    {"time": 67.655, "key": "Y"},
    {"time": 68.739, "key": "B"},
    {"time": 69.278, "key": "R"},
    {"time": 69.851, "key": "B"},
    {"time": 69.851, "key": "Y"},
    {"time": 70.437, "key": "R"},
    {"time": 70.959, "key": "B"},
    {"time": 71.515, "key": "R"},
    {"time": 72.071, "key": "B"},
    {"time": 72.071, "key": "Y"},
    {"time": 72.658, "key": "R"},
    {"time": 73.179, "key": "B"},
    {"time": 73.737, "key": "R"},
    {"time": 74.256, "key": "B"},
    {"time": 74.256, "key": "Y"},
    {"time": 74.848, "key": "R"},
    {"time": 75.387, "key": "B"},
    {"time": 75.967, "key": "R"},
    {"time": 76.512, "key": "B"},
    {"time": 76.512, "key": "Y"},
    {"time": 77.103, "key": "R"},
    {"time": 77.624, "key": "B"},
    {"time": 78.181, "key": "R"},
    {"time": 78.706, "key": "B"},
    {"time": 78.706, "key": "Y"},
    {"time": 79.349, "key": "R"},
    {"time": 79.823, "key": "B"},
    {"time": 80.378, "key": "R"},
    {"time": 80.900, "key": "B"},
    {"time": 80.900, "key": "Y"},

    #
    {"time": 82.336, "key": "P"},
    {"time": 82.716, "key": "B"},
    {"time": 83.096, "key": "R"},
    {"time": 84.259, "key": "B"},
    {"time": 84.793, "key": "R"},
    {"time": 85.346, "key": "B"},

    {"time": 83.096, "key": "P"},
    {"time": 85.346, "key": "P"},
    {"time": 86.467, "key": "B"},
    {"time": 87.536, "key": "Y"},
    {"time": 89.712, "key": "P"},
    {"time": 90.340, "key": "Y"},
    {"time": 91.953, "key": "P"},

    {"time": 85.923, "key": "R"},
    {"time": 86.467, "key": "B"},
    {"time": 87.014, "key": "R"},
    {"time": 87.536, "key": "B"},
    {"time": 88.123, "key": "R"},
    {"time": 88.647, "key": "B"},
    {"time": 89.187, "key": "R"},
    {"time": 89.712, "key": "B"},
    {"time": 90.340, "key": "R"},
    {"time": 90.883, "key": "B"},
    {"time": 91.423, "key": "R"},
    {"time": 91.953, "key": "B"},

    {"time": 94.166, "key": "P"},
    {"time": 95.33, "key": "B"},
    {"time": 96.398, "key": "R"},
    {"time": 96.971, "key": "Y"},
    {"time": 97.462, "key": "G"},
    {"time": 98.035, "key": "R"},
    {"time": 98.562, "key": "P"},
    {"time": 100.734, "key": "R"},

    #Second
    {"time": 103.024, "key": "R"},
    {"time": 103.553, "key": "G"},
    {"time": 104.083, "key": "B"},
    {"time": 104.658, "key": "R"},
    {"time": 105.251, "key": "P"},
    {"time": 107.476, "key": "B"},
    {"time": 108.591, "key": "R"},
    {"time": 109.652, "key": "G"},
    {"time": 111.799, "key": "Y"},
    {"time": 112.898, "key": "R"},
    {"time": 116.245, "key": "P"},
    {"time": 117.377, "key": "G"},
    {"time": 118.472, "key": "Y"},
    {"time": 120.605, "key": "R"},
    {"time": 121.748, "key": "P"},
    {"time": 122.324, "key": "B"},
    {"time": 122.882, "key": "Y"},
    {"time": 125.021, "key": "G"},
    {"time": 126.181, "key": "R"},
    {"time": 127.254, "key": "B"},
    {"time": 129.418, "key": "P"},
    {"time": 129.962, "key": "Y"},
    {"time": 131.636, "key": "G"},
    {"time": 133.828, "key": "R"},
    {"time": 134.966, "key": "B"},
    {"time": 136.042, "key": "P"},
    {"time": 136.836, "key": "Y"},
    {"time": 137.125, "key": "B"},
    {"time": 137.527, "key": "G"},
    {"time": 138.216, "key": "R"},
    {"time": 140.394, "key": "P"},

    {"time": 145.152, "key": "B"},
    {"time": 145.152, "key": "P"},
    {"time": 145.595, "key": "Y"},
    {"time": 146.177, "key": "B"},
    {"time": 146.177, "key": "P"},
    {"time": 146.731, "key": "Y"},
    {"time": 147.255, "key": "B"},
    {"time": 147.255, "key": "P"},
    {"time": 147.823, "key": "Y"},
    {"time": 148.439, "key": "B"},
    {"time": 148.439, "key": "P"},
    {"time": 148.936, "key": "Y"},
    {"time": 149.490, "key": "B"},
    {"time": 149.490, "key": "P"},
    {"time": 150.074, "key": "Y"},
    {"time": 151.718, "key": "B"},
    {"time": 151.718, "key": "P"},
    {"time": 152.747, "key": "G"},
    {"time": 153.794, "key": "B"},
    {"time": 153.794, "key": "P"},
    {"time": 154.996, "key": "G"},

    {"time": 156.100, "key": "G"},
    {"time": 157.776, "key": "G"},
    {"time": 159.482, "key": "G"},
    {"time": 160.556, "key": "G"},
    {"time": 161.616, "key": "G"},
    {"time": 162.665, "key": "G"},
    {"time": 163.793, "key": "G"},
    {"time": 164.858, "key": "G"},
    {"time": 165.960, "key": "G"},


    {"time": 167.174, "key": "P"}, # Eye of the tiger


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

            elif game_state == STATE_PLAYING:

                FALL_TIME = 1.8

                # ==================================================
                # 1. ARDUINO INPUT
                # ==================================================
                if arduino_input:
                    if arduino_input in ["R","G","B","Y","P"]:
                        current_fret = arduino_input.lower()

                    elif arduino_input in ["STRUM_UP","STRUM_DOWN"]:
                        strum_triggered = True

                    arduino_input = None  # clear after use


                # ==================================================
                # 2. KEYBOARD INPUT
                # ==================================================
                if event.type == pygame.KEYDOWN:

                    # FRET KEYS
                    if event.key == pygame.K_d:
                        current_fret = "d"   # red
                    elif event.key == pygame.K_f:
                        current_fret = "f"   # green
                    elif event.key == pygame.K_j:
                        current_fret = "j"   # blue
                    elif event.key == pygame.K_k:
                        current_fret = "k"   # yellow
                    elif event.key == pygame.K_l:
                        current_fret = "l"   # purple


                    # STRUM
                    elif event.key == pygame.K_a:
                        strum_triggered = True

                    # Beat recorder toggle
                    elif event.key == pygame.K_b:
                        beat_recording = not beat_recording

                    # Beat tap
                    # --- 3. Beat Recording ---
                    if event.key == pygame.K_SPACE and beat_recording:
                        raw_time = time.time() - song_start_time
                        adjusted = max(0.0, raw_time - FALL_TIME)
                        beat_times.append(adjusted)
                        print(f"Recorded: {adjusted:.3f}")
                        continue



                    # Stop beat recording
                    elif event.key == pygame.K_s and beat_recording:
                        print("\n=== FINAL NOTE CHART ===")
                        for t in beat_times:
                            print(f'{{"time": {t:.3f}, "key": "R"}},')
                        print("=========================\n")
                        beat_recording = False

                    elif event.key == pygame.K_p:
                        game.toggle_pause()


                # ==================================================
                # 3. UNIVERSAL HIT CHECK (WORKS FOR BOTH INPUTS)
                # ==================================================
                if strum_triggered and current_fret:
                    result = game.handle_input(current_fret)
                    strum_triggered = False  # reset after hit

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
