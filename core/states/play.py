from __future__ import annotations
from typing import TYPE_CHECKING
import pygame

from core.states.state import State
from entities.entity_manager import EntityManager
from world.world import World

if TYPE_CHECKING:
    from core.game import Game



class PlayState(State):
    def __init__(self, game: Game):
        game.screen.fill((0, 0, 0))
        pygame.display.flip()
        self.is_paused = False

    def update(self, dt, game):
        game.input_manager.update()
        if game.input_manager.is_just_pressed(pygame.K_ESCAPE):
                self.is_paused = not self.is_paused
                if self.is_paused:
                    game.ui_manager.on_enter_pause()
                else:
                    game.ui_manager.on_exit_pause()


        if self.is_paused:
            game.ui_manager.update(self.entity_manager.get_player())
            return

        mouse_coords = game.input_manager.mouse_pos()         # TODO: FOLLOW PLAYER
        player_center = self.entity_manager.get_player_center()
        #game.camera.update(game.camera.screen_to_world(mouse_coords), game.input_manager)
        game.camera.update(player_center, game.input_manager)

        game.world.update(dt, game.camera)
        self.entity_manager.update(dt, game.camera, game.world, game.input_manager)
        game.ui_manager.update(self.entity_manager.get_player())

    def draw(self, surface, game):
        surface.fill((135, 206, 235))  # sky blue background, will be covered by background manager
        # DRAW STUFF HERE

        game.world.draw(surface, game.camera)
        self.entity_manager.draw(surface, game.camera)

        # UI
        game.ui_manager.draw(surface)

        # ~~~~~~~~~~~~~~~~~~
        pygame.display.flip()

    def on_enter(self, game: Game):
        if game.save_data:
            game.world = World(game.item_registry, seed=game.save_data.seed, modified_tiles=game.save_data.modified_tiles)
        else:
            game.world = World(game.item_registry)
        self.entity_manager = EntityManager(game.item_registry)

        if game.save_data and game.save_data.entities:
            for entity in game.save_data.entities:
                entity.restore_after_load(game.item_registry, self.entity_manager.sprite_registry)
                entity.entity_manager = self.entity_manager
                self.entity_manager.spawn(entity)
        else:
            self._setup_entities(*game.world.player_spawn)

        game.ui_manager.on_enter_play(self.entity_manager.get_player())
        game.camera.snap_to(self.entity_manager.get_player_center())

    def on_exit(self, game):
        game.ui_manager.on_exit_play()
        game.save_manager.save(game.world, self.entity_manager)

    def _setup_entities(self, x, y):
        if not self.entity_manager.get_player():
            self.entity_manager.spawn_player(x, y)