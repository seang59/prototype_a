import pygame
from entities.player import Player
from constants import TILE_SIZE

class InventoryUI:
    def __init__(self, player: Player):
        self.player = player
        self.slots = 32 
        self.items = player.inventory.items[8:]
        self.show_inventory = player.show_inventory

    def update(self, player: Player):
        self.items = player.inventory.items[8:]
        self.show_inventory = player.show_inventory

    def draw(self, surface, x, y, width, height, font):
        if self.show_inventory:
            slots = self.slots
            slots_per_row = 8
            slot_index = 0

            for i in range(slots // slots_per_row):
                for n in range(slots_per_row):
                    new_y = y
                    if i != 0:
                        new_y = y - (height * i)

                    slot_x = int(n * width / slots_per_row)
                    slot_x_end = int((n + 1) * width / slots_per_row)
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
                    pygame.draw.polygon(surf, (70, 70, 70, 255), points, 3)    # outline
                    surface.blit(surf, (x + slot_x, new_y))
                    
                    if self.items:
                        if not self.items[slot_index].is_empty():
                            sprite = self.items[slot_index].get_item().sprite
                            color = self.items[slot_index].get_item().color
                            stack_size = self.items[slot_index].count

                            padding = 4
                            icon_size = min(w, h) - padding * 2
                            icon_x = x + slot_x + (w - icon_size) // 2
                            icon_y = new_y + (h - icon_size) // 2

                            if color and not sprite:
                                pygame.draw.rect(surface, color, (icon_x, icon_y, icon_size, icon_size))
                            elif sprite:
                                scaled = pygame.transform.scale(sprite, (icon_size, icon_size))
                                surface.blit(scaled, (icon_x, icon_y))
                            
                            if stack_size > 1:
                                stack_text_outline = font[1].render(str(stack_size), True, (0, 0, 0))
                                stack_text = font[0].render(str(stack_size), True, (255, 255, 255))
                                
                                surface.blit(stack_text_outline, (x + slot_x + w - (TILE_SIZE // 4) - padding + 1, new_y - h + (TILE_SIZE) + 1))
                                surface.blit(stack_text, (x + slot_x + w - (TILE_SIZE // 4) - padding, new_y - h + (TILE_SIZE)))
                    slot_index += 1



    
