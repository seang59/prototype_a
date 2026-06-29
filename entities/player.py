import pygame
from core.camera import Camera
from core.input_manager import InputManager
from entities.entity import _GRAVITY, Entity
from items.equipment.equipment import Equipment
from items.placeable_block import PlaceableBlock
from items.registry.registry import ItemRegistry
from items.game_object import EquipmentSlot, GameObject
from entities.entity_animator import EntityAnimator


_PLAYER_SPEED = 20
_PLAYER_MAX_SPEED = _PLAYER_SPEED * 0.4

class Player(Entity):
    ENTITY_KEY = "player"
    __slots__ = ("inventory", "mana", "max_mana", "active_quickbar_slot", "equipement", "active_weapon_slot", "is_weapon_drawn", "show_inventory")
    def __init__(self, x, y, vx, vy, hp, max_hp, is_alive=True, should_remove_on_death=False, mana: float = 100.0, max_mana: float = 100.0, armor=0, facing_right = True, jump_height = -14, on_ground = True, flying = False, sprite = None, 
            inventory = None, show_inventory = False, equipement = None, is_weapon_drawn = True,
            item_registry: ItemRegistry = None, width: float = 1, height: float = 2,
            animator: EntityAnimator = None, entity_manager=None, did_collide_x=False, did_collide_y=False,
        ):
        super().__init__(x, y, vx, vy, _PLAYER_MAX_SPEED, hp, max_hp, armor, is_alive, should_remove_on_death, facing_right, jump_height, on_ground, flying, sprite, item_registry, width, height, animator, entity_manager, did_collide_x, did_collide_y)

        self.inventory = inventory if inventory is not None else Inventory() 
        self.show_inventory = show_inventory
        self.active_quickbar_slot = 0

        self.equipement = equipement if equipement is not None else Equipement()
        self.active_weapon_slot = 0
        self.is_weapon_drawn = is_weapon_drawn

        self.mana = mana
        self.max_mana = max_mana

        self.equipement.equip_item(self.item_registry.create("lightning_quiver"), self.equipement.weapon2_slot)    #TODO
        self.equipement.equip_item(self.item_registry.create("the_first_bow"), self.equipement.weapon1_slot)  
        self.inventory.add_item(self.item_registry.create("dirt_block"), 100)
        self.inventory.items[9].add_item(self.item_registry.create("stone_block"), 50)

    def __getstate__(self):
        state = super().__getstate__()  # Entity slots minus sprite/item_registry
        state.update({slot: getattr(self, slot) for slot in Player.__slots__})
        return state

    def __setstate__(self, state):
        player_state = {slot: state.pop(slot) for slot in Player.__slots__ if slot in state}
        super().__setstate__(state)  # restores Entity slots, nulls sprite/item_registry
        for slot, value in player_state.items():
            object.__setattr__(self, slot, value)

    def restore_after_load(self, item_registry, sprite_registry):
        super().restore_after_load(item_registry, sprite_registry)
        for slot in self.inventory.items:
            if slot.item:
                slot.item.sprite = item_registry.get_sprite(slot.item.id)
        for eq_slot in [
            self.equipement.head_slot, self.equipement.chest_slot,
            self.equipement.legs_slot, self.equipement.feet_slot,
            self.equipement.trinket1_slot, self.equipement.trinket2_slot,
            self.equipement.weapon1_slot, self.equipement.weapon2_slot,
        ]:
            if eq_slot.item:
                eq_slot.item.sprite = item_registry.get_sprite(eq_slot.item.id)

    def update(self, dt, camera: Camera, world, player, input: InputManager):
        super().update(dt, camera, world, player, input)

        if self.equipement.weapon1_slot.get_item():
            self.equipement.weapon1_slot.get_item().update(dt)
        if self.equipement.weapon2_slot.get_item():
            self.equipement.weapon2_slot.get_item().update(dt)

        if not self.is_weapon_drawn:
            if input.is_just_pressed(pygame.K_1):
                self.active_quickbar_slot = 0
            elif input.is_just_pressed(pygame.K_2):
                self.active_quickbar_slot = 1   
            elif input.is_just_pressed(pygame.K_3):
                self.active_quickbar_slot = 2
            elif input.is_just_pressed(pygame.K_4):
                self.active_quickbar_slot = 3
            elif input.is_just_pressed(pygame.K_5):
                self.active_quickbar_slot = 4
            elif input.is_just_pressed(pygame.K_6):
                self.active_quickbar_slot = 5
            elif input.is_just_pressed(pygame.K_7):
                self.active_quickbar_slot = 6
            elif input.is_just_pressed(pygame.K_8):
                self.active_quickbar_slot = 7
        if self.is_weapon_drawn:
            if input.is_just_pressed(pygame.K_1):
                self.active_weapon_slot = 0
            elif input.is_just_pressed(pygame.K_2):
                self.active_weapon_slot = 1
        if input.is_just_pressed(pygame.K_q):
            self.is_weapon_drawn = not self.is_weapon_drawn

        """INVENTORY"""
        if input.is_just_pressed(pygame.K_TAB):
            self.show_inventory = not self.show_inventory

        """MOUSE INPUT"""
        if input.is_mouse_held(pygame.BUTTON_LEFT):
            self.use_active_item(camera, world)
        if input.is_mouse_just_pressed(pygame.BUTTON_RIGHT):
            mouse_pos = input.mouse_pos()
            x, y = camera.screen_to_tile(mouse_pos)
            self.entity_manager.spawn_enemy(x, y, "enemy") #TODO remove

        """MOVEMENT"""
        if (input.is_just_pressed(pygame.K_SPACE) and self.on_ground) or (input.is_just_pressed(pygame.K_w) and self.on_ground):
            self.vy = self.jump_height
            self.on_ground = False

        moving_left = input.is_held(pygame.K_a)
        moving_right = input.is_held(pygame.K_d)
        if moving_left and moving_right:
            moving_left = False
            moving_right = False

        # friction
        if not (moving_left or moving_right) and self.on_ground:
            self.animator.set_animation_state("idle")
            self.vx *= .93 ** (1 - dt)  
        if self.vx < .01 and self.vx > -.01:
            self.vx = 0

        if moving_left:
            self.animator.set_animation_state("run", facing_right=False) if self.on_ground else self.animator.set_animation_state("jump", facing_right=False)
            self.vx -= _PLAYER_SPEED * dt 
            self.facing_right = False
            if self.vx > 0:
                self.vx -= _PLAYER_SPEED * dt * 4  # apply extra deceleration when changing direction        
        if moving_right:
            self.animator.set_animation_state("run", facing_right=True) if self.on_ground else self.animator.set_animation_state("jump", facing_right=True)
            self.vx += _PLAYER_SPEED * dt 
            self.facing_right = True
            if self.vx < 0:
                self.vx += _PLAYER_SPEED * dt * 4  
        
    def draw(self, surface, camera):
        super().draw(surface, camera)

    def get_active_slot_item(self):
        if self.is_weapon_drawn:
            if self.active_weapon_slot == 0:
                return self.equipement.weapon1_slot.get_item()
            elif self.active_weapon_slot == 1:
                return self.equipement.weapon2_slot.get_item()
        else:
            if 0 <= self.active_quickbar_slot < len(self.inventory.items):
                return self.inventory.items[self.active_quickbar_slot].get_item()
        return None
    
    def use_active_item(self, camera, world):
        item = self.get_active_slot_item()

        if item:
            success = item.use(self, camera, world, self.entity_manager)
            print(f"Using item: {item.name if success else 'Failed to use item: ' + item.name}")

            if isinstance(item, PlaceableBlock) and success:
                self.inventory.remove_item(self.active_quickbar_slot)

