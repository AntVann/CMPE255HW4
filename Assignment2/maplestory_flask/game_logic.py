from models import Character, Monster
import random


class Item:
    def __init__(self, name, attack_bonus=0, defense_bonus=0):
        self.name = name
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus


class GameManager:
    def __init__(self):
        self.characters = {}
        self.monsters = {
            "slime": Monster("Slime", 1, 10),
            "mushroom": Monster("Mushroom", 2, 20),
            "snail": Monster("Snail", 3, 30),
        }
        self.items = {
            "wooden_sword": Item("Wooden Sword", attack_bonus=2),
            "leather_armor": Item("Leather Armor", defense_bonus=2),
        }

    def create_character(self, name, job):
        character = Character(name, job)
        self.characters[name] = character
        return character

    def get_character(self, name):
        return self.characters.get(name)

    def get_monster(self, name):
        return self.monsters.get(name)

    def battle(self, character_name, monster_name):
        character = self.get_character(character_name)
        monster = self.get_monster(monster_name)

        if not character or not monster:
            return "Invalid character or monster name."

        character_attack = character.level + sum(
            item.attack_bonus for item in character.inventory
        )
        character_defense = character.level + sum(
            item.defense_bonus for item in character.inventory
        )
        monster_attack = monster.level
        monster_defense = monster.level

        rounds = 0
        while character.level > 0 and monster.level > 0:
            rounds += 1
            if random.random() < 0.5:  # Character attacks first
                damage = max(0, character_attack - monster_defense)
                monster.level -= damage
                if monster.level <= 0:
                    break
                damage = max(0, monster_attack - character_defense)
                character.level -= damage
            else:  # Monster attacks first
                damage = max(0, monster_attack - character_defense)
                character.level -= damage
                if character.level <= 0:
                    break
                damage = max(0, character_attack - monster_defense)
                monster.level -= damage

        if character.level > 0:
            character.gain_exp(monster.exp_reward)
            result = f"{character.name} defeated {monster.name} after {rounds} rounds and gained {monster.exp_reward} exp!"
            if random.random() < 0.1:  # 10% chance to get an item
                item = random.choice(list(self.items.values()))
                character.inventory.append(item)
                result += f" {character.name} found a {item.name}!"
        else:
            result = f"{monster.name} defeated {character.name} after {rounds} rounds. Game Over!"

        return result

    def get_character_info(self, name):
        character = self.get_character(name)
        if not character:
            return None
        return {
            "name": character.name,
            "job": character.job,
            "level": character.level,
            "exp": character.exp,
            "next_level_exp": character.exp_to_next_level(),
            "inventory": [item.name for item in character.inventory],
        }


game_manager = GameManager()


def create_character(name, job):
    return game_manager.create_character(name, job)


def create_monster(name, level, exp_reward):
    return Monster(name, level, exp_reward)


def battle(character_name, monster_name):
    return game_manager.battle(character_name, monster_name)


def get_character_info(character_name):
    return game_manager.get_character_info(character_name)
