from constants import TICK_RATE, WORLD_WIDTH, WORLD_HEIGHT, TILE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, CHUNK_SIZE
from world.background_manager import BackgroundManager
from world.generator import Generator, TileID
from items.registry.registry import ItemRegistry
from collections import defaultdict
import pygame
import random
import numpy as np
from numba import njit


_GRASS_TICKS_PER_FRAME = 10 * TICK_RATE

_MIN_MASS       = 0.05   # cells below this are zeroed; 0.05 * 32px = 1.6px, always renders
_MAX_MASS       = 1.0
_MAX_COMPRESS   = 0.02
_MAX_FLOW       = 1.0
_MAX_HORIZ_FLOW = 0.25

@njit
def _stable_state(total):
    if total <= _MAX_MASS:
        return total
    elif total < 2.0 * _MAX_MASS + _MAX_COMPRESS:
        return (_MAX_MASS * _MAX_MASS + total * _MAX_COMPRESS) / (_MAX_MASS + _MAX_COMPRESS)
    else:
        return (total + _MAX_COMPRESS) / 2.0


@njit
def _water_step_mass(mass, solid, y0, y1, x0, x1, left_to_right):
    new_mass = mass.copy()

    for wy in range(y1 - 1, y0 - 1, -1):
        wx_start = x0      if left_to_right else x1 - 1
        wx_stop  = x1      if left_to_right else x0 - 1
        wx_step  = 1       if left_to_right else -1

        wx = wx_start
        while wx != wx_stop:
            if not solid[wy, wx]:
                m = new_mass[wy, wx]
                if m > _MIN_MASS:
                    # fall down
                    if wy + 1 < y1 and not solid[wy + 1, wx]:
                        below = new_mass[wy + 1, wx]
                        if below < _MAX_MASS:
                            flow = _stable_state(m + below) - below
                            flow = min(min(flow, m), _MAX_FLOW)
                            flow = max(flow, 0.0)
                            new_mass[wy,     wx] -= flow
                            new_mass[wy + 1, wx] += flow
                            m -= flow

                    # flow left
                    if wx - 1 >= x0 and not solid[wy, wx - 1]:
                        diff = m - new_mass[wy, wx - 1]
                        if diff > 0.0:
                            flow = min(diff / 2.0, _MAX_HORIZ_FLOW)
                            new_mass[wy, wx    ] -= flow
                            new_mass[wy, wx - 1] += flow
                            m -= flow

                    # flow right
                    if wx + 1 < x1 and not solid[wy, wx + 1]:
                        diff = m - new_mass[wy, wx + 1]
                        if diff > 0.0:
                            flow = min(diff / 2.0, _MAX_HORIZ_FLOW)
                            new_mass[wy, wx    ] -= flow
                            new_mass[wy, wx + 1] += flow

            wx += wx_step

    # zero sub-threshold cells
    for wy in range(y0, y1):
        for wx in range(x0, x1):
            if not solid[wy, wx] and new_mass[wy, wx] < _MIN_MASS:
                new_mass[wy, wx] = 0.0

    mass[y0:y1, x0:x1] = new_mass[y0:y1, x0:x1]


"""SPRITE VARIANT FUNCTIONS"""
@njit
def _variant_grass_corner(world_arr, wy, wx, cache=None):
    """Left corner=0, flat=1, right corner=2 based on horizontal neighbors."""
    left_air  = wx > 0             and world_arr[wy, wx - 1] == TileID.AIR
    right_air = wx < WORLD_WIDTH-1 and world_arr[wy, wx + 1] == TileID.AIR
    top_air    = wy > 0 and wx < WORLD_WIDTH-1 and world_arr[wy - 1, wx] == TileID.AIR
    bottom_air    = wy > 0 and wx < WORLD_WIDTH-1 and world_arr[wy + 1, wx] == TileID.AIR

    top_grass = (wy > 0 and wx < WORLD_WIDTH-1 and world_arr[wy - 1, wx] == TileID.GRASS)
    left_grass= (wx > 0                 and world_arr[wy, wx - 1] == TileID.GRASS)
    right_grass=(wx < WORLD_WIDTH-1     and world_arr[wy, wx + 1] == TileID.GRASS)

    # inside corners
    if top_grass and left_grass:
        if world_arr[wy - 1, wx - 1] == TileID.GRASS:
                return (3, 2)
        return (5, 2) 
    if top_grass and right_grass:
        return (3, 2)
    
    # vertical edges
    if not top_air and not bottom_air and not right_air and left_air:
        return (0, 1)  
    if not top_air and not bottom_air and right_air and not left_air:
        return (2, 1)
    
    # corners
    if top_air and bottom_air and left_air and not right_air:
        return (0, 0)
    if top_air and bottom_air and not left_air and right_air:
        return (2, 0)
    if left_air and not right_air and bottom_air and not top_air:
        return (0, 2)
    if not left_air and right_air and bottom_air and not top_air:
        return (2, 2)
    if left_air and not right_air:
        return (0, 0)
    if not left_air and right_air and bottom_air:
        return (2, 2)
    if not left_air and right_air:
        return (2, 0)
    return (1, 0)

