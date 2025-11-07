import pygame
from constants import *
import time

class Note:
    def __init__(self, lane_index, spawn_time):
        self.lane_index = lane_index
        self.spawn_time = spawn_time
        self.y = -NOTE_HEIGHT
        self.hit = False

    def update(self, delta_time):
        self.y += NOTE_SPEED * delta_time

    def draw(self, screen):
        color = LANE_COLORS[self.lane_index]
        x = LANE_X[self.lane_index]
        pygame.draw.rect(screen, color, (x, self.y, NOTE_WIDTH, NOTE_HEIGHT))


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

    def load_notes(self, note_chart):
        # Convert key to lane_index
        key_to_lane = {"R": 0, "G": 1, "B": 2, "Y": 3, "P": 4}
        for note in note_chart:
            lane = key_to_lane[note["key"]]
            self.notes.append(Note(lane, note["time"]))

    def start(self):
        self.start_time = time.time()

    def toggle_pause(self):
        if not self.paused:
            self.paused = True
            self.pause_time = time.time()
        else:
            paused_duration = time.time() - self.pause_time
            self.start_time += paused_duration
            self.paused = False

    def restart(self):
        self.active_notes.clear()
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.total_hits = 0
        self.total_misses = 0
        self.start_time = None

    def update(self):
        if self.start_time is None or self.paused:
            return

        current_time = time.time() - self.start_time
        delta_time = 1 / FPS

        # Spawn new notes
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

    def draw(self, screen):
        for note in self.active_notes:
            note.draw(screen)

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
        distance = abs(note.y - HIT_Y)
        hit_type = "Perfect" if distance <= HIT_WINDOW / 2 else "Good"
        self.score += HIT_SCORES[hit_type]
        self.combo += 1
        self.max_combo = max(self.combo, self.max_combo)
        self.total_hits += 1
        return hit_type

    def register_miss(self, note):
        note.hit = True
        self.combo = 0
        self.total_misses += 1
        return "Miss"
