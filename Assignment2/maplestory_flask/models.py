class Character:
    def __init__(self, name, job, level=1, exp=0):
        self.name = name
        self.job = job
        self.level = level
        self.exp = exp
        self.inventory = []

    def gain_exp(self, amount):
        self.exp += amount
        while self.exp >= self.exp_to_next_level():
            self.level_up()

    def exp_to_next_level(self):
        return self.level * 100  # Simplified exp curve

    def level_up(self):
        self.level += 1
        self.exp -= self.exp_to_next_level()
        print(f"{self.name} leveled up to {self.level}!")


class Monster:
    def __init__(self, name, level, exp_reward):
        self.name = name
        self.level = level
        self.exp_reward = exp_reward
