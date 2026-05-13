from items.game_object import GameObject, EquipmentSlot


class Equipment(GameObject):
    def __init__(self, id, name, sprite, color, rarity, stack_size,
        equipment_type: EquipmentSlot, prefix: str = None
    ):
        super().__init__(id, name, sprite, color, rarity, stack_size)
        self.equipment_type = equipment_type
        self.prefix = prefix

    def is_equipment_type(self, type: EquipmentSlot):
        return self.equipment_type == type