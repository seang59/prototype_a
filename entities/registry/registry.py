import pygame
from entities.registry.definitions import ENTITY_DEFINITIONS


class EntitySpriteRegistry:
    def __init__(self):
        self._sprites = {}
        self._load(ENTITY_DEFINITIONS)

    def _load(self, definitions: dict):
        print("Loading entity sprites...")

        for key, entity in definitions.items():
            self._sprites[key] = {}

            for anim_name, path in entity.items():
                if path:
                    loaded_sprite = pygame.image.load(path).convert_alpha()
                    self._sprites[key][anim_name] = loaded_sprite
                else:
                    self._sprites[key][anim_name] = None
            
                print(f"Loaded {anim_name} sprites for entity: {key}")
        print("Entity sprites loaded successfully.")


    def get_sprites(self, entity_key: str) -> dict:
        return self._sprites.get(entity_key, {})