@njit
def _variant_dirt_corner(world_arr, wy, wx, cache=None):
    """Left corner=0, flat=1, right corner=2 based on horizontal neighbors."""
    left_air  = wx > 0             and world_arr[wy, wx - 1] == TileID.AIR
    right_air = wx < WORLD_WIDTH-1 and world_arr[wy, wx + 1] == TileID.AIR
    top_air    = wy > 0 and wx < WORLD_WIDTH-1 and world_arr[wy - 1, wx] == TileID.AIR
    bottom_air    = wy > 0 and wx < WORLD_WIDTH-1 and world_arr[wy + 1, wx] == TileID.AIR

    # vertical edges
    if not top_air and not bottom_air and not right_air and left_air:
        return (0, 1)  
    if not top_air and not bottom_air and right_air and not left_air:
        return (2, 1)
    if not top_air and bottom_air and not right_air and not left_air:
        return (1, 2)
    if top_air and not bottom_air and not right_air and not left_air:
        return (1, 0)
    
    # corners
    if top_air and bottom_air and left_air and not right_air:
        return (0, 0)
    if top_air and bottom_air and not left_air and right_air:
        return (2, 0)
    if left_air and not right_air and bottom_air and not top_air:
        return (0, 2)
    if not left_air and right_air and bottom_air and not top_air:
        return (2, 2)
    if left_air and not right_air:
        return (0, 0)
    if not left_air and right_air and bottom_air:
        return (2, 2)
    if not left_air and right_air:
        return (2, 0)
    return (1, 1)

_SPRITE_VARIANT_FN: dict[str, callable] = {
    "grass_corner": _variant_grass_corner,
    "dirt_corner": _variant_dirt_corner,
}


