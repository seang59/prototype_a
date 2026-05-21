from entities.ammo.ammo import Ammo
from entities.ammo.arrow import Arrow
from entities.player import Player
from .dropped_item import DroppedItem
from entities.enemy import Enemy
from entities.registry.registry import EntitySpriteRegistry
from entities.entity_animator import EntityAnimator

ENEMIES = {
    "enemy": Enemy
}

AMMO_VARIANTS = {
    "arrow": Arrow
}

class EntityManager:
    def __init__(self, item_registry=None):
        self.entities = []
        self.item_registry = item_registry
        self.sprite_registry = EntitySpriteRegistry()

    def update(self, dt, camera, world, input):
        for entity in list(self.entities):
            entity.update(dt, camera, world, self.get_player(), input)

        self.entities = [entity for entity in self.entities if not entity.should_remove_on_death]   

    def draw(self, screen, camera):
        for entity in self.entities:
            entity.draw(screen, camera)

    def spawn(self, entity):
        print(f"Spawning entity: {entity.__class__.__name__} at ({entity.x}, {entity.y})")
        self.entities.append(entity)

    def get_player(self):
        return self.entities[0] if self.entities else None
    
    def get_player_center(self):
        player = self.get_player()
        player_x = player.x + player.width / 2 if player else 0
        player_y = player.y - player.height / 2 + 0.5 if player else 0
        return (player_x, player_y)
    
    def spawn_player(self, x, y):
        if not self.get_player():
            sprites = self.sprite_registry.get_sprites(Player.ENTITY_KEY)
            player = Player(
                x, y, 0, 0, hp=100, max_hp=100, mana=100, max_mana=100,
                item_registry=self.item_registry, animator=EntityAnimator(sprites),
                entity_manager=self
            )
            self.spawn(player)

    def spawn_enemy(self, x, y, enemy_type: str):
        enemy_class = ENEMIES.get(enemy_type)
        if not enemy_class:
            raise ValueError(f"Unknown enemy type: {enemy_type}")

        sprites = self.sprite_registry.get_sprites(enemy_class.ENTITY_KEY)
        self.spawn(
            enemy_class(x, y,
                  item_registry=self.item_registry,
                  animator=EntityAnimator(sprites),
                  entity_manager=self)
        )

    def spawn_ammo(self, x, y, vx, vy, ammo_type: str, damage=0):
        ammo_class = AMMO_VARIANTS.get(ammo_type)
        if not ammo_class:
            raise ValueError(f"Unknown ammo type: {ammo_type}")

        sprites = self.sprite_registry.get_sprites(ammo_class.ENTITY_KEY)
        self.spawn(
            ammo_class(x, y, vx, vy,
                 item_registry=self.item_registry,
                 animator=EntityAnimator(sprites),
                 entity_manager=self,
                 damage=damage)
        )

    def collided_with_entity(self, entity) -> bool:
        for other in self.entities:
            if other is not entity and self.check_collision(entity, other):
                return True
        return False
    
    def collided_ammo_with_entity(self, entity, damage=0) -> bool:
        for other in self.entities:
            if other is not entity and self.check_collision(entity, other) and not isinstance(other, Player) and not isinstance(other, Ammo):
                other.hp -= damage
                return True
        return False
    
    def check_collision(self, entity1, entity2) -> bool:
        return (entity1.x < entity2.x + entity2.width and
                entity1.x + entity1.width > entity2.x and
                entity1.y - entity1.height < entity2.y and
                entity1.y > entity2.y - entity2.height)
    
    def get_entity_type(self, entity):
        if isinstance(entity, Player):
            return "player"
        elif isinstance(entity, Enemy):
            return "enemy"
        elif isinstance(entity, Ammo):
            return "ammo"
        elif isinstance(entity, DroppedItem):
            return "dropped_item"
        else:
            return "unknown"

