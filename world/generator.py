import numpy as np
import noise
import random
import hashlib
from scipy.ndimage import label
from enum import IntEnum
from constants import WORLD_WIDTH, WORLD_HEIGHT, GROUND_VARIATION, STONE_VARIATION, TRANSITION_HALF_WIDTH

class TileID(IntEnum):
    AIR = 0
    GRASS = 1
    DIRT = 2
    STONE = 3
    WATER = 4
    BEDROCK = 5
    COPPER_ORE = 6
    IRON_ORE = 7
    GOLD_ORE = 8
    DIAMOND_ORE = 9
    SHATTERITE_ORE = 10

ORE_CONFIGS = [
    # (tile, min_depth_ratio, large_scale, small_scale, large_thresh, small_thresh, seed_l, seed_s)
    (TileID.SHATTERITE_ORE, 0.75, 6.5, 4.0, 0.414, 0.396, 18, 19),
    (TileID.DIAMOND_ORE,    0.70, 7.0, 4.0, 0.413, 0.395, 18, 19),
    (TileID.GOLD_ORE,       0.55, 8.0, 5.0, 0.40,  0.38,  16, 17),
    (TileID.IRON_ORE,       0.42, 10.0, 6.0, 0.39,  0.36,  14, 15),
    (TileID.COPPER_ORE,     0.00, 12.0, 8.0, 0.39,  0.35,  12, 13),
]

