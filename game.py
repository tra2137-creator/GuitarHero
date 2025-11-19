import pygame
import time
import random
from constants import *

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.radius = random.randint(2,5)
        self.color = color
        self.life = random.uniform(0.3, 0.6)
        self.vel_x = random.uniform(-50,50)
        self.vel_y = random.uniform(-50,-100)

    def update(self, delta_time):
        self.x += self.vel_x * delta_time
        self.y += self.vel_y * delta_time
        self.life -= delta_time

    def draw(self, screen):
        if self.life > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class Note:
    def __init__(self, lane_index, spawn_time, hold_duration=0):
        self.lane_index = lane_index
        self.spawn_time = spawn_time
        self.hold_duration = hold_duration  # seconds (0 = normal note)
        self.y = -NOTE_RADIUS * 2
        self.hit = False
        self.holding = False

    def update(self, delta_time):
        self.y += NOTE_SPEED * delta_time

    def draw(self, screen):
        color = LANE_COLORS[self.lane_index]
        x = LANE_X[self.lane_index]

        # HOLD NOTES (sustain)
        if self.hold_duration > 0:
            hold_pixels = self.hold_duration * NOTE_SPEED
            
            # sustain runs BELOW the head, not above
            start_y = self.y
            end_y = self.y + hold_pixels

            # Draw the sustain line ONLY in visible area
            visible_start = max(start_y, 0)
            visible_end   = min(end_y, SCREEN_HEIGHT)

            if visible_end > visible_start:
                pygame.draw.line(
                    screen,
                    color,
                    (x, visible_start),
                    (x, visible_end),
                    6
                )

            # draw a tail bubble
            pygame.draw.circle(
                screen,
                color,
                (x, int(end_y)),
                int(NOTE_RADIUS * 0.7)
            )

        # NOTE HEAD (always drawn)
        pygame.draw.circle(screen, color, (x, int(self.y)), NOTE_RADIUS)

class Game:
    def __init__(self):
        self.notes = []
        self.active_notes = []
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.total_hits = 0
        self.total_misses = 0
        self.start_time = None
        self.paused = False
        self.pause_time = 0
        self.particles = []

    def load_notes(self, note_chart):
        key_to_lane = {"R":0,"G":1,"B":2,"Y":3,"P":4}
        for note in note_chart:
            lane = key_to_lane[note["key"]]
            hold = note.get("hold",0)  # hold duration optional
            self.notes.append(Note(lane, note["time"], hold))

    def start(self):
        self.start_time = time.time()

    def toggle_pause(self):
        if not self.paused:
            self.paused = True
            self.pause_time = time.time()
        else:
            self.start_time += time.time() - self.pause_time
            self.paused = False

    def update(self):
        if self.start_time is None or self.paused:
            return

        current_time = time.time() - self.start_time
        delta_time = 1 / FPS

        # Spawn notes
        for note in self.notes:
            if note.spawn_time <= current_time and note not in self.active_notes:
                self.active_notes.append(note)

        # Update notes
        for note in self.active_notes:
            note.update(delta_time)

        # Check misses
        for note in self.active_notes[:]:
            if note.y > HIT_Y + HIT_WINDOW and not note.hit:
                self.register_miss(note)

        # Update particles
        for particle in self.particles[:]:
            particle.update(delta_time)
            if particle.life <= 0:
                self.particles.remove(particle)

    def draw(self, screen):
        # Draw hit zones
        for lane_index, x in LANE_X.items():
            pygame.draw.circle(screen, LANE_COLORS[lane_index], (x, HIT_Y), HIT_RADIUS, 5)

        # Draw notes
        for note in self.active_notes:
            note.draw(screen)

        # Draw particles
        for particle in self.particles:
            particle.draw(screen)

    def handle_input(self, key_pressed):
        if self.paused:
            return None

        for note in self.active_notes:
            if note.hit:
                continue
            if KEY_MAPPING[note.lane_index] == key_pressed:
                distance = abs(note.y - HIT_Y)
                if distance <= HIT_WINDOW:
                    return self.register_hit(note)
        return None

    def register_hit(self, note):
        note.hit = True
        note.holding = note.hold_duration > 0
        distance = abs(note.y - HIT_Y)
        hit_type = "Perfect" if distance <= HIT_WINDOW / 2 else "Good"
        self.score += HIT_SCORES[hit_type]
        self.combo += 1
        self.max_combo = max(self.combo, self.max_combo)
        self.total_hits += 1

        # particles
        x = LANE_X[note.lane_index]
        for _ in range(15):
            self.particles.append(Particle(x, HIT_Y, LANE_COLORS[note.lane_index]))

        return hit_type

    def register_miss(self, note):
        note.hit = True
        self.combo = 0
        self.total_misses += 1
        return "Miss"
