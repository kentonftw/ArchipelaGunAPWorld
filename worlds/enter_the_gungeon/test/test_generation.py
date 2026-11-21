"""Generation tests in Archipelago's own format. WorldTestBase also checks, for every class here, that the world
fills, that everything is reachable with all items and that something is reachable with none."""
from . import GungeonTestBase


class TestDefaults(GungeonTestBase):
    pass


class TestAllChecks(GungeonTestBase):
    options = {
        "boss_checks": True,
        "enemy_kill_checks": True,
        "master_round_checks": True,
        "shrine_checks": True,
        "npc_rescue_checks": True,
        "achievement_locations": 2,
        "ap_item_locations": 2,
    }

    def test_new_check_kinds_exist(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        for name in ("Master Round I", "Master Round V", "Use an Ammo Shrine", "Complete a Challenge Shrine",
                     "Rescue Flynt", "Defeat Bullet King", "Enemy Kills 1"):
            self.assertIn(name, names)


class TestNoLocks(GungeonTestBase):
    options = {
        "chamber_access_locks": False,
        "bullet_parts": False,
        "sell_creeps_favor": False,
        "power_logic": 0,
    }

    def test_forge_open_from_start(self) -> None:
        self.assertTrue(self.can_reach_region("Forge"))
