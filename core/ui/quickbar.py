import pygame
from entities.player import Player
from items.registry.registry import ItemRegistry
from constants import TILE_SIZE

class Quickbar:
    def __init__(self, player: Player):
        self.slots = 8  # Number of quickbar slots
        self.items = player.inventory.items[:self.slots]
        self.active_slot = player.active_quickbar_slot
        self.is_weapon_drawn = player.is_weapon_drawn
    
    def update(self, player: Player):
        self.items = player.inventory.items[:self.slots]
        self.active_slot = player.active_quickbar_slot
        self.is_weapon_drawn = player.is_weapon_drawn

    def draw(self, surface, x, y, width, height, font):
        for i in range(self.slots):
            slot_x = int(i * width / self.slots)
            slot_x_end = int((i + 1) * width / self.slots)
            w = slot_x_end - slot_x
            h = height
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
            if not self.is_weapon_drawn:
                if i == self.active_slot:
                    pygame.draw.polygon(surf, (100, 255, 50, 150), points)  # highlight active slot
            pygame.draw.polygon(surf, (70, 70, 70, 255), points, 3)    # outline
            surface.blit(surf, (x + slot_x, y))
            
            if self.items:
                if not self.items[i].is_empty():
                    sprite = self.items[i].get_item().sprite
                    color = self.items[i].get_item().color
                    stack_size = self.items[i].count

                    padding = 4
                    icon_size = min(w, h) - padding * 2
                    icon_x = x + slot_x + (w - icon_size) // 2
                    icon_y = y + (h - icon_size) // 2
                    text_offset = -22

                    if color and not sprite:
                        pygame.draw.rect(surface, color, (icon_x, icon_y, icon_size, icon_size))
                    elif sprite:
                        scaled = pygame.transform.scale(sprite, (icon_size, icon_size))
                        surface.blit(scaled, (icon_x, icon_y))
                    
                    if stack_size > 1:
                        stack_text_outline = font[1].render(str(stack_size), True, (0, 0, 0))
                        stack_text = font[0].render(str(stack_size), True, (255, 255, 255))
                        
                        surface.blit(stack_text_outline, (x + slot_x + w - (TILE_SIZE // 4) - padding + 1 + text_offset, y - h + (TILE_SIZE) + 1))
                        surface.blit(stack_text, (x + slot_x + w - (TILE_SIZE // 4) - padding + text_offset, y - h + (TILE_SIZE)))


