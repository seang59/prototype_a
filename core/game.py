import pygame
import sys

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from world.world import World
from world.generator import TileID
from core.camera import Camera
from entities.entity_manager import EntityManager
from entities.player import Player
from core.ui.ui_manager import UIManager
from items.registry.registry import ItemRegistry
from core.input_manager import InputManager
from core.save_manager import SaveManager


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("My Game")
        self.clock = pygame.time.Clock()
        self.running = True

        self.input_manager = InputManager()
        self.item_registry = ItemRegistry()
        self.camera = Camera()
        self.save_manager = SaveManager()

        save_data = self.save_manager.load()
        if save_data:
            self.world = World(self.item_registry, seed=save_data.seed, modified_tiles=save_data.modified_tiles)
        else:
            self.world = World(self.item_registry)

        self.entity_manager = EntityManager(self.item_registry)
        if save_data and save_data.entities:
            for entity in save_data.entities:
                entity.restore_after_load(self.item_registry, self.entity_manager.sprite_registry)
                entity.entity_manager = self.entity_manager
                self.entity_manager.spawn(entity)
        else:
            self._setup_entities(*self.world.player_spawn) 

        self.ui_manager = UIManager(self.entity_manager.get_player(), self.clock)
        

    def run(self):
        camera = self.camera

        while self.running:
            dt = self.clock.tick(FPS) / 1000  # delta time in seconds

            self.update(dt, camera, self.world, self.input_manager)
            self.draw(self.screen, camera)

            if self.input_manager.should_quit() or self.input_manager.is_just_pressed(pygame.K_ESCAPE):
                self.running = False
                self.quit()
            
    def update(self, dt, camera, world, input_manager):
        input_manager.update()

        mouse_coords = input_manager.mouse_pos()         # TODO: FOLLOW PLAYER
        player_center = self.entity_manager.get_player_center()
        #self.camera.update(self.camera.screen_to_world(mouse_coords), input_manager)
        self.camera.update(player_center, input_manager)

        world.update(dt, camera)
        self.entity_manager.update(dt, camera, world, input_manager)
        self.ui_manager.update(self.entity_manager.get_player())

    def draw(self, surface, camera):
        self.screen.fill((135, 206, 235))  # sky blue background, will be covered by background manager
        # DRAW STUFF HERE

        self.world.draw(surface, camera)
        self.entity_manager.draw(surface, camera)

        # UI
        self.ui_manager.draw(surface)

        # ~~~~~~~~~~~~~~~~~~
        pygame.display.flip()

    def quit(self): #TODO
        self.save_manager.save(self.world, self.entity_manager)
        pygame.quit()
        sys.exit()

    def _setup_entities(self, x, y):
        if not self.entity_manager.get_player():
            self.entity_manager.spawn_player(x, y)
    