class World:
    def __init__(self, registry: ItemRegistry, seed = None, modified_tiles: dict[tuple[int, int], TileID] = None):
        self.generator = Generator(seed)
        self.world = self.generator.generate()
        self.player_spawn = self.generator.player_spawn

        water_mask = self.world == TileID.WATER
        self.world[water_mask] = TileID.AIR
        self.water_mass = np.zeros(self.world.shape, dtype=np.float32)
        self.water_mass[water_mask] = 1.0
        self.solid = (self.world != TileID.AIR).astype(np.bool_)

        self.TILE_DATA = {i: registry.get_tile_data(i) for i in range(len(TileID))}

        self.chunks: dict[tuple[int, int], pygame.Surface] = {}
        # Maps chunk_key -> set of (world_y, world_x) tiles needing a patch
        self._dirty_tiles: defaultdict[tuple[int, int], set] = defaultdict(set)
        self._scaled_sprites: dict[int, pygame.Surface] = {}
        self._last_zoom: float | None = None
        self._vp: tuple[int, int, int, int] = (0, WORLD_WIDTH, 0, WORLD_HEIGHT)

        self.modified_tiles: dict[tuple[int, int], TileID] = modified_tiles if modified_tiles else {}
        if modified_tiles:
            self._reconstruct_saved_world(self.modified_tiles)

        self.water_timer = 0
        self.water_update_interval = 0.2  # update water 5x per second
        self._water_scan_ltr = True
        self.grass_y_min, self.grass_y_max = self.generator.grass_y_bounds

        self._settle_water()

        self.active_biome = None
        self.background_manager = BackgroundManager(grass_y=(self.grass_y_min * TILE_SIZE))

    def _reconstruct_saved_world(self, modified_tiles: dict[tuple[int, int], TileID]):
        for (y, x), tile_id in modified_tiles.items():
            self._set_tile(y, x, tile_id)

    def _settle_water(self, max_iterations: int = 100) -> None:
        for i in range(max_iterations):
            before = self.water_mass.copy()
            ltr = (i % 2 == 0)
            _water_step_mass(self.water_mass, self.solid,
                             0, WORLD_HEIGHT, 0, WORLD_WIDTH, ltr)
            if np.allclose(self.water_mass, before, atol=1e-4):
                break

    def update(self, dt, camera):
        camera_zoom, camera_x, camera_y = camera.zoom, camera.x, camera.y
        
        visible_tiles_wide = SCREEN_WIDTH / camera_zoom
        visible_tiles_tall = SCREEN_HEIGHT / camera_zoom

        viewport_tile_left   = max(0, int(camera_x // TILE_SIZE))
        viewport_tile_right  = min(WORLD_WIDTH,  int((camera_x + visible_tiles_wide) // TILE_SIZE) + 1)
        viewport_tile_top    = max(0, int(camera_y // TILE_SIZE))
        viewport_tile_bottom = min(WORLD_HEIGHT, int((camera_y + visible_tiles_tall) // TILE_SIZE) + 1)
        self._vp = (viewport_tile_left, viewport_tile_right, viewport_tile_top, viewport_tile_bottom)

        # update region = 3x viewport (one viewport of margin on each side)
        viewport_width_tiles  = viewport_tile_right - viewport_tile_left
        viewport_height_tiles = viewport_tile_bottom - viewport_tile_top
        update_left   = max(0, viewport_tile_left   - viewport_width_tiles)
        update_right  = min(WORLD_WIDTH,  viewport_tile_right  + viewport_width_tiles)
        update_top    = max(0, viewport_tile_top    - viewport_height_tiles)
        update_bottom = min(WORLD_HEIGHT, viewport_tile_bottom + viewport_height_tiles)

        self.water_timer += dt
        if self.water_timer >= self.water_update_interval:
            self.water_timer -= self.water_update_interval
            self.update_water(update_top, update_bottom, update_left, update_right)

        self.update_grass(update_left, update_right)

    def draw(self, surface, camera):
        self.background_manager.draw(surface, camera)

        camera_zoom, camera_x, camera_y = camera.zoom, camera.x, camera.y
        scaled_tile_size = int(TILE_SIZE * camera_zoom)
        chunk_surface_size = CHUNK_SIZE * scaled_tile_size
        chunks = self.chunks
        dirty_tiles = self._dirty_tiles

        if camera_zoom != self._last_zoom:
            chunks.clear()
            self._scaled_sprites.clear()
            self._last_zoom = camera_zoom

        viewport_tile_left, viewport_tile_right, viewport_tile_top, viewport_tile_bottom = self._vp
        first_visible_chunk_x = viewport_tile_left  // CHUNK_SIZE
        last_visible_chunk_x  = max(first_visible_chunk_x, (viewport_tile_right  - 1) // CHUNK_SIZE)
        first_visible_chunk_y = viewport_tile_top   // CHUNK_SIZE
        last_visible_chunk_y  = max(first_visible_chunk_y, (viewport_tile_bottom - 1) // CHUNK_SIZE)

        for chunk_row in range(first_visible_chunk_y, last_visible_chunk_y + 1):
            for chunk_col in range(first_visible_chunk_x, last_visible_chunk_x + 1):
                chunk_key = (chunk_row, chunk_col)
                if chunk_key not in chunks:
                    self._rebuild_chunk(chunk_row, chunk_col, scaled_tile_size, chunk_surface_size)
                elif chunk_key in dirty_tiles:
                    for (wy, wx) in dirty_tiles.pop(chunk_key):
                        self._patch_tile(wy, wx, scaled_tile_size)

                screen_x = int((chunk_col * CHUNK_SIZE * TILE_SIZE - camera_x) * camera_zoom)
                screen_y = int((chunk_row * CHUNK_SIZE * TILE_SIZE - camera_y) * camera_zoom)
                surface.blit(chunks[chunk_key], (screen_x, screen_y))

    def _rebuild_chunk(self, chunk_row: int, chunk_col: int, scaled_tile_size: int, chunk_surface_size: int) -> None:
        chunk_surf = pygame.Surface((chunk_surface_size, chunk_surface_size))
        chunk_surf.fill((0, 0, 0))  
        chunk_surf.set_colorkey((0, 0, 0))

        water_surf = pygame.Surface((chunk_surface_size, chunk_surface_size), pygame.SRCALPHA)

        world_tile_y_start = chunk_row * CHUNK_SIZE
        world_tile_x_start = chunk_col * CHUNK_SIZE

        for tile_row in range(CHUNK_SIZE):
            world_y = world_tile_y_start + tile_row
            if world_y >= WORLD_HEIGHT:
                break
            for tile_col in range(CHUNK_SIZE):
                world_x = world_tile_x_start + tile_col
                if world_x >= WORLD_WIDTH:
                    break
                tile  = self.world[world_y, world_x]
                water = self.water_mass[world_y, world_x]

                if tile == TileID.AIR and water < _MIN_MASS:
                    continue

                draw_x = tile_col * scaled_tile_size
                draw_y = tile_row * scaled_tile_size

                if tile != TileID.AIR:
                    tile_data = self.TILE_DATA[tile]
                    color  = tile_data["color"]
                    sprite = tile_data["sprite"]
                    if color and not sprite:
                        pygame.draw.rect(chunk_surf, color, (draw_x, draw_y, scaled_tile_size, scaled_tile_size))
                    elif sprite:
                        variant_type = tile_data.get("sprite_variant")
                        if variant_type:
                            col = _SPRITE_VARIANT_FN[variant_type](self.world, world_y, world_x)
                            variant_key = (tile, col)
                            if variant_key not in self._scaled_sprites:
                                sub = sprite.subsurface((col[0] * TILE_SIZE, col[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                                self._scaled_sprites[variant_key] = pygame.transform.scale(sub, (scaled_tile_size, scaled_tile_size))
                            chunk_surf.blit(self._scaled_sprites[variant_key], (draw_x, draw_y))
                        else:
                            if tile not in self._scaled_sprites:
                                self._scaled_sprites[tile] = pygame.transform.scale(
                                    sprite, (scaled_tile_size, scaled_tile_size)
                                )
                            chunk_surf.blit(self._scaled_sprites[tile], (draw_x, draw_y))


                if water >= _MIN_MASS:
                    fill_h = int(min(1.0, water) * scaled_tile_size)
                    if fill_h > 0:
                        pygame.draw.rect(water_surf, (30, 80, 200, 155),
                                         (draw_x, draw_y + (scaled_tile_size - fill_h), scaled_tile_size, fill_h))

        chunk_surf.blit(water_surf, (0, 0))
        self.chunks[(chunk_row, chunk_col)] = chunk_surf

    def _patch_tile(self, world_y: int, world_x: int, scaled_tile_size: int) -> None:
        """Redraw a single tile on an already-cached chunk"""
        chunk_key = (world_y // CHUNK_SIZE, world_x // CHUNK_SIZE)
        if chunk_key not in self.chunks:
            return
        draw_x = (world_x % CHUNK_SIZE) * scaled_tile_size
        draw_y = (world_y % CHUNK_SIZE) * scaled_tile_size
        chunk_surf = self.chunks[chunk_key]
        chunk_surf.fill((0, 0, 0), (draw_x, draw_y, scaled_tile_size, scaled_tile_size))

        tile  = self.world[world_y, world_x]
        water = self.water_mass[world_y, world_x]

        if tile != TileID.AIR:
            if world_y > 0:
                if tile == TileID.GRASS and self.solid[world_y - 1, world_x]:
                    self._set_tile(world_y, world_x, TileID.DIRT)
                    tile = TileID.DIRT

            tile_data = self.TILE_DATA[tile]
            color  = tile_data["color"]
            sprite = tile_data["sprite"]
            if color and not sprite:
                pygame.draw.rect(chunk_surf, color, (draw_x, draw_y, scaled_tile_size, scaled_tile_size))
            elif sprite:
                variant_type = tile_data.get("sprite_variant")
                if variant_type:
                    col = _SPRITE_VARIANT_FN[variant_type](self.world, world_y, world_x)
                    variant_key = (tile, col)
                    if variant_key not in self._scaled_sprites:
                        sub = sprite.subsurface((col[0] * TILE_SIZE, col[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                        self._scaled_sprites[variant_key] = pygame.transform.scale(sub, (scaled_tile_size, scaled_tile_size))
                    chunk_surf.blit(self._scaled_sprites[variant_key], (draw_x, draw_y))
                else:
                    if tile not in self._scaled_sprites:
                        self._scaled_sprites[tile] = pygame.transform.scale(sprite, (scaled_tile_size, scaled_tile_size))
                    chunk_surf.blit(self._scaled_sprites[tile], (draw_x, draw_y))

        if water >= _MIN_MASS:
            fill_h = int(min(1.0, water) * scaled_tile_size)
            if fill_h > 0:
                tmp = pygame.Surface((scaled_tile_size, fill_h), pygame.SRCALPHA)
                tmp.fill((30, 80, 200, 155))
                chunk_surf.blit(tmp, (draw_x, draw_y + (scaled_tile_size - fill_h)))

    def _set_tile(self, y: int, x: int, tile_id: int) -> None:
        self.world[y, x] = tile_id
        self.solid[y, x] = (tile_id != TileID.AIR)
        self._dirty_tiles[(y // CHUNK_SIZE, x // CHUNK_SIZE)].add((y, x))
        self.modified_tiles[(y, x)] = tile_id
        for ny, nx in (
            (y-1, x), (y+1, x), (y, x-1), (y, x+1),   # cardinals
            (y-1, x-1), (y-1, x+1), (y+1, x-1), (y+1, x+1),  # diagonals
        ):
            if 0 <= ny < WORLD_HEIGHT and 0 <= nx < WORLD_WIDTH:
                self._dirty_tiles[(ny // CHUNK_SIZE, nx // CHUNK_SIZE)].add((ny, nx))

    def place_tile(self, tile_y: int, tile_x: int, tile_id: int) -> None:
        if not (0 <= tile_y < WORLD_HEIGHT and 0 <= tile_x < WORLD_WIDTH):
            return False
        if self.world[tile_y, tile_x] != TileID.AIR:
            return False
        
        self._set_tile(tile_y, tile_x, tile_id)
        if tile_id != TileID.AIR:
            self.water_mass[tile_y, tile_x] = 0.0
        return True

    def update_grass(self, region_tile_left, region_tile_right):
        sky_clearance = 17
        region_width  = region_tile_right - region_tile_left
        region_height = self.grass_y_max - self.grass_y_min + 1
        if region_width <= 0 or region_height <= 0:
            return
        for _ in range(_GRASS_TICKS_PER_FRAME):
            world_y = self.grass_y_min + random.randint(0, region_height - 1)
            world_x = region_tile_left + random.randint(0, region_width - 1)
            if self.world[world_y, world_x] != TileID.DIRT:
                continue
            sky_top = max(0, world_y - sky_clearance)
            if np.all(self.world[sky_top:world_y, world_x] == TileID.AIR):
                self._set_tile(world_y, world_x, TileID.GRASS)
                break

    def update_water(self, region_tile_top, region_tile_bottom, region_tile_left, region_tile_right):
        water = self.water_mass
        solid = self.solid
        scan_ltr = self._water_scan_ltr
        dirty_tiles = self._dirty_tiles

        before = water[region_tile_top:region_tile_bottom, region_tile_left:region_tile_right].copy()
        _water_step_mass(water, solid, region_tile_top, region_tile_bottom, region_tile_left, region_tile_right, scan_ltr)
        self._water_scan_ltr = not scan_ltr
        after = water[region_tile_top:region_tile_bottom, region_tile_left:region_tile_right]
        changed = np.argwhere(after != before)

        if len(changed):
            world_ys = (region_tile_top  + changed[:, 0]).tolist()
            world_xs = (region_tile_left + changed[:, 1]).tolist()
            for wy, wx in zip(world_ys, world_xs):
                dirty_tiles[(wy // CHUNK_SIZE, wx // CHUNK_SIZE)].add((wy, wx))
