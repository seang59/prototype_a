from items.equipment.weapon.bow import Bow, Quiver
from items.game_object import WeaponType, ItemRarity
from items.equipment.weapon.weapon import Weapon
from items.placeable_block import PlaceableBlock
from world.generator import TileID

"""
    0–99	Blocks / Placeables
    100–199	Ores / Materials
    200–299	Tools
    300–499	Weapons
    500–599	Armor
    600–699	Accessories
    700–799	Consumables
    800–899	Ammo
"""

DEFINITIONS = {

    # 0–99 Blocks / Placeables

    "air_block": {
        "class": PlaceableBlock,
        "id": TileID.AIR,
        "name": "Air Block",
        "sprite": None,
        "color": None,
        "rarity": ItemRarity.COMMON,
        "stack_size": 200,
    },
    "grass_block": {
        "class": PlaceableBlock,
        "id": TileID.GRASS,
        "name": "Grass Block",
        "sprite": "sprites/blocks/DoneGrass.png",
        "sprite_variant": "grass_corner",
        "color": "chartreuse4",
        "rarity": ItemRarity.COMMON,
        "stack_size": 200,
    },
    "dirt_block": {
        "class": PlaceableBlock,
        "id": TileID.DIRT,
        "name": "Dirt Block",
        "sprite": "sprites/blocks/StarterDirt.png",
        "sprite_variant": "dirt_corner",
        "color": "burlywood4",
        "rarity": ItemRarity.COMMON,
        "stack_size": 200,
    },
    "stone_block": {
        "class": PlaceableBlock,
        "id": TileID.STONE,
        "name": "Stone Block",
        "sprite": "sprites/blocks/Sprite-0004.png",
        "color": None,
        "rarity": ItemRarity.COMMON,
        "stack_size": 200,
    },
    "water_block": {
        "class": PlaceableBlock,
        "id": TileID.WATER,
        "name": "Water Block",
        "sprite": None,
        "color": "blue",
        "rarity": ItemRarity.COMMON,
        "stack_size": 200,
    },
    "bedrock_block": {
        "class": PlaceableBlock,
        "id": TileID.BEDROCK,
        "name": "Bedrock Block",
        "sprite": None,
        "color": "white",
        "rarity": ItemRarity.COMMON,
        "stack_size": 200,
    },
    "copper_ore_block": {
        "class": PlaceableBlock,
        "id": TileID.COPPER_ORE,
        "name": "Copper Ore Block",
        "sprite": None,
        "color": "orange",
        "rarity": ItemRarity.COMMON,
        "stack_size": 200,
    },
    "iron_ore_block": {
        "class": PlaceableBlock,
        "id": TileID.IRON_ORE,
        "name": "Iron Ore Block",
        "sprite": None,
        "color": "gray",
        "rarity": ItemRarity.COMMON,
        "stack_size": 200,
    },
    "gold_ore_block": {
        "class": PlaceableBlock,
        "id": TileID.GOLD_ORE,
        "name": "Gold Ore Block",
        "sprite": None,
        "color": "yellow",
        "rarity": ItemRarity.COMMON,
        "stack_size": 200,
    },
    "diamond_ore_block": {
        "class": PlaceableBlock,
        "id": TileID.DIAMOND_ORE,
        "name": "Diamond Ore Block",
        "sprite": None,
        "color": "cyan",
        "rarity": ItemRarity.UNCOMMON,
        "stack_size": 200,
    },
    "shatterite_ore_block": {
        "class": PlaceableBlock,
        "id": TileID.SHATTERITE_ORE,
        "name": "Shatterite Ore Block",
        "sprite": None,
        "color": "magenta",
        "rarity": ItemRarity.RARE,
        "stack_size": 200,
    },

    # 100–199 Ores / Materials

    # 200–299 Tools

    # 300–499 Weapons: 300-349 melee, 350-399 ranged
    # id, name, sprite, color, stack_size, type: WeaponType, rarity: ItemRarity, damage, attack_speed

    "copper_sword": {
        "class": Weapon,
        "id": 300,
        "name": "Copper Sword",
        "sprite": None,
        "color": "orange",
        "stack_size": 1,
        "type": WeaponType.SWORD,
        "rarity": ItemRarity.COMMON,
        "damage": 5,
        "attack_speed": 1.0,
    },
    "iron_sword": {
        "class": Weapon,
        "id": 301,
        "name": "Iron Sword",
        "sprite": None,
        "color": "gray",
        "stack_size": 1,
        "type": WeaponType.SWORD,
        "rarity": ItemRarity.COMMON,
        "damage": 8,
        "attack_speed": 1.0,
    },
    "iron_claymore": {
        "class": Weapon,
        "id": 302,
        "name": "Iron Claymore",
        "sprite": None,
        "color": "gray",
        "stack_size": 1,
        "type": WeaponType.LONG_SWORD,
        "rarity": ItemRarity.COMMON,
        "damage": 14,
        "attack_speed": 0.8,
    },
    "gold_sword": {
        "class": Weapon,
        "id": 303,
        "name": "Gold Sword",
        "sprite": None,
        "color": "yellow",
        "stack_size": 1,
        "type": WeaponType.SWORD,
        "rarity": ItemRarity.COMMON,
        "damage": 12,
        "attack_speed": 1.1,
    },
    "shining_bastard_sword": {
        "class": Weapon,
        "id": 304,
        "name": "Shining Bastard Sword",
        "sprite": None,
        "color": "yellow",
        "stack_size": 1,
        "type": WeaponType.SWORD,
        "rarity": ItemRarity.UNCOMMON,
        "damage": 12,
        "attack_speed": 1.1,
    },
    "diamond_sword": {
        "class": Weapon,
        "id": 305,
        "name": "Diamond Sword",
        "sprite": None,
        "color": "cyan",
        "stack_size": 1,
        "type": WeaponType.SWORD,
        "rarity": ItemRarity.RARE,
        "damage": 16,
        "attack_speed": 1.2,
    },
    "sonic_sword": {
        "class": Weapon,
        "id": 306,
        "name": "Sonic Sword",
        "sprite": None,
        "color": "cyan",
        "stack_size": 1,
        "type": WeaponType.SWORD,
        "rarity": ItemRarity.EPIC,
        "damage": 11,
        "attack_speed": 1.6,
    },
    "hyper_sword": {
        "class": Weapon,
        "id": 307,
        "name": "Hyper Sword",
        "sprite": None,
        "color": "cyan",
        "stack_size": 1,
        "type": WeaponType.SWORD,
        "rarity": ItemRarity.EPIC,
        "damage": 10,
        "attack_speed": 2.0,
    },
    


    "the_first_bow": {
        "class": Bow,
        "id": 350,
        "name": "The First Bow",
        "sprite": None,
        "color": "brown",
        "stack_size": 1,
        "type": WeaponType.RANGED,
        "rarity": ItemRarity.COMMON,
        "damage": 0,
        "attack_speed": 1.0,
        "damage_mult": 1.0,
    },
        "basic_quiver": {
        "class": Quiver,
        "id": 351,
        "name": "Basic Quiver",
        "sprite": None,
        "color": "red",
        "stack_size": 1,
        "type": WeaponType.RANGED,
        "rarity": ItemRarity.COMMON,
        "damage": 5,
        "attack_speed": 1.0,
        "arrow_type": "arrow",
    },
        "lightning_quiver": {
        "class": Quiver,
        "id": 352,
        "name": "Lightning Quiver",
        "sprite": None,
        "color": "blue",
        "stack_size": 1,
        "type": WeaponType.RANGED,
        "rarity": ItemRarity.COMMON,
        "damage": 5,
        "attack_speed": 1.0,
        "arrow_type": "lightning_arrow",
    },
    # 500–599 Armor
    # 600–699 Accessories
    # 700–799 Consumables
    # 800–899 Ammo

}
