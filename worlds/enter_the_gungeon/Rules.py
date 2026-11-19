import typing
from BaseClasses import CollectionState, MultiWorld
from .Options import (GungeonOptions, DragunGoal, LichGoal, KillThePastGoal, BaseSecretChamberBosses,
                      AdvancedGungeonDragunsBosses, FarewellToArmsBosses)


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
    # Note: this option's values are inverted compared to the others (required = 0, optional = 1).
    if options.farewell_arms.value == FarewellToArmsBosses.option_required:
        required.append("Farewell To Arms Bosses")

    return required


def set_rules(multiworld: MultiWorld, options: GungeonOptions, player,
              area_connections: typing.Dict[int, int], area_cost_map: typing.Dict[int, int]):
    # TODO (logic design): no location or goal-event access rules yet, so every check is in sphere 1.
    # Earlier commented-out intent: Old King needs "Old Crest", Resourceful Rat needs "Gnawed Key",
    # Advanced Dragun needs "Weird Egg", Lich needs some number of items.

    required_events = get_required_goal_events(options)
    multiworld.completion_condition[player] = \
        lambda state: state.has_all(required_events, player)
