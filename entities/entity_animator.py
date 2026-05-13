import pygame


class EntityAnimator:
    def __init__(self, sprites):
        self.animations = sprites
        self.current_animation = "idle"
        self.frame = 0
        self.facing_right = True

        self.timer = 0
        self.animation_speed = 0.2
        self.rotation = 0

    def update(self, dt):
        self.timer += dt

        while self.timer >= self.animation_speed:
            self.timer -= self.animation_speed
            self.frame += 1

            if self.frame >= (self.animations[self.current_animation].get_width() // 32):
                self.frame = 0

    def return_sprite(self):
        width = self.animations[self.current_animation].get_width()
        height = self.animations[self.current_animation].get_height()

        if width <= 32:
            sprite =  self.animations[self.current_animation]

            if not self.facing_right:
                sprite = pygame.transform.flip(sprite, True, False)
            return sprite

        sprite = self.animations[self.current_animation].subsurface((self.frame * 32, 0, 32, height))

        if not self.facing_right:
            sprite = pygame.transform.flip(sprite, True, False)
        return sprite

    def set_animation_state(self, state: str, facing_right = None):
        if not state in self.animations:
            return
        if facing_right is not None:
            self.facing_right = facing_right
        if state == self.current_animation:
            return

        self.current_animation = state
        self.frame = 0
        self.timer = 0

    def set_rotation(self, angle):
        self.rotation = angle

    def get_rotation(self):
        return self.rotation
            
        