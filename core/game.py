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
from core.state_manager import StateManager
from core.states import PlayState, TitleState


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("My Game")
        self.clock = pygame.time.Clock()
        self.running = True

        self.world = None

        self.input_manager = InputManager()
        self.item_registry = ItemRegistry()
        self.camera = Camera()
        
        self.save_manager = SaveManager()
        self.save_data = self.save_manager.load()

        self.state_manager = StateManager()
        self.ui_manager = UIManager(self, self.clock)
        self.state_manager.enter_state(PlayState(self), self)
        
        

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000  # delta time in seconds

            self.state_manager.update(dt, self)
            self.state_manager.draw(self.screen, self)

    def quit(self): #TODO: move to state manager?
        pygame.quit()
        sys.exit()

    
    