class Generator:
    def __init__(
        self,
        seed = None,
        width = WORLD_WIDTH,
        height = WORLD_HEIGHT,
        scale = 80.0,
        octaves = 6,
        persistence = 0.5,
        lacunarity = 2.0,
    ):
        self.width = width
        self.height = height

        self.seed = (seed % 255) if seed is not None else random.randint(0, 255)
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self._base_cache: dict[int, int] = {}
        self.player_spawn = (0, 0)

    @property
    def grass_y_bounds(self):
        ground_variation = 38
        return (int(self.height * 0.35), int(self.height * 0.35) + ground_variation)
    
    def get_world_seed(self):
        return self.seed

    def generate(self):
        # Build with Python lists for fast per-element noise writes
        tiles = [[TileID.AIR] * self.width for _ in range(self.height)]

        self._generate_base_terrain(tiles)
        self._spread_grass(tiles)

        # Convert to NumPy for vectorised operations in subsequent passes
        tiles = np.array(tiles, dtype=np.uint8)

        self._generate_caves(tiles)
        self._regrow_grass(tiles)
        self._generate_water(tiles)

        # bottom layer
        self._generate_bedrock_layer(tiles)

        return tiles
    
    def _generate_base_terrain(self, tiles):
        dirt_patch_scale_large = 20.0
        dirt_patch_scale_small = 10.0

        # chose player spawn x
        rng = random.Random(self.seed)
        player_spawn_x = self.width // 2 + rng.randint(-20, 20)

        for x in range(self.width):
            x_coord = x + 0.5  # avoid exact integer float inputs with noise
            """GRASS"""
            
            ground_noise = noise.pnoise1(
                x_coord / (self.scale * 1.2),
                octaves = self.octaves,
                persistence = self.persistence,
                lacunarity = self.lacunarity,
                base = self._layer_base(0)
            )
            normalized_ground_noise = max(0.0, min(1.0, (ground_noise + 1) / 2)) # normalizing output from (-1, 1) to (0, 1)

            ground_detail_noise = noise.pnoise1(
                x_coord / (self.scale * .4),
                octaves = 2,
                persistence = .5,
                lacunarity = 2.0,
                base = self._layer_base(0)
            )
            normalized_detail_noise  = max(0.0, min(1.0, (ground_detail_noise + 1) / 2))            

            """STONE"""
            stone_layer_noise = noise.pnoise1(
                x_coord / (self.scale * 2),
                octaves = 3,
                persistence = self.persistence * 0.8,
                lacunarity = self.lacunarity,                           
                base = self._layer_base(1)
            )
            normalized_stone_noise = max(0, min(1.0, ((stone_layer_noise / 0.7 + 0.55) / 2)))

            # combining ground_noise and detail_noise           
            combined_ground_noise = normalized_ground_noise * (0.7 + normalized_detail_noise * 0.35) # modify coefficient for more extreme terrain
            
            # self.height * x = base height, variation adds/subtracts from that
            # ground_variation = range +/- from base height, modified by noise
            ground_y_values = max(1, min(self.height - 2,
                int((self.height * 0.3) + (combined_ground_noise * GROUND_VARIATION))))
           
            stone_y_values = max(ground_y_values + 1, min(self.height - 1,
                int((self.height * 0.55) + (normalized_stone_noise * STONE_VARIATION))))  

            # top layer
            tiles[ground_y_values][x] = TileID.GRASS

            # point of transition between stone and dirt layers, modified by noise
            transition_center = stone_y_values

            # player spawn point
            if player_spawn_x == x:
                self.player_spawn = (x, ground_y_values - 1)

            for y in range(ground_y_values + 1, self.height):
                t = (y - (transition_center - TRANSITION_HALF_WIDTH)) / (TRANSITION_HALF_WIDTH * 2)
                t = max(0.0, min(1.0, t))
                
                if t <= 0.0:
                    base_tile = TileID.DIRT
                else:
                    large, small = self._gen_cave_noise(x, y, dirt_patch_scale_large, dirt_patch_scale_small, 4, 5)

                    if t >= 1.0:
                        base_tile = TileID.DIRT if (large > 0.38 or small > 0.25) else TileID.STONE
                    else:
                        normalized_noise = max(large, small) + 0.5
                        base_tile = TileID.STONE if normalized_noise < t else TileID.DIRT

                if base_tile == TileID.DIRT:
                    large, small = self._gen_cave_noise(x, y, 18.0, 12.0, 6, 7)
                    if large > 0.35 or small > 0.12:
                        base_tile = TileID.STONE

                if base_tile == TileID.STONE:
                    ore_tile = self._get_ore(x, y)
                    if ore_tile is not None:
                        tiles[y][x] = ore_tile
                    else:
                        tiles[y][x] = TileID.STONE
                else:
                    tiles[y][x] = base_tile

    def _spread_grass(self, tiles):
        copy_tiles = [row.copy() for row in tiles]

        for y in range(1, self.grass_y_bounds[1] + 1):
            for x in range(1, self.width - 1):
                if copy_tiles[y][x] == TileID.DIRT:
                    if (
                        copy_tiles[y - 1][x] == TileID.GRASS and
                        (copy_tiles[y][x - 1] == TileID.GRASS or copy_tiles[y][x + 1] == TileID.GRASS)
                    ):
                        tiles[y][x] = TileID.GRASS

    
    def _generate_caves(self, tiles):
        cave_scale_large = 27.0   # larger = bigger, more open caves
        cave_scale_small = 12.0   # smaller = tighter, winding tunnels

        for y, x in np.argwhere(tiles != TileID.AIR):
            large_cave, small_cave = self._gen_cave_noise(x, y, cave_scale_large, cave_scale_small, 2, 3)
            if large_cave > 0.32 or small_cave > 0.25:
                tiles[y, x] = TileID.AIR

        return tiles
    
    def _generate_water(self, tiles):
        rng = random.Random(self.seed)
        np_rng = np.random.default_rng(self.seed)

        water_level = int(self.height * 0.4)
        subregion = tiles[water_level:]
        air_mask = subregion == TileID.AIR
        labeled_air, num_caves = label(air_mask)

        caves_to_flood = {i: rng.uniform(0.1, 0.9) for i in range(1, num_caves + 1) if rng.random() < 0.26}

        for cave_id, fill_rate in caves_to_flood.items():
            cave_mask = labeled_air == cave_id
            random_mask = np_rng.random(cave_mask.shape) < fill_rate
            subregion[cave_mask & random_mask] = TileID.WATER

    def _layer_base(self, layer: int) -> int:
        if layer not in self._base_cache:
            h = hashlib.md5(f"{self.seed}:{layer}".encode()).digest()
            self._base_cache[layer] = (h[0] % 255) + 1  # always [1, 255]
        return self._base_cache[layer]

    def _gen_cave_noise(self, x, y, scale_large, scale_small, seed_large, seed_small):
        large = noise.pnoise2(
            (x + 0.5) / scale_large, 
            (y + 0.5) / scale_large,
            octaves=2, persistence=0.5, lacunarity=2.0,
            base=self._layer_base(seed_large)
        )
        small = noise.pnoise2(
            (x + 0.5) / scale_small, 
            (y + 0.5) / scale_small,
            octaves=2, persistence=0.5, lacunarity=2.0,
            base=self._layer_base(seed_small)
        )
        return large, small
    
    def _generate_bedrock_layer(self, tiles):
        tiles[-1, :] = TileID.BEDROCK

    def _regrow_grass(self, tiles):
        sky_clearance = 17
        grass_min_y, grass_max_y = self.grass_y_bounds
        region = tiles[grass_min_y:grass_max_y + 1]

        for dy, x in np.argwhere(region == TileID.DIRT):
            y = grass_min_y + dy
            top = max(0, y - sky_clearance)
            if np.all(tiles[top:y, x] == TileID.AIR):  # also vectorize the sky check
                tiles[y, x] = TileID.GRASS

    def _get_ore(self, x, y):
        depth_ratio = y / self.height

        for (tile, min_depth, scale_l, scale_s, thresh_l, thresh_s, seed_l, seed_s) in ORE_CONFIGS:
            if depth_ratio < min_depth:
                continue

            large, small = self._gen_cave_noise(x, y, scale_l, scale_s, seed_l, seed_s)

            if large > thresh_l or small > thresh_s:
                return tile

        return None
