import typing
from dataclasses import dataclass
from typing import Dict, Any
from Options import Option, Choice, DeathLink, DefaultOnToggle, Range, Toggle, PerGameCommonOptions, OptionGroup, OptionSet

# https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/options%20api.md

class DragunGoal(Choice):
    """Require High Dragun defeat for completion"""
    display_name = "Dragun Goal"
    option_required = 1
    option_optional = 0
    default = 1

class KillThePastGoal(Choice):
    """Require Past Kills for game completion. 'Standard' is base 4 characters. 'All' adds Robot & Bullet
    Mod provides way to use all game characters"""
    display_name = "Kill The Past Goal"
    option_optional = 0
    option_standard = 1
    option_all_pasts = 2
    default = 1

class LichGoal(Choice):
    """Require Lich Goal defeat for completion"""
    display_name = "Lich Goal"
    option_required = 1
    option_optional = 0
    default = 1

class BaseSecretChamberBosses(Choice):
    """Require Blobulord & Old King for completion"""
    display_name = "Base Secret Chamber Boss Goal"
    option_required = 1
    option_optional = 0
    default = 1

class AdvancedGungeonDragunsBosses(Choice):
    """Require bosses from the AG&D Update (Resourceful Rat, Advanced Dragun) for completion.
    Do not need to beat Rat at Punch Out"""
    display_name = "Advanced Gungeon & Draguns Bosses"
    option_required = 1
    option_optional = 0
    default = 0

class FarewellToArmsBosses(Choice):
    """Require bosses from the Farewell To Arms Update (Cam Clarke AS Agunim) for completion
    [Paradox Lich currently WIP]"""
    display_name = "Farewell To Arms Bosses"
    option_required = 1
    option_optional = 0
    default = 0

class RandomizeEnemies(Choice):
    """Randomize all basic enemies in the Gungeon."""
    display_name = "Randomize Enemies"
    option_random_enemies = 1
    option_standard_enemies = 0
    default = 1

class ParadoxMode(Choice):
    """Start all runs as Paradox. Other playable characters are Items in randomizer"""
    display_name = "Paradox Mode"
    option_enabled = 1
    option_disabled = 0
    default = 1

class ReverseCurseMode(Choice):
    """Gain curse at the beginning of every run & add randomizer items to reduce curse.
    Standard adds curse after 1 Past is cleared. Hard adds curse immediately"""
    display_name = "Reverse Curse Mode"
    option_disabled = 0
    option_standard = 1
    option_hard = 2
    default = 1

class ChamberAccessLocks(DefaultOnToggle):
    """Lock each elevator down to the next chamber until you receive a Progressive Chamber Access item.
    Adds 4 Progressive Chamber Access items to the pool."""
    display_name = "Chamber Access Locks"

class BulletPartsAsItems(DefaultOnToggle):
    """The four parts of the Bullet That Can Kill The Past (Prime Primer, Arcane Gunpowder, Planar Lead,
    Obsidian Shell Casing) become randomizer items. The Blacksmith only builds the Bullet once all four are received."""
    display_name = "Bullet Parts As Items"

class SellCreepsFavorItem(DefaultOnToggle):
    """The Sell Creep only opens the grate to the R&G Dept. once you receive Sell Creep's Favor."""
    display_name = "Sell Creep's Favor"

class AllowGlitchChestSkips(Toggle):
    """Let Glitch Chests send you to the next floor even when its chamber is locked.
    Off: a Glitch Chest opens like a normal chest while the next chamber is locked. Skips are never expected by logic."""
    display_name = "Allow Glitch Chest Skips"

class AllowTeleporterSkips(Toggle):
    """Let the Teleporter Prototype warp you to a locked next floor, or to the Abbey without the Old Crest.
    Off: those warps are removed from its random outcomes until you have access. Skips are never expected by logic."""
    display_name = "Allow Teleporter Prototype Skips"

class BossChecks(DefaultOnToggle):
    """Adds a check for the first kill of each boss: Bullet King, Gatling Gull, Trigger Twins, Ammoconda,
    Beholster, Gorgun, Cannonbalrog, Treadnaught, Mine Flayer, Door Lord, Wallmonger, High Priest,
    Kill Pillars, High Dragun, Advanced Dragun, Blobulord, Old King, Resourceful Rat, Agunim and the Lich."""
    display_name = "Boss Checks"

class EnemyKillChecks(DefaultOnToggle):
    """Adds checks for total enemies killed across all runs. Short: 3, Standard: 6, Marathon: 10 checks,
    following the Achievement Locations setting."""
    display_name = "Enemy Kill Checks"

class PersistentUpgrades(DefaultOnToggle):
    """Adds permanent upgrades that apply at the start of every run: Progressive Max Health (x3),
    Progressive Armor (x3), Progressive Blank (x3), Starting Casings (x4, 25 each) and Starting Key (x3)."""
    display_name = "Persistent Upgrades"

