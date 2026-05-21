import pygame
from constants import TILE_SIZE, WORLD_WIDTH, WORLD_HEIGHT
from entities.entity_animator import EntityAnimator

_GRAVITY = 24
_MAX_FALL_SPEED = 20.0

class Entity:
    ENTITY_KEY = "entity"
    __slots__ = ("x", "y", "vx", "vy", "max_speed", "hp", "max_hp", "armor", "is_alive", "should_remove_on_death", "facing_right", "jump_height", "on_ground", "flying", "sprite", "item_registry", "width", "height", "animator", "entity_manager", "did_collide_x", "did_collide_y")

    def __init__(
        self, 
        x: float, y: float, vx: float, vy: float, max_speed: float,
        hp: int, max_hp: int, armor: int, is_alive: bool = True, should_remove_on_death: bool = False,
        facing_right: bool = True, 
        jump_height: int = -10, on_ground: bool = True, flying: bool = False,
        sprite: str = None, item_registry=None,
        width: float = 1.0, height: float = 2.0,
        animator: EntityAnimator = None,
        entity_manager=None,
        did_collide_x=False, did_collide_y=False,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # movement speed
        self.vx = vx
        self.vy = vy
        self.max_speed = max_speed

        self.did_collide_x = did_collide_x
        self.did_collide_y = did_collide_y

        self.hp = hp
        self.max_hp = max_hp
        self.armor = armor
        self.is_alive = is_alive
        self.should_remove_on_death = should_remove_on_death

        self.facing_right = facing_right
        self.jump_height = jump_height
        self.on_ground = on_ground
        self.flying = flying

        self.sprite = sprite
        self.item_registry = item_registry
        self.animator = animator
        self.entity_manager = entity_manager

    def __getstate__(self):
        # Only collect Entity's own slots; exclude unpicklable fields
        return {slot: getattr(self, slot) for slot in Entity.__slots__
                if slot not in ('sprite', 'item_registry', 'animator', 'entity_manager')}

    def __setstate__(self, state):
        for slot, value in state.items():
            object.__setattr__(self, slot, value)
        object.__setattr__(self, 'sprite', None)
        object.__setattr__(self, 'item_registry', None)
        object.__setattr__(self, 'animator', None)
        object.__setattr__(self, 'entity_manager', None)

    def restore_after_load(self, item_registry, sprite_registry):
        """Re-attach item_registry and reload sprites after unpickling."""
        self.item_registry = item_registry
        sprites = sprite_registry.get_sprites(self.__class__.ENTITY_KEY)
        self.animator = EntityAnimator(sprites)

    @property
    def center(self):
        return (self.x + self.width / 2, self.y - self.height / 2 + 0.5)

    def update(self, dt, camera, world, player, input=None):
        if self.hp <= 0:
            self.die()
            return
        self.animator.update(dt) if self.animator else None

        if not self.on_ground:
            self.vy += _GRAVITY * .0135 ** (1 - dt)
            if self.vy > _MAX_FALL_SPEED:
                self.vy = _MAX_FALL_SPEED

        if self.vx > self.max_speed:
            self.vx = self.max_speed
        elif self.vx < -self.max_speed:
            self.vx = -self.max_speed

        self.x += self.vx * dt
        self.did_collide_x = self._resolve_x_collision(world)

        self.y += self.vy * dt
        self.did_collide_y = self._resolve_y_collision(world)

        

    def draw(self, surface, camera):
        camera_zoom, camera_x, camera_y = camera.zoom, camera.x, camera.y
        scaled_w = int(TILE_SIZE * self.width * camera_zoom)
        scaled_h = int(TILE_SIZE * self.height * camera_zoom)

        x = (self.x * TILE_SIZE - camera_x) * camera_zoom
        y = ((self.y - self.height + 1) * TILE_SIZE - camera_y) * camera_zoom

        if self.animator:
            frame_sprite = self.animator.return_sprite()
            scaled_sprite = pygame.transform.scale(frame_sprite, (scaled_w, scaled_h))
            rotation = self.animator.get_rotation()
            if rotation != 0:
                rotated_sprite = pygame.transform.rotate(scaled_sprite, rotation)
                # re-center: rotated surface is larger than scaled_w x scaled_h
                cx = x + scaled_w / 2
                cy = y + scaled_h / 2
                blit_x = cx - rotated_sprite.get_width() / 2
                blit_y = cy - rotated_sprite.get_height() / 2
                surface.blit(rotated_sprite, (blit_x, blit_y))
            else:
                surface.blit(scaled_sprite, (x, y))
        elif self.sprite:
            scaled_sprite = pygame.transform.scale(self.sprite, (scaled_w, scaled_h))
            surface.blit(scaled_sprite, (x, y))
        else:
            pygame.draw.rect(surface, "red", (x, y, scaled_w, scaled_h))

    def _resolve_x_collision(self, world):
        head_row = int(self.y - self.height + 1)
        feet_row = int(self.y)

        if self.vx > 0:
            col = int(self.x + self.width)      # right leading edge
            for ty in (head_row, feet_row):
                if 0 <= ty < WORLD_HEIGHT and 0 <= col < WORLD_WIDTH:
                    if world.solid[ty, col]:
                        self.x = col - self.width   # right edge flush with tile left boundary
                        self.vx = 0
                        return True
        elif self.vx < 0:
            col = int(self.x)                   # left leading edge
            for ty in (head_row, feet_row):
                if 0 <= ty < WORLD_HEIGHT and 0 <= col < WORLD_WIDTH:
                    if world.solid[ty, col]:
                        self.x = col + 1.0          # left edge flush with tile right boundary
                        self.vx = 0
                        return True
        return False

    def _resolve_y_collision(self, world):
        left_col  = int(self.x)
        right_col = int(self.x + self.width - 1e-9)  # avoid checking next tile when exactly on boundary

        if self.vy >= 0:  # falling or stationary 
            ground_row = int(self.y + 1)  # entity bottom is at y+1; ground tile is that row
            for tx in (left_col, right_col):
                if 0 <= ground_row < WORLD_HEIGHT and 0 <= tx < WORLD_WIDTH:
                    if world.solid[ground_row, tx]:
                        self.y = float(ground_row - 1)  # entity bottom (y+1) flush with ground top
                        self.vy = 0
                        self.on_ground = True
                        return True
            self.on_ground = False
            return False

        else:  # moving up
            head_row = int(self.y - self.height + 1)  # entity top tile
            for tx in (left_col, right_col):
                if 0 <= head_row < WORLD_HEIGHT and 0 <= tx < WORLD_WIDTH:
                    if world.solid[head_row, tx]:
                        self.y = float(head_row + self.height)  # push feet so head clears ceiling
                        self.vy = 0
                        return True
            self.on_ground = False
            return False

    def die(self):
        self.is_alive = False

    