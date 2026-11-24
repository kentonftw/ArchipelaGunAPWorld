from typing import List
from .Items import unlock_item_table, bullet_part_table
from .Items import item_table, pickup_item_table, trap_item_table, GungeonItem, progression_item_table, fill_item_table
from .Items import gun_item_table, passive_item_table, paradox_character_unlock_table, get_progression_item_names, get_upgrade_item_names, persistent_upgrade_table
from .Items import (item_name_groups, token_item_table, power_item_names, get_all_upgrade_names, get_starting_chamber_access,
                    CHAMBER_ACCESS, ARCHIPELAGO_TOKEN)
from .Locations import boss_location_table, master_round_table, shrine_table, npc_rescue_table, master_round_region, \
    boss_location_region
from .Options import ShopAPItems
from . import Items
from .Locations import location_table, GungeonLocation, LocationGeneration
from .Options import GungeonOptions, gungeon_option_groups, gungeon_options_presets
from .Rules import set_rules
from .Regions import create_regions, get_gungeon_items_count, get_user_requested_locations_count
from BaseClasses import Item, ItemClassification, MultiWorld, Tutorial
from ..AutoWorld import World, WebWorld

client_version = 1

useful_names = {"Random A Tier Gun", "Random S Tier Gun", "Random A Tier Passive", "Random S Tier Passive", "Random Rare Active Item",
                "Reverse Curse Reversal"} | set(persistent_upgrade_table)
progression_names = set(progression_item_table) | set(unlock_item_table) | set(bullet_part_table) \
    | set(paradox_character_unlock_table) | set(token_item_table)


def build_location_name_groups():
    """By floor and by kind, for "!hint" and trackers."""
    from .Regions import location_region, location_kind, KEEP, FORGE
    from .Locations import location_table, event_location_table
    groups = {}
    for name in location_table:
        if name in event_location_table:
            continue
        kind = location_kind(name)
        floor = (boss_location_region.get(name) or master_round_region.get(name)
                 or (FORGE if name in npc_rescue_table else None) or location_region.get(kind, KEEP))
        groups.setdefault(floor, set()).add(name)
    groups["Bosses"] = set(boss_location_table)
    groups["Master Rounds"] = set(master_round_table)
    groups["Shrines"] = set(shrine_table)
    groups["NPC Rescues"] = set(npc_rescue_table)
    groups["AP Items"] = {n for n in location_table if n.startswith("Gungeon AP Item ")}
    groups["Enemy Kills"] = {n for n in location_table if n.startswith("Enemy Kills ")}
    return groups


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
    item_name_groups = item_name_groups
    location_name_groups = build_location_name_groups()

    options_dataclass = GungeonOptions
    options: GungeonOptions

    def generate_early(self):
        # Universal Tracker regenerates from slot data; take the options from there when it does
        passthrough = getattr(self.multiworld, "re_gen_passthrough", {}).get(self.game)
        if passthrough:
            for option_name, slot_key in self.slot_data_options.items():
                if slot_key in passthrough:
                    getattr(self.options, option_name).value = passthrough[slot_key]

        # Boss Hunt needs the boss checks to exist
        if self.options.boss_hunt.value > 0 and not self.options.boss_checks.value:
            self.options.boss_checks.value = 1

    # option attribute -> slot data key, for Universal Tracker
    slot_data_options = {
        "dragun": "Dragun", "lich": "Lich", "past_kills": "Pasts", "base_secret_chamber": "BaseSecret",
        "advanced_gungeon": "AdvancedGungeon", "farewell_arms": "FarewellArms", "paradox_mode": "Paradox",
        "reverse_curse": "ReverseCurse", "chamber_access_locks": "ChamberAccessLocks", "bullet_parts": "BulletParts",
        "sell_creeps_favor": "SellCreepsFavor", "allow_glitch_chest_skips": "AllowGlitchChestSkips",
        "allow_teleporter_skips": "AllowTeleporterSkips", "boss_checks": "BossChecks",
        "enemy_kill_checks": "EnemyKillChecks", "persistent_upgrades": "PersistentUpgrades",
        "start_with_upgrades": "StartWithUpgrades", "starting_chamber_access": "StartingChamberAccess",
        "power_logic": "PowerLogic", "master_round_checks": "MasterRoundChecks", "shrine_checks": "ShrineChecks",
        "npc_rescue_checks": "NPCRescueChecks", "boss_hunt": "BossHunt", "tokens_required": "TokensRequired",
        "token_pool_percentage": "TokenPoolPercentage", "achievement_locations": "AchievementChecks",
        "ap_item_locations": "APItemChecks", "guns": "Guns", "passives": "Passives", "traps": "Traps",
        "consumable": "Consumables",
    }

    @staticmethod
    def interpret_slot_data(slot_data):
        # Universal Tracker: hand slot data back so generate_early can rebuild the same world
        return slot_data

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
            "BossChecks": self.options.boss_checks.value,
            "EnemyKillChecks": self.options.enemy_kill_checks.value,
            "PersistentUpgrades": self.options.persistent_upgrades.value,
            "StartWithUpgrades": self.options.start_with_upgrades.value,
            "StartingChamberAccess": self.options.starting_chamber_access.value,
            "PowerLogic": self.options.power_logic.value,
            "MasterRoundChecks": self.options.master_round_checks.value,
            "ShrineChecks": self.options.shrine_checks.value,
            "NPCRescueChecks": self.options.npc_rescue_checks.value,
            "ShopAPItemRate": {ShopAPItems.option_off: 0, ShopAPItems.option_rare: 5, ShopAPItems.option_normal: 3,
                               ShopAPItems.option_frequent: 2}[self.options.shop_ap_items.value],
            "BossHunt": self.options.boss_hunt.value,
            "TokensRequired": self.options.tokens_required.value,
            "TokenPoolPercentage": self.options.token_pool_percentage.value,
            "Guns": self.options.guns.value,
            "Passives": self.options.passives.value,
            "Traps": self.options.traps.value,
            "Consumables": self.options.consumable.value,

            "AchievementChecks": self.options.achievement_locations.value,
            "APItemChecks": self.options.ap_item_locations.value,
            "ExtraLocations": self.count_extra_locations(),
            "APWorld": "0.5.0"
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
        if name in progression_names or (name in power_item_names and self.options.power_logic.value):
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

        "Persistent upgrades (applied every run) =========="
        for upgrade_name in get_upgrade_item_names(self.options):
            item_pool.append(self.create_useful_item(upgrade_name))
        if self.options.start_with_upgrades.value:
            for upgrade_name in get_all_upgrade_names(self.options):
                self.multiworld.push_precollected(self.create_useful_item(upgrade_name))

        "Starting Chamber Access =========="
        for i in range(get_starting_chamber_access(self.options)):
            self.multiworld.push_precollected(self.create_progress_item(CHAMBER_ACCESS))

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
        trap_names = list(trap_item_table)
        other_names = [name for name in fill_item_table if name not in trap_item_table]
        trap_percent = self.options.filler_trap_percentage.value
        for i in range(0, amount_to_fill):
            if self.random.randrange(100) < trap_percent:
                item_pool.append(self.create_item(self.random.choice(trap_names)))
            else:
                item_pool.append(self.create_item(self.random.choice(other_names)))

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
