from enum import IntEnum

class ItemRarity(IntEnum):
    COMMON = 0
    UNCOMMON = 1
    RARE = 2
    EPIC = 3
    LEGENDARY = 4

class EquipmentSlot(IntEnum):
    HEAD = 0
    CHEST = 1
    LEGS = 2
    FEET = 3
    TRINKET = 4
    WEAPON = 5

class WeaponType(IntEnum):
    SWORD = 0
    LONG_SWORD = 1
    AXE = 2
    RANGED = 3
    MAGIC = 4
    AMMO = 5

class AmmoType(IntEnum):
    ARROW = 0
    BULLET = 1
    MANA = 2
    
class ArmorType(IntEnum):
    LIGHT = 0
    MEDIUM = 1
    HEAVY = 2

class ConsumableType(IntEnum):
    HEALTH_POTION = 0
    MANA_POTION = 1
    STAMINA_POTION = 2

class GameObject:
    def __init__(self, id: int, name: str, sprite: str = None, color: str = None, rarity: ItemRarity = ItemRarity.COMMON, stack_size: int = 1):
        self.id = id
        self.name = name
        self.sprite = sprite

        self.color = color
        self.stack_size = stack_size
        self.rarity = rarity

    def use(self, player, camera, world, entity_manager = None):
        pass

    def __getstate__(self):
        state = self.__dict__.copy()
        state['sprite'] = None  # pygame Surface is not picklable; restored via item_registry after load
        return state





