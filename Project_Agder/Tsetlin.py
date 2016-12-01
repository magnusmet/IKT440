import random


class Judge:
    def __init__(self):
        self.reward_prob = [0.0, 0.2, 0.4, 0.6, 0.4, 0.2]

    def reward(self, voters):
        number_of_yes_votes = voters.count(1)

        rewards = []
        for voter in voters:
            if random.random() <= self.reward_prob[number_of_yes_votes]:
                rewards.append(True)
            else:
                rewards.append(False)
        return rewards


class Tsetlin:
    def __init__(self, n):
        # n is the number of states per action
        self.n = n

        # Initial state selected randomly
        self.state = random.choice([self.n, self.n + 1])

    def reward_or_penalty(self, reward):
        if reward == True:
            if self.state <= self.n and self.state > 1:
                self.state -= 1
            elif self.state > self.n and self.state < 2 * self.n:
                self.state += 1
        else:
            if self.state <= self.n:
                self.state += 1
            elif self.state > self.n:
                self.state -= 1

    def makeDecision(self):
        if self.state <= self.n:
            return 0
        else:
            return 1