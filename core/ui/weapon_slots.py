from entities.player import Player
import pygame
from constants import TILE_SIZE

class WeaponSlots:
    def __init__(self, player: Player):                         #TODO
        self.slots = 2
        self.weapon1 = player.equipement.weapon1_slot.get_item()
        self.weapon2 = player.equipement.weapon2_slot.get_item()
        self.active_weapon_slot = player.active_weapon_slot
        self.is_weapon_drawn = player.is_weapon_drawn

    def update(self, player: Player):
        self.weapon1 = player.equipement.weapon1_slot.get_item()
        self.weapon2 = player.equipement.weapon2_slot.get_item()
        self.active_weapon_slot = player.active_weapon_slot
        self.is_weapon_drawn = player.is_weapon_drawn

    def draw(self, surface, x, y, width, height, font):
        for i in range(self.slots): 
            slot_y = int(i * height / self.slots)
            slot_y_end = int((i + 1) * height / self.slots)
            w = width
            h = slot_y_end - slot_y
            cut = 6

            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            points = [
                (cut, 0),
                (w - 1 - cut, 0),
                (w - 1, cut),
                (w - 1, h - cut - 1),
                (w - 1 - cut, h - 1),
                (cut, h - 1),
                (0, h - cut - 1),
                (0, cut)
            ]

            pygame.draw.polygon(surf, (199, 199, 199, 200), points)       # filled
            if self.is_weapon_drawn:
                if i == self.active_weapon_slot:
                    pygame.draw.polygon(surf, (100, 255, 50, 150), points)  # highlight active slot
            pygame.draw.polygon(surf, (70, 70, 70, 255), points, 3)    # outline
            surface.blit(surf, (x, y + slot_y))
            
            if self.weapon1 or self.weapon2:
                weapons = [self.weapon1, self.weapon2]
                weapon = weapons[i]

                if weapon:
                    sprite = weapon.sprite
                    color = weapon.color

                    padding = 6
                    icon_size = min(w, h) - padding * 2
                    icon_x = x + (w - icon_size) // 2
                    icon_y = y + slot_y + (h - icon_size) // 2

                    if color and not sprite:
                        pygame.draw.rect(surface, color, (icon_x, icon_y, icon_size, icon_size))
                    elif sprite:
                        scaled = pygame.transform.scale(sprite, (icon_size, icon_size))
                        surface.blit(scaled, (icon_x, icon_y))
                    