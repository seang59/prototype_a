from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from items.equipment.weapon.weapon import Weapon


if TYPE_CHECKING:
    from entities.entity_manager import EntityManager     


class Bow(Weapon):
    def __init__(self, id, name, sprite, color, stack_size, type, rarity, damage, attack_speed, damage_mult):
        super().__init__(id, name, sprite, color, stack_size, type, rarity, damage, attack_speed)
        self.damage_mult = damage_mult

    def use(self, player, camera, world, entity_manager: EntityManager = None):
        if self.is_on_cooldown():
            return False

        arrow_speed = 32
        mouse_x, mouse_y = camera.screen_to_tile(pygame.mouse.get_pos())

        dx = mouse_x - player.center[0]
        dy = mouse_y - player.center[1]

        length = (dx ** 2 + dy ** 2) ** 0.5

        if length == 0:
            return False

        vx = (dx / length) * arrow_speed
        vy = (dy / length) * arrow_speed

        if isinstance(player.equipement.weapon2_slot.get_item(), Quiver):
            entity_manager.spawn_ammo(player.x, player.y - 1, vx, vy, player.equipement.weapon2_slot.get_item().get_ammo_type(), damage=player.equipement.weapon2_slot.get_item().get_damage() * self.damage_mult)
            self.cooldown_remaining = self.use_time
            return True
        else:
            return False
        

        
class Quiver(Weapon):
    def __init__(self, id, name, sprite, color, stack_size, type, rarity, damage, attack_speed, arrow_type="arrow"):
        super().__init__(id, name, sprite, color, stack_size, type, rarity, damage, attack_speed)
        self.arrow_type = arrow_type

    def get_ammo_type(self):
        return self.arrow_type
    
    def get_damage(self):
        return self.damage