class GunItems(Choice):
    """Amount of Guns in your item pool"""
    display_name = "Gun Pool Items"
    option_short = 0
    option_standard = 1
    option_marathon = 2
    default = 1

class PassiveItems(Choice):
    """Amount of Passive & Active items in your item pool"""
    display_name = "Passive & Active Pool Items"
    option_short = 0
    option_standard = 1
    option_marathon = 2
    default = 1

class ConsumableItems(Choice):
    """Amount of Consumable items in your item pool"""
    display_name = "Consumable Items"
    option_short = 0
    option_standard = 1
    option_marathon = 2
    default = 0

class TrapItems(Choice):
    """Amount of Traps in your item pool"""
    option_short = 0
    option_standard = 1
    option_marathon = 2
    default = 1

class AchievementLocationChecks(Choice):
    """Location checks for accomplishing tasks in Enter the Gungeon"""
    option_short = 0
    option_standard = 1
    option_marathon = 2
    default = 1

class APItemLocationChecks(Choice):
    """Location checks from APItem replacing item in chests, shops, etc."""
    option_short = 0
    option_standard = 1
    option_marathon = 2
    default = 1


gungeon_option_groups = [
    OptionGroup("Boss Goals Options", [
        DragunGoal,
        KillThePastGoal,
        LichGoal,
        BaseSecretChamberBosses,
        AdvancedGungeonDragunsBosses,
        FarewellToArmsBosses
    ]),
    OptionGroup("Randomizer Options", [
       DeathLink,
       ParadoxMode,
       RandomizeEnemies,
       ReverseCurseMode
    ]),
    OptionGroup("Progression Options", [
       ChamberAccessLocks,
       BulletPartsAsItems,
       SellCreepsFavorItem,
       AllowGlitchChestSkips,
       AllowTeleporterSkips
    ]),
    OptionGroup("Extra Checks and Items", [
       BossChecks,
       EnemyKillChecks,
       PersistentUpgrades
    ]),
    OptionGroup("Gungeon Item Pool Options", [
       GunItems,
       PassiveItems,
       ConsumableItems,
       TrapItems
    ]),

    OptionGroup("Location Check Options", [
       APItemLocationChecks,
       AchievementLocationChecks
    ]),

]

gungeon_options_presets: Dict[str, Dict[str, Any]] = {
    "Quick Run": {
        "dragun": DragunGoal.option_required,
        "past_kills": KillThePastGoal.option_optional,
        "lich": LichGoal.option_optional,
        "base_secret_chamber": BaseSecretChamberBosses.option_optional,
        "advanced_gungeon": AdvancedGungeonDragunsBosses.option_optional,
        "farewell_arms": FarewellToArmsBosses.option_optional,
        "guns": GunItems.option_short,
        "passives": PassiveItems.option_short,
        "traps": TrapItems.option_short,
        "consumable": ConsumableItems.option_short,
        "achievement_locations": AchievementLocationChecks.option_short,
        "ap_item_locations": APItemLocationChecks.option_short,
    },
    "Marathon": {
        "dragun": DragunGoal.option_required,
        "past_kills": KillThePastGoal.option_all_pasts,
        "lich": LichGoal.option_required,
        "base_secret_chamber": BaseSecretChamberBosses.option_required,
        "advanced_gungeon": AdvancedGungeonDragunsBosses.option_required,
        "farewell_arms": FarewellToArmsBosses.option_required,
        "guns": GunItems.option_marathon,
        "passives": PassiveItems.option_marathon,
        "traps": TrapItems.option_marathon,
        "consumable": ConsumableItems.option_marathon,
        "achievement_locations": AchievementLocationChecks.option_marathon,
        "ap_item_locations": APItemLocationChecks.option_marathon,
    },
}

@dataclass
class GungeonOptions(PerGameCommonOptions):
    dragun: DragunGoal
    past_kills: KillThePastGoal
    lich: LichGoal
    base_secret_chamber: BaseSecretChamberBosses
    advanced_gungeon: AdvancedGungeonDragunsBosses
    farewell_arms: FarewellToArmsBosses

    paradox_mode: ParadoxMode
    random_enemies: RandomizeEnemies
    death_link: DeathLink
    reverse_curse: ReverseCurseMode

    chamber_access_locks: ChamberAccessLocks
    bullet_parts: BulletPartsAsItems
    sell_creeps_favor: SellCreepsFavorItem
    allow_glitch_chest_skips: AllowGlitchChestSkips
    allow_teleporter_skips: AllowTeleporterSkips
    boss_checks: BossChecks
    enemy_kill_checks: EnemyKillChecks
    persistent_upgrades: PersistentUpgrades

    guns: GunItems
    passives: PassiveItems
    traps: TrapItems
    consumable: ConsumableItems

    achievement_locations: AchievementLocationChecks
    ap_item_locations: APItemLocationChecks



