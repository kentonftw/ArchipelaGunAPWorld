from . import GungeonTestBase


class TestChamberAccess(GungeonTestBase):
    options = {
        "chamber_access_locks": True,
        "power_logic": 0,
    }

    def test_each_access_opens_one_chamber(self) -> None:
        self.assertTrue(self.can_reach_region("Keep of the Lead Lord"))
        self.assertFalse(self.can_reach_region("Gungeon Proper"))
        self.collect(self.get_items_by_name("Progressive Chamber Access")[0])
        self.assertTrue(self.can_reach_region("Gungeon Proper"))
        self.assertFalse(self.can_reach_region("Black Powder Mine"))


class TestStartingChamberAccess(GungeonTestBase):
    options = {
        "chamber_access_locks": True,
        "starting_chamber_access": 2,
        "power_logic": 0,
    }

    def test_starts_two_chambers_deep(self) -> None:
        self.assertTrue(self.can_reach_region("Black Powder Mine"))
        self.assertFalse(self.can_reach_region("Hollow"))

    def test_pool_has_the_rest(self) -> None:
        self.assertEqual(len(self.get_items_by_name("Progressive Chamber Access")), 2)


class TestPowerLogic(GungeonTestBase):
    options = {
        "chamber_access_locks": True,
        "starting_chamber_access": 4,
        "power_logic": 1,
    }

    def test_hollow_needs_good_items(self) -> None:
        self.assertTrue(self.can_reach_region("Black Powder Mine"))
        self.assertFalse(self.can_reach_region("Hollow"))
        self.collect(self.get_items_by_name("Random A Tier Gun")[:2])
        self.assertTrue(self.can_reach_region("Hollow"))
        self.assertFalse(self.can_reach_region("Forge"))


class TestTokenHunt(GungeonTestBase):
    options = {
        "tokens_required": 10,
        "token_pool_percentage": 150,
    }

    def test_token_count(self) -> None:
        self.assertEqual(len(self.get_items_by_name("Archipelago Token")), 15)


class TestBossHunt(GungeonTestBase):
    options = {
        "boss_checks": False,
        "boss_hunt": 8,
    }

    def test_boss_hunt_turns_on_boss_checks(self) -> None:
        self.assertTrue(self.world.options.boss_checks.value)


class TestStartWithUpgrades(GungeonTestBase):
    options = {
        "persistent_upgrades": True,
        "start_with_upgrades": True,
    }

    def test_upgrades_not_in_pool(self) -> None:
        self.assertEqual(len(self.get_items_by_name("Progressive Max Health")), 0)
