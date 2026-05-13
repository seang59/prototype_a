from entities.entity import Entity


class Ammo(Entity):
    def __init__(self, x, y, vx, vy, max_speed, hp=1, max_hp=1, armor=0, is_alive = True, should_remove_on_death = False, facing_right = True, jump_height = -10, on_ground = True, flying = False, sprite = None, item_registry=None, width = 1, height = 2, animator = None, entity_manager=None, did_collide_x=False, did_collide_y=False, damage=0):
        super().__init__(x, y, vx, vy, max_speed, hp, max_hp, armor, is_alive, should_remove_on_death, facing_right, jump_height, on_ground, flying, sprite, item_registry, width, height, animator, entity_manager, did_collide_x, did_collide_y)
        self.damage = damage

    def update(self, dt, camera, world, player, input=None):
        super().update(dt, camera, world, player, input)

        if self.did_collide_x or self.did_collide_y or self.entity_manager.collided_ammo_with_entity(self, damage=self.damage):
            self.die()
    
    def draw(self, surface, camera):
        super().draw(surface, camera)
    
    def die(self):
        super().die()
        self.should_remove_on_death = True