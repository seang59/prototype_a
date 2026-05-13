import pygame
from items.placeable_block import PlaceableBlock
from items.registry.definitions import DEFINITIONS
from items.game_object import GameObject

class ItemRegistry:
    def __init__(self):
        self._items: dict = {}
        self._sprites: dict[int, pygame.Surface] = {}
        self._tile_data = {}
        self._load(DEFINITIONS)

    def _load(self, definitions: dict):
        print("Loading item definitions...")

        for key, data in definitions.items():
            self._items[key] = data
            item_id = data["id"]
            sprite_path = data.get("sprite")
            sprite = pygame.image.load(sprite_path).convert_alpha() if sprite_path else None
            if sprite_path:
                self._sprites[item_id] = sprite
            if data.get("class") == PlaceableBlock:    
                self._tile_data[item_id] = {"sprite": sprite, "color": data.get("color"), "sprite_variant": data.get("sprite_variant")}

            print(f"Loaded item: {key} (ID: {item_id})")

        print("Item definitions loaded successfully.")

    def create(self, key: str) -> GameObject:
        data = self._items[key].copy()
        object_class = data.pop("class")
        data["sprite"] = self._sprites.get(data["id"])

        return object_class(**data)

    def get(self, key: str) -> dict:
        return self._items[key]

    def get_tile_data(self, tile_id: int) -> dict | None:
        return self._tile_data.get(tile_id)
    
    def get_sprite(self, item_id: int):
        return self._sprites.get(item_id)

    def get_stack_size(self, key: str) -> int:
        item_data = self._items.get(key)
        if item_data is None:
            raise ValueError(f"Item '{key}' not found in registry.")
        
        return item_data.get("stack_size", 1)