import typing
from BaseClasses import CollectionState, MultiWorld
from .Options import (GungeonOptions, DragunGoal, LichGoal, KillThePastGoal, BaseSecretChamberBosses,
                      AdvancedGungeonDragunsBosses, FarewellToArmsBosses)
from .Items import (CHAMBER_ACCESS, SELL_CREEPS_FAVOR, bullet_part_table, base_character_items,
                    all_character_items)
from .Regions import (KEEP, PROPER, MINE, HOLLOW, FORGE, ABBEY, RAT_LAIR, RG_DEPT, PASTS, BULLET_HELL,
                      entrance_name, location_kind)

Rule = typing.Callable[[CollectionState], bool]

# Milestone checks that count up across every floor. With chamber locks on, the later checks of each kind
# expect deeper chamber access, so they spread through the multiworld instead of all landing in sphere 1.
# Every one of them is still physically possible earlier (by replaying the Keep), so this never soft-locks.
SCALED_KINDS = ["Room Clear Points", "Chests Opened", "Cash Spent", "Gungeon AP Item", "Enemy Kills"]
CHAMBER_COUNT = 5


def get_required_goal_events(options: GungeonOptions) -> typing.List[str]:
    """Event items (placed in __init__.place_events) that the chosen goal options require."""
    required = []

    if options.dragun.value == DragunGoal.option_required:
        required.append("Defeat The High Dragun")
    if options.lich.value == LichGoal.option_required:
        required.append("Defeat The Lich")
    if options.past_kills.value != KillThePastGoal.option_optional:
        required.append("Past Killed")
    if options.base_secret_chamber.value == BaseSecretChamberBosses.option_required:
        required.append("Base Secret Chamber Bosses")
    if options.advanced_gungeon.value == AdvancedGungeonDragunsBosses.option_required:
        required.append("Advanced Gungeon Bosses")
    if options.farewell_arms.value == FarewellToArmsBosses.option_required:
        required.append("Farewell To Arms Bosses")

    return required


def set_rules(multiworld: MultiWorld, options: GungeonOptions, player,
              area_connections: typing.Dict[int, int], area_cost_map: typing.Dict[int, int]):
    locks = bool(options.chamber_access_locks.value)
    parts = bool(options.bullet_parts.value)
    favor = bool(options.sell_creeps_favor.value)
    paradox = options.paradox_mode.value == 1

    def chamber(n: int) -> Rule:
        """Can reach chamber n (1 = Keep). Needs n - 1 Progressive Chamber Access when locks are on."""
        if not locks or n <= 1:
            return lambda state: True
        return lambda state: state.has(CHAMBER_ACCESS, player, n - 1)

    def has_bullet(state: CollectionState) -> bool:
        return not parts or state.has_all(bullet_part_table, player)

    def characters(count: int, pool: typing.List[str] = all_character_items) -> Rule:
        """Has `count` of the characters in `pool`. Without Paradox Mode every character is playable."""
        if not paradox:
            return lambda state: True
        return lambda state: state.has_from_list(pool, player, count)

    def can_reach_rat_lair(state: CollectionState) -> bool:
        return chamber(3)(state) and state.has("Gnawed Key", player)

    def entrance(source: str, target: str, rule: Rule):
        multiworld.get_entrance(entrance_name(source, target), player).access_rule = rule

    def location(name: str, rule: Rule):
        multiworld.get_location(name, player).access_rule = rule

    # Main chambers: each elevator needs one more Progressive Chamber Access.
    entrance(KEEP, PROPER, chamber(2))
    entrance(PROPER, MINE, chamber(3))
    entrance(MINE, HOLLOW, chamber(4))
    entrance(HOLLOW, FORGE, chamber(5))

    # Secret floors. The Oubliette keeps its vanilla in-run requirements (water + 2 keys), so no item gate.
    entrance(PROPER, ABBEY, lambda state: state.has("Old Crest", player))
    entrance(MINE, RAT_LAIR, lambda state: state.has("Gnawed Key", player))
    # The R&G Dept. drops you straight into the Forge (no elevator), so the mod also requires Forge access.
    entrance(HOLLOW, RG_DEPT,
             lambda state: chamber(5)(state) and (not favor or state.has(SELL_CREEPS_FAVOR, player)))

    # Pasts need the Bullet That Can Kill The Past and at least one character who has a past.
    entrance(FORGE, PASTS, lambda state: has_bullet(state) and characters(1)(state))
    # Bullet Hell opens once the four base Gungeoneers' pasts are killed.
    entrance(PASTS, BULLET_HELL, characters(4, base_character_items))

    # "Past Clears N" needs N different characters.
    for loc in multiworld.get_locations(player):
        if location_kind(loc.name) == "Past Clears":
            count = int(loc.name.rsplit(" ", 1)[1])
            loc.access_rule = characters(count)

    # Spread the cumulative milestone checks across chambers 1 to 5.
    if locks:
        by_kind: typing.Dict[str, list] = {kind: [] for kind in SCALED_KINDS}
        for loc in multiworld.get_locations(player):
            kind = location_kind(loc.name)
            if kind in by_kind:
                by_kind[kind].append(loc)
        for locs in by_kind.values():
            locs.sort(key=lambda l: int(l.name.rsplit(" ", 1)[1]))
            for index, loc in enumerate(locs):
                loc.access_rule = chamber(1 + index * CHAMBER_COUNT // len(locs))

    # Goal events beyond their region's entrance.
    past_pool = base_character_items if options.past_kills.value == KillThePastGoal.option_standard \
        else all_character_items
    location("Past Killed", characters(len(past_pool), past_pool))
    location("Base Secret Chamber Bosses", lambda state: True)  # Oubliette is open from the Keep
    location("Advanced Gungeon Bosses", can_reach_rat_lair)  # Rat's Lair also covers the Advanced Dragun

    # Boss checks live in their floor's region; the Advanced Dragun also needs the Rat's Lair (or Weird Egg)
    if options.boss_checks.value:
        location("Defeat Advanced Dragun",
                 lambda state: can_reach_rat_lair(state) or state.has("Weird Egg", player))

    required_events = get_required_goal_events(options)
    multiworld.completion_condition[player] = \
        lambda state: state.has_all(required_events, player)
