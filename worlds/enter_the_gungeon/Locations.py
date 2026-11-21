from BaseClasses import Location, MultiWorld
from .Options import AchievementLocationChecks, APItemLocationChecks
from .Items import progression_item_table

class GungeonLocation(Location):
    game: str = "Enter The Gungeon"


class LocationGeneration:

    location_id = {
        "Room Clear Points": 8755200,
        "Chests Opened": 8755300,
        "Cash Spent": 8755400,
        "Past Clears": 8755600,
        "Floor 1 Clears": 8755700,
        "Floor 2 Clears": 8755720,
        "Floor 3 Clears": 8755740,
        "Floor 4 Clears": 8755760,
        "Floor 5 Clears": 8755780,
        "Bullet Hell Clears": 8755800,
        "Oubliette Clears": 8755820,
        "Abbey Clears": 8755840,
        "Resourceful Rat Lair Clears": 8755860,
        "R&D Department Clears": 8755880,
        "Gungeon AP Item": 8755000,
    }

    short_location_count = {
        "Room Clear Points": 5,
        "Chests Opened": 4,
        "Cash Spent": 3,
        "Past Clears": 1,
        "Floor 1 Clears": 4,
        "Floor 2 Clears": 4,
        "Floor 3 Clears": 3,
        "Floor 4 Clears": 3,
        "Floor 5 Clears": 2,
        "Bullet Hell Clears": 1,
        "Oubliette Clears": 2,
        "Abbey Clears": 1,
        "Resourceful Rat Lair Clears": 0,
        "R&D Department Clears": 0,
        "Gungeon AP Item": 16,
    }

    standard_location_count = {
        "Room Clear Points": 8,
        "Chests Opened": 6,
        "Cash Spent": 5,
        "Past Clears": 4,
        "Floor 1 Clears": 6,
        "Floor 2 Clears": 6,
        "Floor 3 Clears": 4,
        "Floor 4 Clears": 4,
        "Floor 5 Clears": 4,
        "Bullet Hell Clears": 2,
        "Oubliette Clears": 3,
        "Abbey Clears": 2,
        "Resourceful Rat Lair Clears": 1,
        "R&D Department Clears": 1,
        "Gungeon AP Item": 25,
    }

    marathon_location_count = {
        "Room Clear Points": 13,
        "Chests Opened": 8,
        "Cash Spent": 7,
        "Past Clears": 6,
        "Floor 1 Clears": 8,
        "Floor 2 Clears": 8,
        "Floor 3 Clears": 6,
        "Floor 4 Clears": 6,
        "Floor 5 Clears": 6,
        "Bullet Hell Clears": 3,
        "Oubliette Clears": 6,
        "Abbey Clears": 3,
        "Resourceful Rat Lair Clears": 2,
        "R&D Department Clears": 2,
        "Gungeon AP Item": 40,
    }

    @classmethod
    def get_achievement_location_count(cls, case_number=1):

        match case_number:
            case 0:
                return 33
            case 1:
                return 56
            case 2:
                return 84

        return 56

    @classmethod
    def get_ap_item_location_count(cls, case_number=1):

        match case_number:
            case 0:
                return 16
            case 1:
                return 25
            case 2:
                return 40

        return 40

    @classmethod
    def get_ap_item_sub_count(cls, case_number=1):
        match case_number:
            case 0:
                return 16
            case 1:
                return 25
            case 2:
                return 40

        return 25

    @classmethod
    def get_location_count_list(cls, case_number=1):
        match case_number:
            case 0:
                return LocationGeneration.short_location_count
            case 1:
                return LocationGeneration.standard_location_count
            case 2:
                return LocationGeneration.marathon_location_count

        return LocationGeneration.standard_location_count


# When the item pool is bigger than the requested checks, Regions.fill_add_locations adds extra
# "Gungeon AP Item N" locations numbered after the chosen AP item count. The largest pool (all
# Marathon + every progression option + Reverse Curse) is 129 items against 33 Short achievement checks,
# which needs names up to 96. 150 leaves headroom and stays below the next ID block (Room Clear Points, +200).
MAX_AP_ITEM_LOCATIONS = 150
assert LocationGeneration.location_id["Gungeon AP Item"] + MAX_AP_ITEM_LOCATIONS \
    <= min(loc_id for name, loc_id in LocationGeneration.location_id.items() if name != "Gungeon AP Item")


def fill_achievement_locations():
    name_list = LocationGeneration.location_id.keys()

    for name in name_list:
        count = LocationGeneration.marathon_location_count[name]
        if name == "Gungeon AP Item":
            count = MAX_AP_ITEM_LOCATIONS

        for i in range(0, count):
            location_table.update({f"{name} {i + 1}": LocationGeneration.location_id[name] + i})

    return


