import typing
from BaseClasses import MultiWorld, Region, Entrance, Location
from .Locations import master_round_table, master_round_region, shrine_table, npc_rescue_table
from .Locations import ENEMY_KILLS, enemy_kill_location_count, boss_location_table, boss_location_region,\
     GungeonLocation, location_table, event_location_table, LocationGeneration
from .Items import ItemPoolGeneration, get_progression_item_names, get_upgrade_item_names
from .Options import GungeonOptions

def get_gungeon_items_count(options: GungeonOptions):
    item_count = 0

    item_count += ItemPoolGeneration.get_guns_count(options.guns.value)
    item_count += ItemPoolGeneration.get_passive_count(options.passives.value)
    item_count += ItemPoolGeneration.get_consumables_count(options.consumable.value)
    item_count += ItemPoolGeneration.get_traps_count(options.traps.value)

    item_count += len(get_progression_item_names(options))
    item_count += len(get_upgrade_item_names(options))

    if options.reverse_curse.value != 0:
        item_count += 8

    return item_count

def get_user_requested_locations_count(options: GungeonOptions):
    loc_count = 0
    loc_count += LocationGeneration.get_achievement_location_count(options.achievement_locations.value)
    loc_count += LocationGeneration.get_ap_item_location_count(options.ap_item_locations.value)
    loc_count += len(get_extra_check_names(options))

    return loc_count


def fill_add_locations(amount: 10, item_case: 1):

    chest_fill = amount

    last_chest = LocationGeneration.get_ap_item_sub_count(case_number=item_case)
    loc_name_list = []

    for i in range(0, chest_fill):
        loc_name = f"Gungeon AP Item {i + 1 + last_chest}"
        loc_name_list.append(loc_name)

    return loc_name_list


# Region graph. Each tuple is (from, to); entrance rules are set in Rules.set_rules.
MENU = "Menu"
KEEP = "Keep of the Lead Lord"
PROPER = "Gungeon Proper"
MINE = "Black Powder Mine"
HOLLOW = "Hollow"
FORGE = "Forge"
OUBLIETTE = "Oubliette"
ABBEY = "Abbey of the True Gun"
RAT_LAIR = "Resourceful Rat's Lair"
RG_DEPT = "R&G Dept."
PASTS = "Character Pasts"
BULLET_HELL = "Bullet Hell"

region_names = [MENU, KEEP, PROPER, MINE, HOLLOW, FORGE, OUBLIETTE, ABBEY, RAT_LAIR, RG_DEPT, PASTS, BULLET_HELL]

connections = [
    (MENU, KEEP),
    (KEEP, PROPER), (PROPER, MINE), (MINE, HOLLOW), (HOLLOW, FORGE),
    (KEEP, OUBLIETTE), (PROPER, ABBEY), (MINE, RAT_LAIR), (HOLLOW, RG_DEPT),
    (FORGE, PASTS), (PASTS, BULLET_HELL),
]


def entrance_name(source: str, target: str) -> str:
    return f"{source} -> {target}"


# Which region each kind of milestone check lives in. Checks not listed here (room clears, chests,
# cash spent, AP items) count up across all floors, so they live in the Keep and get scaled rules.
location_region = {
    "Floor 1 Clears": KEEP,
    "Floor 2 Clears": PROPER,
    "Floor 3 Clears": MINE,
    "Floor 4 Clears": HOLLOW,
    "Floor 5 Clears": FORGE,
    "Oubliette Clears": OUBLIETTE,
    "Abbey Clears": ABBEY,
    "Resourceful Rat Lair Clears": RAT_LAIR,
    "R&D Department Clears": RG_DEPT,
    "Past Clears": PASTS,
    "Bullet Hell Clears": BULLET_HELL,
}

event_region = {
    "The High Dragun": FORGE,
    "The Lich": BULLET_HELL,
    "Base Secret Chamber Bosses": ABBEY,
    "Past Killed": PASTS,
    "Advanced Gungeon Bosses": FORGE,
    "Farewell To Arms Bosses": RG_DEPT,
}


def get_extra_check_names(options: GungeonOptions) -> typing.List[str]:
    """Boss and enemy-kill checks, when their options are on."""
    names = []
    if options.enemy_kill_checks.value:
        count = enemy_kill_location_count[options.achievement_locations.value]
        names += [f"{ENEMY_KILLS} {i + 1}" for i in range(count)]
    if options.boss_checks.value:
        names += list(boss_location_table)
    if options.master_round_checks.value:
        names += list(master_round_table)
    if options.shrine_checks.value:
        names += list(shrine_table)
    if options.npc_rescue_checks.value:
        names += list(npc_rescue_table)
    return names


def get_location_names(options: GungeonOptions) -> typing.List[str]:
    """All non-event location names this slot creates, including extra AP item locations."""
    names = []

    achievement_count_list = LocationGeneration.get_location_count_list(options.achievement_locations.value)
    ap_item_count_list = LocationGeneration.get_location_count_list(options.ap_item_locations.value)

    for name in LocationGeneration.location_id:
        count_list = ap_item_count_list if name == "Gungeon AP Item" else achievement_count_list
        names += [f"{name} {i + 1}" for i in range(count_list[name])]

    names += get_extra_check_names(options)

    item_count = get_gungeon_items_count(options)
    location_count = get_user_requested_locations_count(options)
    if item_count > location_count:
        names += fill_add_locations(item_count - location_count, options.ap_item_locations.value)

    return names


def location_kind(location_name: str) -> str:
    """'Floor 2 Clears 3' -> 'Floor 2 Clears'"""
    return location_name.rsplit(" ", 1)[0]


def create_regions(world: MultiWorld, options: GungeonOptions, player: int):
    regions = {name: Region(name, player, world) for name in region_names}

    for location_name in get_location_names(options):
        region_name = (boss_location_region.get(location_name) or master_round_region.get(location_name)
                       or (FORGE if location_name in npc_rescue_table else None)
                       or location_region.get(location_kind(location_name), KEEP))
        region = regions[region_name]
        region.locations.append(GungeonLocation(player, location_name, location_table[location_name], region))

    for event_name, region_name in event_region.items():
        region = regions[region_name]
        region.locations.append(GungeonLocation(player, event_name, None, region))

    for source, target in connections:
        regions[source].connect(regions[target], entrance_name(source, target))

    world.regions += regions.values()
