import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE, WORLD_HEIGHT, WORLD_WIDTH

_WORLD_PIXEL_WIDTH = WORLD_WIDTH * TILE_SIZE
_WORLD_PIXEL_HEIGHT = WORLD_HEIGHT * TILE_SIZE

_ZOOM_MIN = 0.125
_ZOOM_MAX = 2.0
_ZOOM_STEP = 0.25


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.zoom = 1.0

    def adjust_zoom(self, direction):
        self.zoom = max(_ZOOM_MIN, min(_ZOOM_MAX, round(self.zoom + direction * _ZOOM_STEP, 2)))

    def update(self, target, input):
        if input.is_just_pressed(pygame.K_EQUALS) or input.is_just_pressed(pygame.K_KP_PLUS):
            self.adjust_zoom(1)
        elif input.is_just_pressed(pygame.K_MINUS) or input.is_just_pressed(pygame.K_KP_MINUS):
            self.adjust_zoom(-1)
        elif input.is_just_pressed(pygame.K_0) or input.is_just_pressed(pygame.K_KP_0):
            self.zoom = 1.0

        visible_width = SCREEN_WIDTH / self.zoom 
        visible_height = SCREEN_HEIGHT / self.zoom 
        # * TILE_SIZE if following player, not mouse
        self.x = max(0, min(int((target[0]) * TILE_SIZE - visible_width / 2),  _WORLD_PIXEL_WIDTH - visible_width)) 
        self.y = max(0, min(int((target[1]) * TILE_SIZE - visible_height / 2), _WORLD_PIXEL_HEIGHT - visible_height))

    def apply(self, rect):
        return rect.move(-self.x, -self.y)
    
    def screen_to_world(self, screen_pos) -> tuple[float, float]:
        world_x = (screen_pos[0] / SCREEN_WIDTH)  * _WORLD_PIXEL_WIDTH
        world_y = (screen_pos[1] / SCREEN_HEIGHT) * _WORLD_PIXEL_HEIGHT

        return (world_x, world_y)

    def screen_to_tile(self, screen_pos) -> tuple[int, int]:
        world_x = screen_pos[0] / self.zoom + self.x
        world_y = screen_pos[1] / self.zoom + self.y
        
        return int(world_x // TILE_SIZE), int(world_y // TILE_SIZE)