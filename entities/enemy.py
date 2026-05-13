import pygame
from entities.entity import Entity
from entities.entity_animator import EntityAnimator
from entities.player import _PLAYER_SPEED


_ENEMY_SPEED = 10
_ENEMY_MAX_SPEED = _ENEMY_SPEED * 0.4

class Enemy(Entity):
    ENTITY_KEY = "enemy"
    def __init__(self, x: float, y: float, vx: float = 0, vy: float = 0, max_speed: float = 6, hp: int = 1, max_hp: int = 1, armor: int = 0, is_alive: bool = True, should_remove_on_death: bool = False, facing_right: bool = True, jump_height: int = -10, on_ground: bool = True, flying: bool = False, sprite: str = None, item_registry=None, animator: EntityAnimator = None, entity_manager=None):
        super().__init__(x, y, vx, vy, max_speed, hp, max_hp, armor, is_alive, should_remove_on_death, facing_right, jump_height, on_ground, flying, sprite, item_registry, animator=animator, entity_manager=entity_manager)

    def update(self, dt, camera, world, player, input=None):
        super().update(dt, camera, world, player, input)
    
        """MOVEMENT"""
        if self.should_jump() and self.on_ground:
            self.vy = self.jump_height
            self.on_ground = False

        self.AI_move_to_player(player)
    
    def draw(self, surface, camera):
        super().draw(surface, camera)
    
    def die(self):
        super().die()
        self.should_remove_on_death = True

    def AI_move_to_player(self, player):
        distance_x = player.x - self.x

        if abs(distance_x) < 200: 
            if distance_x < 0:
                self.vx = max(self.vx - _ENEMY_SPEED, -_ENEMY_MAX_SPEED)
                self.facing_right = False
            else:
                self.vx = min(self.vx + _ENEMY_SPEED, _ENEMY_MAX_SPEED)
                self.facing_right = True

    def should_jump(self):
        if self.vx == 0:
            return True
        else:
            return False

