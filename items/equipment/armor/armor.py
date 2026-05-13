from items.equipment.equipment import Equipment
from items.game_object import EquipmentSlot, ItemRarity


class Armor(Equipment):
    def __init__(self, id, name, sprite, color, stack_size, equipment_type: EquipmentSlot, rarity: ItemRarity, armor, durability, prefix: str = None):
        super().__init__(id, name, sprite, color, stack_size, rarity, equipment_type, prefix)
        self.armor = armor
        self.durability = durability
        self.prefix = prefix

