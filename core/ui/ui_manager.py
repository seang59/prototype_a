import pygame
from core.ui.healthbar import HealthBar
from core.ui.inventory import InventoryUI
from core.ui.manabar import ManaBar
from core.ui.quickbar import Quickbar
from core.ui.weapon_slots import WeaponSlots
from entities.player import Player
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class UIManager:
    def __init__(self, player: Player, clock):
        self.quickbar = Quickbar(player)
        self.inventory = InventoryUI(player)
        self.weapon_slots = WeaponSlots(player)
        
        self.player_stat_font = pygame.font.SysFont("bahnschrift", 16)
        self.player_stat_font_outline = pygame.font.SysFont("bahnschrift", 18)

        self.health_bar = HealthBar(player)
        self.mana_bar = ManaBar(player)
        self.player_stat_font = pygame.font.SysFont("bahnschrift", 18)

        #FPS
        self.show_fps = True
        self.fps_font = pygame.font.SysFont("bahnschrift", 22)
        self.clock = clock

    def update(self, player: Player):
        self.health_bar.update(player)
        self.mana_bar.update(player)
        self.quickbar.update(player) 
        self.weapon_slots.update(player)
        self.inventory.update(player)

    def draw(self, surface):
        self.health_bar.draw(surface, (SCREEN_WIDTH // 2) - 150, SCREEN_HEIGHT - 68, 300, 30, (self.player_stat_font, self.player_stat_font_outline))
        self.mana_bar.draw(surface, (SCREEN_WIDTH // 2) - 150, SCREEN_HEIGHT - 40, 300, 30, (self.player_stat_font, self.player_stat_font_outline))

        self.quickbar.draw(surface, (SCREEN_WIDTH // 2) - 150, SCREEN_HEIGHT - 100, 300, 30, (self.player_stat_font, self.player_stat_font_outline))
        self.inventory.draw(surface, (SCREEN_WIDTH // 2) - 150, SCREEN_HEIGHT - 130, 300, 30, (self.player_stat_font, self.player_stat_font_outline))

        self.weapon_slots.draw(surface, (SCREEN_WIDTH // 2) - 191, SCREEN_HEIGHT - 86, 38, 76, (self.player_stat_font, self.player_stat_font_outline))
        
        
        if self.show_fps:
            fps_surf = self.fps_font.render(f"{self.clock.get_fps():.0f} FPS", True, (255, 255, 0))
            surface.blit(fps_surf, (SCREEN_WIDTH - fps_surf.get_width() - 8, 8))