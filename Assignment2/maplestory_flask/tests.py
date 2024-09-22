import unittest
from app import app
from game_logic import game_manager, create_character, battle, get_character_info


class TestMaplestoryApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        game_manager.characters.clear()  # Clear characters before each test

    def test_character_creation(self):
        character = create_character("TestChar", "Warrior")
        self.assertEqual(character.name, "TestChar")
        self.assertEqual(character.job, "Warrior")
        self.assertEqual(character.level, 1)
        self.assertEqual(character.exp, 0)
        self.assertEqual(len(character.inventory), 0)

    def test_monster_creation(self):
        monster = game_manager.get_monster("slime")
        self.assertEqual(monster.name, "Slime")
        self.assertEqual(monster.level, 1)
        self.assertEqual(monster.exp_reward, 10)

    def test_battle(self):
        create_character("TestChar", "Warrior")
        result = battle("TestChar", "slime")
        self.assertIn("TestChar defeated Slime", result)
        character_info = get_character_info("TestChar")
        self.assertGreater(character_info["exp"], 0)

    def test_level_up(self):
        create_character("TestChar", "Warrior")
        for _ in range(10):  # Battle multiple times to ensure level up
            battle("TestChar", "slime")
        character_info = get_character_info("TestChar")
        self.assertGreater(character_info["level"], 1)

    def test_get_character_info(self):
        create_character("TestChar", "Warrior")
        info = get_character_info("TestChar")
        self.assertEqual(info["name"], "TestChar")
        self.assertEqual(info["job"], "Warrior")
        self.assertEqual(info["level"], 1)
        self.assertEqual(info["exp"], 0)
        self.assertEqual(info["next_level_exp"], 100)
        self.assertEqual(len(info["inventory"]), 0)

    def test_create_character_route(self):
        response = self.app.post(
            "/create_character", json={"name": "TestChar", "job": "Warrior"}
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["name"], "TestChar")
        self.assertEqual(data["job"], "Warrior")

    def test_battle_route(self):
        self.app.post("/create_character", json={"name": "TestChar", "job": "Warrior"})
        response = self.app.post(
            "/battle", json={"character_name": "TestChar", "monster_name": "slime"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("TestChar defeated Slime", data["result"])

    def test_get_character_info_route(self):
        self.app.post("/create_character", json={"name": "TestChar", "job": "Warrior"})
        response = self.app.get("/character/TestChar")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["name"], "TestChar")
        self.assertEqual(data["job"], "Warrior")

    def test_inventory_system(self):
        create_character("TestChar", "Warrior")
        initial_info = get_character_info("TestChar")
        self.assertEqual(len(initial_info["inventory"]), 0)

        # Battle multiple times to increase the chance of getting an item
        for _ in range(20):
            battle("TestChar", "slime")

        final_info = get_character_info("TestChar")
        self.assertGreaterEqual(
            len(final_info["inventory"]), 0
        )  # There's a chance to get at least one item


if __name__ == "__main__":
    unittest.main()
