from BaseClasses import Item

class ItemPoolGeneration:

    short_item_count = {
        "Random D or C Tier Gun": 4,
        "Random Active Item": 3,
        "Random B Tier Gun": 3,
        "Random A Tier Gun": 2,
        "Random S Tier Gun": 1,
        "Random D or C Tier Passive": 4,
        "Random Rare Active Item": 3,
        "Random B Tier Passive": 4,
        "Random A Tier Passive": 3,
        "Random S Tier Passive": 2,
        "Consumables": 10,
        "Traps": 10
    }

    standard_item_count = {
        "Random D or C Tier Gun": 5,
        "Random Active Item": 4,
        "Random B Tier Gun": 4,
        "Random A Tier Gun": 3,
        "Random S Tier Gun": 2,
        "Random D or C Tier Passive": 5,
        "Random Rare Active Item": 4,
        "Random B Tier Passive": 4,
        "Random A Tier Passive": 3,
        "Random S Tier Passive": 2,
        "Consumables": 20,
        "Traps": 15
    }

    marathon_item_count = {
        "Random D or C Tier Gun": 7,
        "Random Active Item": 5,
        "Random B Tier Gun": 5,
        "Random A Tier Gun": 3,
        "Random S Tier Gun": 3,
        "Random D or C Tier Passive": 7,
        "Random Rare Active Item": 7,
        "Random B Tier Passive": 5,
        "Random A Tier Passive": 3,
        "Random S Tier Passive": 3,
        "Consumables": 30,
        "Traps": 25
    }

    @classmethod
    def get_guns_count(cls, case_number=1):
        match case_number:
            case 0:
                return 13
            case 1:
                return 18
            case 2:
                return 23

        return 18

    @classmethod
    def get_passive_count(cls, case_number=1):
        match case_number:
            case 0:
                return 16
            case 1:
                return 18
            case 2:
                return 25

        return 18

    @classmethod
    def get_consumables_count(cls, case_number=1):

        match case_number:
            case 0:
                return ItemPoolGeneration.short_item_count["Consumables"]
            case 1:
                return ItemPoolGeneration.standard_item_count["Consumables"]
            case 2:
                return ItemPoolGeneration.marathon_item_count["Consumables"]

        return ItemPoolGeneration.standard_item_count["Consumables"]

    @classmethod
    def get_traps_count(cls, case_number=1):

        match case_number:
            case 0:
                return ItemPoolGeneration.short_item_count["Traps"]
            case 1:
                return ItemPoolGeneration.standard_item_count["Traps"]
            case 2:
                return ItemPoolGeneration.marathon_item_count["Traps"]

        return ItemPoolGeneration.standard_item_count["Traps"]

class GungeonItem(Item):
    game: str = "Enter The Gungeon"


item_table = {}

gun_item_table = {
    "Random D or C Tier Gun": 8754000,
    "Random Active Item": 8754001,
    "Random B Tier Gun": 8754002,
    "Random A Tier Gun": 8754003,
    "Random S Tier Gun": 8754004,
}

passive_item_table = {
    "Random D or C Tier Passive": 8754005,
    "Random Rare Active Item": 8754006,
    "Random B Tier Passive": 8754007,
    "Random A Tier Passive": 8754008,
    "Random S Tier Passive": 8754009,
}

pickup_item_table = {
    "Glassful of Guons": 8754100,
    "50 Casings": 8754101,
    "Key": 8754102,
    "Blank": 8754103,
    "Armor": 8754104,
    "Heart": 8754105,
    "Ammo": 8754106,
}

trap_item_table = {
    "Rats!! Trap": 8754200,
    "Mimic Gun Trap": 8754201,
    "Curse Trap": 8754202,
    "Fumble Gun Trap": 8754203,
    "Fire Trap": 8754204,
    "Poison Trap": 8754205,
    "Curse Meter Trap": 8754206,
    "Enemy Trap": 8754207,
}

progression_item_table = {
    "Gnawed Key": 8754301,
    "Old Crest": 8754302,
    "Weird Egg": 8754303,
}

paradox_character_unlock_table = {
    "Marine Paradox": 8754400,
    "Convict Paradox": 8754401,
    "Pilot Paradox": 8754402,
    "Hunter Paradox": 8754403,
    "Robot Paradox": 8754404,
    "Bullet Paradox": 8754405,
}

useful_item_table = {
    "Reverse Curse Reversal": 8754500
}

CHAMBER_ACCESS = "Progressive Chamber Access"
CHAMBER_ACCESS_COUNT = 4  # one per elevator: Chamber 2 to Chamber 5
SELL_CREEPS_FAVOR = "Sell Creep's Favor"

unlock_item_table = {
    CHAMBER_ACCESS: 8754320,
    SELL_CREEPS_FAVOR: 8754321,
}

# Applied by the mod at the start of every run, for each copy received
persistent_upgrade_counts = {
    "Progressive Max Health": 3,
    "Progressive Armor": 3,
    "Progressive Blank": 3,
    "Starting Casings": 4,
    "Starting Key": 3,
}

persistent_upgrade_table = {
    "Progressive Max Health": 8754600,
    "Progressive Armor": 8754601,
    "Progressive Blank": 8754602,
    "Starting Casings": 8754603,
    "Starting Key": 8754604,
}


def get_upgrade_item_names(options) -> list:
    """Persistent upgrade items this slot puts in the pool, with repeats."""
    names = []
    if options.persistent_upgrades.value:
        for name, count in persistent_upgrade_counts.items():
            names += [name] * count
    return names


bullet_part_table = {
    "Prime Primer": 8754310,
    "Arcane Gunpowder": 8754311,
    "Planar Lead": 8754312,
    "Obsidian Shell Casing": 8754313,
}

base_character_items = ["Marine Paradox", "Convict Paradox", "Pilot Paradox", "Hunter Paradox"]
all_character_items = list(paradox_character_unlock_table)


def get_progression_item_names(options) -> list:
    """Every progression item this slot puts in the pool, with repeats. Used for both creation and counting."""
    names = list(progression_item_table)

    if options.chamber_access_locks.value:
        names += [CHAMBER_ACCESS] * CHAMBER_ACCESS_COUNT
    if options.bullet_parts.value:
        names += list(bullet_part_table)
    if options.sell_creeps_favor.value:
        names.append(SELL_CREEPS_FAVOR)
    if options.paradox_mode.value == 1:
        names += all_character_items

    return names

item_table.update(gun_item_table)
item_table.update(passive_item_table)
item_table.update(pickup_item_table)
item_table.update(trap_item_table)
item_table.update(progression_item_table)
item_table.update(paradox_character_unlock_table)
item_table.update(useful_item_table)
item_table.update(unlock_item_table)
item_table.update(bullet_part_table)
item_table.update(persistent_upgrade_table)

fill_item_table = {}
fill_item_table.update(gun_item_table)
fill_item_table.update(passive_item_table)
fill_item_table.update(pickup_item_table)
fill_item_table.update(trap_item_table)
