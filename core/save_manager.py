import json 
import pickle
from entities.ammo.ammo import Ammo
from entities.enemy import Enemy
from entities.entity_manager import EntityManager
from entities.player import Player
from world.world import World
from dataclasses import dataclass, field
    
@dataclass
class SaveData:
    seed: int
    modified_tiles: dict[tuple[int, int], int] = field(default_factory=dict)
    entities: list = field(default_factory=list)

class SaveManager: #TODO
    def __init__(self, player_name="bob", save_path="saves"):
        self.save_path = f"{save_path}/{player_name}.save"

    def save(self, world: World, entity_manager: EntityManager):
        for e in entity_manager.entities:
            if isinstance(e, Player):
                e.vx = 0
                e.vy = 0
        data = {
            "seed": world.generator.get_world_seed(),
            "world": {f"{y},{x}": int(tile_id) for (y, x), tile_id in world.modified_tiles.items()},
            "entities": [e for e in entity_manager.entities if not isinstance(e, (Ammo, Enemy))],
        }

        with open(self.save_path, 'wb') as f:
            pickle.dump(data, f)

    def load(self) -> SaveData | None:
        try:
            with open(self.save_path, 'rb') as f:
                raw = pickle.load(f)

            print(f"Loaded save data")
            return SaveData(
                seed=raw["seed"],
                modified_tiles={
                    tuple(int(v) for v in k.split(",")): v
                    for k, v in raw.get("world", {}).items()
                },
                entities=raw.get("entities", [])
            )
        except FileNotFoundError:
            return None
        except Exception:
            # Handles corrupt saves or old JSON format incompatibility
            return None