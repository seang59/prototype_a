import math
from entities.ammo.ammo import Ammo
from entities.entity_animator import EntityAnimator
from entities.particles.sparkle import Sparkle


class LightningArrow(Ammo):
    ENTITY_KEY = "arrow"
    def __init__(self, x, y, vx, vy, max_speed=32, hp=1, max_hp=1, armor=0, is_alive=True, should_remove_on_death=False, facing_right=True, jump_height=-10, on_ground=True, flying=False, sprite=None, item_registry=None, width=1, height=0.16, animator: EntityAnimator=None, entity_manager=None, did_collide_x=False, did_collide_y=False, damage=0):
        super().__init__(x, y, vx, vy, max_speed, hp, max_hp, armor, is_alive, should_remove_on_death, facing_right, jump_height, on_ground, flying, sprite, item_registry, width, height, animator, entity_manager, did_collide_x, did_collide_y, damage)
        self.sparkles = []

    def update(self, dt, camera, world, player, input=None):
        super().update(dt, camera, world, player, input)

        if self.vx < 0:
            self.facing_right = False

        self.animator.set_animation_state("idle", self.facing_right) 
    
        if self.vx > 0:
            angle = -math.degrees(math.atan2(self.vy, abs(self.vx)))
        else:
            angle = math.degrees(math.atan2(self.vy, abs(self.vx)))
        self.animator.set_rotation(angle)   

        cx, cy = self.center
        sparkle = Sparkle(cx, cy, self.vx, self.vy)
        self.sparkles.append(sparkle)
        
        for sparkle in self.sparkles:
            sparkle.update(dt)
            if not sparkle.is_alive():
                self.sparkles.remove(sparkle)

    
    def draw(self, surface, camera):
        super().draw(surface, camera)
        for sparkle in self.sparkles:
            sparkle.draw(surface, camera)
    
    def die(self):
        super().die()