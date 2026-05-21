from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from core.states.state import State
from core.states.play import PlayState

if TYPE_CHECKING:
    from core.game import Game

class TitleState(State):
    def __init__(self, game: Game):
        pass

    def update(self, dt, game: Game):
        game.input_manager.update()
        if game.input_manager.should_quit() or game.input_manager.is_just_pressed(pygame.K_ESCAPE):
                self.on_exit(game)
                game.running = False
                game.quit()

        if game.input_manager.is_mouse_just_pressed(pygame.BUTTON_RIGHT):
            game.state_manager.enter_state(PlayState(game), game)

        game.ui_manager.update(None)

    def draw(self, surface, game: Game):
        surface.fill((10, 255, 235))  # sky blue background, will be covered by background manager
        # DRAW STUFF HERE

        game.ui_manager.draw(surface)

        # ~~~~~~~~~~~~~~~~~~
        pygame.display.flip()

    def on_enter(self, game: Game):
        game.ui_manager.on_enter_title()

    def on_exit(self, game: Game):
        game.ui_manager.on_exit_title()