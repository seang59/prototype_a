import pygame
from items.game_object import GameObject, ItemRarity


class PlaceableBlock(GameObject):
    def __init__(self, id: int, name: str, sprite: str = None, sprite_variant: str = None, color: str = None, rarity: ItemRarity = ItemRarity.COMMON, stack_size: int = 200):
        super().__init__(id, name, sprite, color, rarity, stack_size)
        self.sprite_variant = sprite_variant
    
    def use(self, player, camera, world, entity_manager=None):
        x, y = camera.screen_to_tile(pygame.mouse.get_pos())
        success = world.place_tile(y, x, self.id)

        return success