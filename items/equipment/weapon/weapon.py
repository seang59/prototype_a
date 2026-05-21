from items.equipment.equipment import Equipment
from items.game_object import EquipmentSlot, EquipmentSlot, ItemRarity, WeaponType


class Weapon(Equipment):
    def __init__(self, id, name, sprite, color, stack_size, type: WeaponType, rarity: ItemRarity, damage, attack_speed, prefix: str = None):
        super().__init__(id, name, sprite, color, stack_size, rarity, EquipmentSlot.WEAPON, attack_speed, prefix)
        self.damage = damage
        self.type = type
        self.prefix = prefix

        self.use_time = 1 / attack_speed if attack_speed > 0 else 0


    def use(self, player, camera, world, entity_manager=None):
        pass