# Cumulative enemy kills across runs. The count follows the Achievement Locations setting.
ENEMY_KILLS = "Enemy Kills"
ENEMY_KILLS_START_ID = 8755900
enemy_kill_location_count = {0: 3, 1: 6, 2: 10}

# First kill of each boss, and the region it's fought in (names match Regions.py)
boss_location_start_id = 8756000
boss_locations = [
    ("Defeat Bullet King", "Keep of the Lead Lord"),
    ("Defeat Gatling Gull", "Keep of the Lead Lord"),
    ("Defeat Trigger Twins", "Keep of the Lead Lord"),
    ("Defeat Ammoconda", "Gungeon Proper"),
    ("Defeat Beholster", "Gungeon Proper"),
    ("Defeat Gorgun", "Gungeon Proper"),
    ("Defeat Cannonbalrog", "Black Powder Mine"),
    ("Defeat Treadnaught", "Black Powder Mine"),
    ("Defeat Mine Flayer", "Black Powder Mine"),
    ("Defeat Door Lord", "Black Powder Mine"),
    ("Defeat Wallmonger", "Hollow"),
    ("Defeat High Priest", "Hollow"),
    ("Defeat Kill Pillars", "Hollow"),
    ("Defeat High Dragun", "Forge"),
    ("Defeat Advanced Dragun", "Forge"),
    ("Defeat Blobulord", "Oubliette"),
    ("Defeat Old King", "Abbey of the True Gun"),
    ("Defeat Resourceful Rat", "Resourceful Rat's Lair"),
    ("Defeat Agunim", "R&G Dept."),
    ("Defeat the Lich", "Bullet Hell"),
]
boss_location_table = {name: boss_location_start_id + i for i, (name, _) in enumerate(boss_locations)}
boss_location_region = {name: region for name, region in boss_locations}

# Master Rounds: beat a chamber's boss without taking damage
master_round_start_id = 8756100
master_round_locations = [
    ("Master Round I", "Keep of the Lead Lord"),
    ("Master Round II", "Gungeon Proper"),
    ("Master Round III", "Black Powder Mine"),
    ("Master Round IV", "Hollow"),
    ("Master Round V", "Forge"),
]
master_round_table = {name: master_round_start_id + i for i, (name, _) in enumerate(master_round_locations)}
master_round_region = {name: region for name, region in master_round_locations}

# Shrines: first use of each kind. They can show up on any floor, so they live in the Keep.
shrine_start_id = 8756200
shrine_locations = [
    "Use an Ammo Shrine",
    "Use a Blank Shrine",
    "Use a Blood Shrine",
    "Use a Cleanse Shrine",
    "Use a Companion Shrine",
    "Use a Dice Shrine",
    "Use a Glass Shrine",
    "Use a Hero Shrine",
    "Use a Junk Shrine",
    "Use a Health Swap Shrine",
    "Complete a Challenge Shrine",
]
shrine_table = {name: shrine_start_id + i for i, name in enumerate(shrine_locations)}

# NPC rescues, detected from the game's own flags. Where each one's cell can appear varies, so they all
# expect Forge access to keep logic safe.
npc_rescue_start_id = 8756300
npc_rescue_locations = [
    "Rescue Flynt",
    "Rescue Old Red",
    "Rescue Cursula",
    "Rescue Professor Goopton",
    "Rescue Trorc",
    "Rescue the Gunsling King",
    "Rescue the Lost Adventurer",
    "Rescue Tonic",
    "Rescue Frifle and Mauser",
    "Rescue Daisuke",
    "Rescue Bowler",
    "Rescue the Sorceress",
    "Rescue the Synergrace",
]
npc_rescue_table = {name: npc_rescue_start_id + i for i, name in enumerate(npc_rescue_locations)}

location_table = {}

fill_achievement_locations()

for i in range(max(enemy_kill_location_count.values())):
    location_table[f"{ENEMY_KILLS} {i + 1}"] = ENEMY_KILLS_START_ID + i
location_table.update(boss_location_table)
location_table.update(master_round_table)
location_table.update(shrine_table)
location_table.update(npc_rescue_table)

event_location_table = {
    "The High Dragun": None,
    "The Lich": None,
    "Base Secret Chamber Bosses": None,
    "Past Killed": None,
    "Advanced Gungeon Bosses": None,
    "Farewell To Arms Bosses": None
}

location_table.update(event_location_table)
