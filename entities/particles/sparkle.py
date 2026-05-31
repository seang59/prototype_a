import pygame
import random  
from constants import TILE_SIZE


_GRAVITY = 24
_MAX_FALL_SPEED = 20.0

class Sparkle:
    def __init__(self, x, y, vx, vy, lifetime=1):
        self.x = x
        self.y = y
        self.vx = random.gauss(0, 0.6) - vx * 0.4
        self.vy = random.gauss(0, 0.6) - vy * 0.4
        self.size = random.uniform(0.04, 0.15)
        self.lifetime = lifetime
        self._max_lifetime = lifetime
        self.color = random.choice([
            (255, 255, 255),    # white
            (180, 220, 255),    # blue
            (220, 255, 180),    # yellow-green
        ])

    def update(self, dt):
        if self.lifetime <= 0:
            return

        self.vy += _GRAVITY * .0135 ** (1 - dt)
        if self.vy > _MAX_FALL_SPEED:
            self.vy = _MAX_FALL_SPEED

        self.x += self.vx * dt
        self.y += self.vy * dt
        self.lifetime -= 1 * dt

    def draw(self, surface, camera):
        if self.is_alive():
            camera_zoom, camera_x, camera_y = camera.zoom, camera.x, camera.y
            scaled_size = max(1, int(TILE_SIZE * self.size * camera_zoom))
            x = (self.x * TILE_SIZE - camera_x) * camera_zoom
            y = (self.y * TILE_SIZE - camera_y) * camera_zoom
            
            alpha = int(255 * (self.lifetime / self._max_lifetime))
            sparkle_surf = pygame.Surface((scaled_size * 2, scaled_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(sparkle_surf, (*self.color, alpha), (scaled_size, scaled_size), scaled_size)
            surface.blit(sparkle_surf, (x - scaled_size, y - scaled_size))

    def is_alive(self):
        return self.lifetime > 0