class Inventory:
    def __init__(self):
        self.items = [InventorySlot() for i in range(40)]

    def add_item(self, item: GameObject, count=1):
        for slot in self.items:
            if not slot.is_empty() and slot.can_stack(item, count):
                if slot.count + count > item.stack_size:
                    remaining_count = slot.count + count - item.stack_size
                    slot.add_item(item, item.stack_size)
                    self.add_item(item, remaining_count)  # RECURSION W 
                else:
                    slot.add_item(item, slot.count + count)
                return True

            if slot.is_empty():
                if count > item.stack_size:
                    slot.add_item(item, item.stack_size)
                    self.add_item(item, count - item.stack_size)  # RECURSION W
                else:
                    slot.add_item(item, count)  
                return True
        return False  # Inventory is full
    
    def remove_item(self, slot_index: int):
        if 0 <= slot_index < len(self.items):
            slot = self.items[slot_index]
            if not slot.is_empty():
                slot.remove_item()
                return True

        return False  # Item slot empty or index out of range
    
    def get_item(self, slot_index: int):
        if 0 <= slot_index < len(self.items):
            return self.items[slot_index].item
        return None  # Index out of range

    def get_stack_count(self, slot_index: int):
        if 0 <= slot_index < len(self.items):
            return self.items[slot_index].count
        return None  # Index out of range

class InventorySlot:
    def __init__(self, item: GameObject = None, count=0):
        self.item = item
        self.count = count

    def is_empty(self):
        return self.item is None 
    
    def add_item(self, item: GameObject, count=0):
        self.item = item
        self.count = count

    def remove_item(self):
        if not self.is_empty():
            self.count -= 1
            if self.count <= 0:
                self.item = None
                self.count = 0

    def can_stack(self, item: GameObject, amount_of_items_to_add = 0):
        return self.item.id == item.id and self.count + amount_of_items_to_add <= item.stack_size
    
    def get_item(self):
        return self.item
    
class Equipement: #TODO
    def __init__(self, 
        head = None, chest = None, legs = None, feet = None, 
        trinket1 = None, trinket2 = None, 
        weapon1 = None, weapon2 = None
    ):
        self.head_slot = head if head else EquipementSlot(EquipmentSlot.HEAD)
        self.chest_slot = chest if chest else EquipementSlot(EquipmentSlot.CHEST)
        self.legs_slot = legs if legs else EquipementSlot(EquipmentSlot.LEGS)
        self.feet_slot = feet if feet else EquipementSlot(EquipmentSlot.FEET)
        self.trinket1_slot = trinket1 if trinket1 else EquipementSlot(EquipmentSlot.TRINKET)
        self.trinket2_slot = trinket2 if trinket2 else EquipementSlot(EquipmentSlot.TRINKET)
        self.weapon1_slot = weapon1 if weapon1 else EquipementSlot(EquipmentSlot.WEAPON)
        self.weapon2_slot = weapon2 if weapon2 else EquipementSlot(EquipmentSlot.WEAPON)

    def equip_item(self, item: Equipment, slot: EquipmentSlot):
        if item.is_equipment_type(slot.slot_type):
            slot.item = item
        else:
            pass

    def unequip_item(self, slot: EquipmentSlot):
        slot.item = None

    def get_equipment_bonuses(self, slot: EquipmentSlot):
        pass #TODO
    
    def get_weapon_slots(self, slot: int):
        if slot == 1:
            return self.weapon1_slot.get_item()
        elif slot == 2:
            return self.weapon2_slot.get_item()
        else:
            raise ValueError("Invalid weapon slot. Must be 1 or 2.")
            
class EquipementSlot:
    def __init__(self, slot_type: EquipmentSlot, item: GameObject = None):
        self.slot_type = slot_type
        self.item = item
    
    def get_item(self):
        return self.item

    



        