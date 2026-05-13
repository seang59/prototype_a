
from core.camera import Camera
import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, WORLD_HEIGHT, WORLD_WIDTH, TILE_SIZE

class BackgroundManager:
    def __init__(self, biome=None, grass_y=0):
        self.biome = biome
        self.grass_y = grass_y  # world-pixel y of the grass surface
        self.bg = pygame.image.load("sprites/background/BackgroundCastle-Sheet.png").convert()
        self.bg.set_colorkey((0, 0, 0))
        self.bg_width = self.bg.get_width()
        self.bg_height = self.bg.get_height()
        self._cached_zoom = None
        self._scaled_bg = None
        self._scaled_w = 0
        self._scaled_h = 0
    
    def update(self, player, camera):
        pass

    def draw(self, surface, camera: Camera):
        scale_image_factor = 5

        if camera.zoom != self._cached_zoom:
            self._scaled_w = int(self.bg_width * camera.zoom) * scale_image_factor
            self._scaled_h = int(self.bg_height * camera.zoom) * scale_image_factor
            self._scaled_bg = pygame.transform.scale(self.bg, (self._scaled_w, self._scaled_h))
            self._cached_zoom = camera.zoom

        x_parallax_factor = 0.3
        offset_x = int(camera.x * x_parallax_factor * camera.zoom) % self._scaled_w

        # Anchor bottom of image to the grass surface in screen space
        grass_screen_y = (self.grass_y - camera.y) * camera.zoom
        y = int(grass_screen_y) - self._scaled_h

        x = -offset_x
        while x < SCREEN_WIDTH:
            surface.blit(self._scaled_bg, (x, y))
            x += self._scaled_w

        surface.fill((0, 0, 0), (0, self.grass_y, SCREEN_WIDTH, SCREEN_HEIGHT - self.grass_y)) #TODO

    def set_biome(self, biome):
        self.biome = biome


