import pygame
from core.ui.healthbar import HealthBar
from core.ui.inventory import InventoryUI
from core.ui.manabar import ManaBar
from core.ui.quickbar import Quickbar
from core.ui.weapon_slots import WeaponSlots
from entities.player import Player
from core.states.play import PlayState
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from core.ui.ui_elements.button import Button


class UIManager:
    def __init__(self, game, clock):
        self.game = game

        # menu state elements
        self.play_button = None
        self.quit_button = None

        # play state elements
        self.health_bar = None
        self.mana_bar = None
        self.quickbar = None
        self.inventory = None
        self.weapon_slots = None
        self.player_stat_font = None
        self.player_stat_font_outline = None

        # FPS counter — always active regardless of state
        self.show_fps = True
        self.fps_font = pygame.font.SysFont("bahnschrift", 22)
        self.clock = clock

    # PlayState hooks

    def on_enter_play(self, player: Player):
        self.player_stat_font = pygame.font.SysFont("bahnschrift", 18)
        self.player_stat_font_outline = pygame.font.SysFont("bahnschrift", 18)
        self.health_bar = HealthBar(player)
        self.mana_bar = ManaBar(player)
        self.quickbar = Quickbar(player)
        self.inventory = InventoryUI(player)
        self.weapon_slots = WeaponSlots(player)

    def on_exit_play(self):
        self.health_bar = None
        self.mana_bar = None
        self.quickbar = None
        self.inventory = None
        self.weapon_slots = None
        self.player_stat_font = None
        self.player_stat_font_outline = None

    # TitleState hooks

    def on_enter_title(self):
        self.play_button = Button(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 25, 300, 50, "Play", lambda: self.game.state_manager.enter_state(PlayState(self.game), self.game))
        self.quit_button = Button(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 50, 300, 50, "Quit", lambda: self.game.quit())

    def on_exit_title(self):
        self.play_button = None
        self.quit_button = None

    # Update / Draw

    def update(self, player: Player):
        if self.health_bar is not None:
            self.health_bar.update(player)
            self.mana_bar.update(player)
            self.quickbar.update(player)
            self.weapon_slots.update(player)
            self.inventory.update(player)

        if self.play_button is not None:
            mouse_pos = self.game.input_manager.mouse_pos()
            mouse_pressed = self.game.input_manager.is_mouse_just_pressed(pygame.BUTTON_LEFT)
            self.play_button.update(mouse_pos, mouse_pressed)
            if self.quit_button is not None:
                self.quit_button.update(mouse_pos, mouse_pressed)

    def draw(self, surface):
        if self.health_bar is not None:
            self.health_bar.draw(surface, (SCREEN_WIDTH // 2) - 150, SCREEN_HEIGHT - 68, 300, 30, (self.player_stat_font, self.player_stat_font_outline))
            self.mana_bar.draw(surface, (SCREEN_WIDTH // 2) - 150, SCREEN_HEIGHT - 40, 300, 30, (self.player_stat_font, self.player_stat_font_outline))

            self.quickbar.draw(surface, (SCREEN_WIDTH // 2) - 150, SCREEN_HEIGHT - 100, 300, 30, (self.player_stat_font, self.player_stat_font_outline))
            self.inventory.draw(surface, (SCREEN_WIDTH // 2) - 150, SCREEN_HEIGHT - 130, 300, 30, (self.player_stat_font, self.player_stat_font_outline))

            self.weapon_slots.draw(surface, (SCREEN_WIDTH // 2) - 191, SCREEN_HEIGHT - 86, 38, 76, (self.player_stat_font, self.player_stat_font_outline))

        if self.play_button is not None:
            self.play_button.draw(surface, self.fps_font)
            self.quit_button.draw(surface, self.fps_font)

        if self.show_fps:
            fps_surf = self.fps_font.render(f"{self.clock.get_fps():.0f} FPS", True, (255, 255, 0))
            surface.blit(fps_surf, (SCREEN_WIDTH - fps_surf.get_width() - 8, 8))