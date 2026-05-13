from .entity import Entity
from items.game_object import GameObject
import math
import pygame
from constants import TILE_SIZE

_ITEM_SIZE = 0.66

class DroppedItem(Entity):
    def __init__(self, item: GameObject, x, y, vx=0, vy=0, stack_count=1):
        super().__init__(x, y, vx, vy, should_remove_on_death=False, max_speed=10, hp=1, max_hp=1, armor=0,
                         width=_ITEM_SIZE, height=_ITEM_SIZE)
        self.item = item
        self.sprite = item.sprite
        self.color = item.color
        self.lifetime = 300.0  # 5 min
        self.stack_count = stack_count

    def __getstate__(self):
        state = super().__getstate__()
        state['item'] = self.item
        state['color'] = self.color
        state['lifetime'] = self.lifetime
        state['stack_count'] = self.stack_count
        return state

    def __setstate__(self, state):
        item = state.pop('item')
        color = state.pop('color')
        lifetime = state.pop('lifetime')
        stack_count = state.pop('stack_count')
        super().__setstate__(state)
        self.item = item
        self.color = color
        self.lifetime = lifetime
        self.stack_count = stack_count

    def restore_after_load(self, item_registry, sprite_registry):
        self.item.sprite = item_registry.get_sprite(self.item.id)
        self.sprite = self.item.sprite

    def update(self, dt, camera, world, player, input=None):
        super().update(dt, camera, world, player, input)  # No input for dropped items
        self.try_pickup(dt, player)

        self.lifetime -= dt
        if self.lifetime <= 0:
            self.die()

    def draw(self, surface, camera):
        camera_zoom, camera_x, camera_y = camera.zoom, camera.x, camera.y
        scaled_size = int(TILE_SIZE * _ITEM_SIZE * camera_zoom)

        x = (self.x * TILE_SIZE - camera_x) * camera_zoom
        y = ((self.y - self.height + 1) * TILE_SIZE - camera_y) * camera_zoom

        if self.sprite:
            scaled_sprite = pygame.transform.scale(self.sprite, (scaled_size, scaled_size))
            surface.blit(scaled_sprite, (x, y))
        else:
            pygame.draw.rect(surface, self.color, (x, y, scaled_size, scaled_size))

    def try_pickup(self, dt, player) -> bool:
        if player is None:
            return False

        dx = player.x - self.x
        dy = player.y - 0.5 - self.y

        if abs(dx) < 2 and abs(dy) < 2:
            dist = math.hypot(dx, dy)
            if dist > 0:
                speed = 10.0
                self.vx = (dx / dist) * speed
                self.vy = (dy / dist) * speed

            if abs(dx) < 0.5 and abs(dy) < 0.5:
                if player.inventory.add_item(self.item, self.stack_count):
                    self.should_remove_on_death = True
                    return True
        else:
            decel = 10.0
            if self.vx > 0:
                self.vx = max(0.0, self.vx - decel * dt)
            elif self.vx < 0:
                self.vx = min(0.0, self.vx + decel * dt)
            if self.vy > 0:
                self.vy = max(0.0, self.vy - decel * dt)
            elif self.vy < 0:
                self.vy = min(0.0, self.vy + decel * dt)

        return False
    
    def die(self):
        super().die()
        self.should_remove_on_death = True
