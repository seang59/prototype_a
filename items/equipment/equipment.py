from items.game_object import GameObject, EquipmentSlot


class Equipment(GameObject):
    def __init__(self, id, name, sprite, color, rarity, stack_size,
        equipment_type: EquipmentSlot, attack_speed, prefix: str = None
    ):
        super().__init__(id, name, sprite, color, rarity, stack_size)
        self.equipment_type = equipment_type
        self.attack_speed = attack_speed
        self.prefix = prefix
        self.cooldown_remaining = 0

    def update(self, dt):
        if self.cooldown_remaining > 0:
            self.cooldown_remaining = max(0, self.cooldown_remaining - dt)

    def is_equipment_type(self, type: EquipmentSlot):
        return self.equipment_type == type

    def is_on_cooldown(self):
        return self.cooldown_remaining > 0