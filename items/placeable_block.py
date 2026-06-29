import pygame
import math
from constants import TILE_SIZE
from items.game_object import GameObject, ItemRarity


class PlaceableBlock(GameObject):
    def __init__(self, id: int, name: str, sprite: str = None, sprite_variant: str = None, color: str = None, rarity: ItemRarity = ItemRarity.COMMON, stack_size: int = 200):
        super().__init__(id, name, sprite, color, rarity, stack_size)
        self.sprite_variant = sprite_variant
    
    def use(self, player, camera, world, entity_manager=None):
        player_reach = 5  # max distance for placing blocks
        player_x, player_y = map(int, player.center)
        x, y = camera.screen_to_tile(pygame.mouse.get_pos())

        if (x == player_x and y == player_y) or (x == player_x and y == player_y - 1):
            return False
        
        dx = x - player_x
        dy = y - player_y

        if dx * dx + dy * dy > player_reach * player_reach:
            return False
        
        return world.place_tile(y, x, self.id)