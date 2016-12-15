import random


class Judge:
    def __init__(self):
        self.reward_prob = 0.0
        self.max_profit = 100
        self.nr_of_iteration_since_change = 0

    def set_max_profit(self, max):
        if max*1.1 < max+15 :
            self.max_profit = max+15
        else :
            self.max_profit = max*1.1
        self.nr_of_iteration_since_change = 0

    def iterations_since_change(self):
        self.nr_of_iteration_since_change += 1
        return self.nr_of_iteration_since_change

    def reset_iterations_since_change(self):
        self.nr_of_iteration_since_change = 0

    def print_(self):
        print self.max_profit
        #print self.nr_of_iteration_since_change

    def reward_probability(self, profit):
        self.reward_prob = profit/self.max_profit #profit/maxprofit


    def reward(self):
        if random.random() <= self.reward_prob:
            return True
        else:
            return False

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