from typing import List
from .Items import unlock_item_table, bullet_part_table
from .Items import item_table, pickup_item_table, trap_item_table, GungeonItem, progression_item_table, fill_item_table
from .Items import gun_item_table, passive_item_table, paradox_character_unlock_table, get_progression_item_names
from .Locations import location_table, GungeonLocation, LocationGeneration
from .Options import GungeonOptions, gungeon_option_groups, gungeon_options_presets
from .Rules import set_rules
from .Regions import create_regions, get_gungeon_items_count, get_user_requested_locations_count
from BaseClasses import Item, ItemClassification, MultiWorld, Tutorial
from ..AutoWorld import World, WebWorld

client_version = 1

useful_names = {"Random A Tier Gun", "Random S Tier Gun", "Random A Tier Item", "Random S Tier Item",
                "Reverse Curse Reversal"}
progression_names = set(progression_item_table) | set(unlock_item_table) | set(bullet_part_table) \
    | set(paradox_character_unlock_table)


class GungeonWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Enter The Gungeon for Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["MaoBoulve"]
    )]

    option_groups = gungeon_option_groups
    options_presets = gungeon_options_presets


class GungeonWorld(World):
    # Lifted from Store Page
    """ Enter the Gungeon is a bullet hell roguelike to get the Gungeon's treasure: the gun that can kill the past.

    The randomizer replaces all chests with APItems location checks. Milestones also send location checks.
    Received items/traps play a matching effect and spawn by the player.
    """

    game: str = "Enter The Gungeon"
    topology_present = False
    web = GungeonWeb()

    item_name_to_id = item_table
    location_name_to_id = location_table

    options_dataclass = GungeonOptions
    options: GungeonOptions

    def create_regions(self):
        create_regions(self.multiworld, self.options, self.player)
        self.place_events()

    """Defines Session.DataStorage.GetSlotData() dict"""

    def fill_slot_data(self):
        return {
            "Dragun": self.options.dragun.value,
            "Lich": self.options.lich.value,

            "Pasts": self.options.past_kills.value,

            "BaseSecret": self.options.base_secret_chamber.value,
            "AdvancedGungeon": self.options.advanced_gungeon.value,
            "FarewellArms": self.options.farewell_arms.value,

            "Paradox": self.options.paradox_mode.value,
            "DeathLink": self.options.death_link.value,
            "RandomEnemies": self.options.random_enemies.value,
            "ReverseCurse": self.options.reverse_curse.value,
            "ChamberAccessLocks": self.options.chamber_access_locks.value,
            "BulletParts": self.options.bullet_parts.value,
            "SellCreepsFavor": self.options.sell_creeps_favor.value,
            "AllowGlitchChestSkips": self.options.allow_glitch_chest_skips.value,
            "AllowTeleporterSkips": self.options.allow_teleporter_skips.value,

            "AchievementChecks": self.options.achievement_locations.value,
            "APItemChecks": self.options.ap_item_locations.value,
            "ExtraLocations": self.count_extra_locations(),
            "APWorld": "0.3.0"
        }

    def count_extra_locations(self):

        item_count = get_gungeon_items_count(self.options)
        location_count = get_user_requested_locations_count(self.options)

        extra_locations = item_count - location_count

        if extra_locations > 0:
            return extra_locations

        else:
            return 0

    def set_rules(self):
        self.area_connections = {}
        self.area_cost_map = {}
        set_rules(self.multiworld, self.options, self.player, self.area_connections, self.area_cost_map)

    def create_item(self, name: str) -> Item:
        if name in progression_names:
            return self.create_progress_item(name)
        if name in useful_names:
            return self.create_useful_item(name)
        if name in trap_item_table:
            return self.create_trap_item(name)
        return GungeonItem(name, ItemClassification.filler, item_table[name], self.player)

    def get_filler_item_name(self) -> str:
        return self.random.choice(list(pickup_item_table))

    def create_progress_item(self, name: str) -> Item:
        return GungeonItem(name, ItemClassification.progression, item_table[name], self.player)

    def create_useful_item(self, name: str) -> Item:
        return GungeonItem(name, ItemClassification.useful, item_table[name], self.player)

    def create_trap_item(self, name: str) -> Item:
        return GungeonItem(name, ItemClassification.trap, item_table[name], self.player)

    def create_event(self, name: str) -> GungeonItem:
        return GungeonItem(name, ItemClassification.progression, None, self.player)

    def create_items(self):
        item_pool: List[GungeonItem] = []

        item_pool = self.create_item_pool(item_pool, amount_case=self.options.guns.value,
                                          item_table_list=gun_item_table)
        item_pool = self.create_item_pool(item_pool, amount_case=self.options.passives.value,
                                          item_table_list=passive_item_table)

        "Progress items (key items, chamber access, bullet parts, Sell Creep's Favor, Paradox characters) ====="
        for progression_item_name in get_progression_item_names(self.options):
            item_pool.append(self.create_progress_item(progression_item_name))

        consumables_count = Items.ItemPoolGeneration.get_consumables_count(self.options.consumable.value)
        "Consumables items =============================="
        consumable_names = list(pickup_item_table)
        self.random.shuffle(consumable_names)
        for i in range(0, consumables_count):
            item_pool.append(self.create_item(consumable_names[i % len(consumable_names)]))

        trap_count = Items.ItemPoolGeneration.get_traps_count(self.options.traps.value)
        "Traps =============================="
        trap_names = list(trap_item_table)
        self.random.shuffle(trap_names)
        for i in range(0, trap_count):
            item_pool.append(self.create_trap_item(trap_names[i % len(trap_names)]))

        "Reverse Curse =============================="
        if self.options.reverse_curse.value != 0:
            for i in range(0, 8):
                item_pool.append(self.create_useful_item("Reverse Curse Reversal"))

        "Check for fill =============================="

        item_count = get_gungeon_items_count(self.options)
        location_count = get_user_requested_locations_count(self.options)

        if location_count > item_count:
            items_to_fill = location_count - item_count
            item_pool = self.create_fill_items(item_pool, items_to_fill)

        self.multiworld.itempool += item_pool

    def create_fill_items(self, item_pool, amount_to_fill=10):
        fill_names = list(fill_item_table)
        for i in range(0, amount_to_fill):
            item_pool.append(self.create_item(self.random.choice(fill_names)))

        return item_pool

    def create_item_pool(self, item_pool, amount_case=0, item_table_list=gun_item_table):
        item_name_list = item_table_list.keys()

        for name in item_name_list:
            quantity = 0

            match amount_case:
                case 0:
                    "Short amount"
                    quantity = Items.ItemPoolGeneration.short_item_count[name]
                case 1:
                    "Standard"
                    quantity = Items.ItemPoolGeneration.standard_item_count[name]
                case 2:
                    "Marathon"
                    quantity = Items.ItemPoolGeneration.marathon_item_count[name]
            item_pool += [self.create_item(name) for i in range(0, quantity)]
        return item_pool

    def place_events(self):
        self.multiworld.get_location("The High Dragun", self.player).place_locked_item(
            self.create_event("Defeat The High Dragun"))

        self.multiworld.get_location("The Lich", self.player).place_locked_item(
            self.create_event("Defeat The Lich"))

        self.multiworld.get_location("Base Secret Chamber Bosses", self.player).place_locked_item(
            self.create_event("Base Secret Chamber Bosses"))

        self.multiworld.get_location("Past Killed", self.player).place_locked_item(
            self.create_event("Past Killed"))

        self.multiworld.get_location("Advanced Gungeon Bosses", self.player).place_locked_item(
            self.create_event("Advanced Gungeon Bosses"))

        self.multiworld.get_location("Farewell To Arms Bosses", self.player).place_locked_item(
            self.create_event("Farewell To Arms Bosses"))
        return
