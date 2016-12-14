import random



class Production:
    def __init__(self):
        self.price = [15,15,8,14,9,10,7,14,13,9,12,11,10,10,8,5,5,14,9,5,8,9,10,7]
        #self.price = [7,7,7,7,7,7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8,8,8,8]
        #self.max_profit = 15*24 #maxprice*24h
        self.efficiency = []

    def production(self, t, water_level):
        if water_level == 0:
            return 0
        efficiency = water_level/50.0 #max_wl/wl

        profit = self.price[t]*efficiency

        return profit


class WaterLevel:
    def __init__(self):

        self.first_reserve = 0.0
        self.first_reserve_max = 50.0
        self.second_reserve = 0.0
        self.second_reserve_max = 50.0
        self.first_outflow = 4.0
        self.second_outflow = 4.0
        #self.inflow = []
        self.inflow = [2.7, 4.1, 4.4, 4.2, 2.0, 4.8, 1.9, 2.3, 2.2, 4.4, 1.4, 4.1, 1.6, 4.9, 4.3, 1.5, 3.2, 2.9, 2.6, 4.8, 4.9,
             4.8, 4.0, 1.0]
        if not len(self.inflow) == 24: assert(False)


        #for i in range(0,24):
            #self.inflow.append(random.randrange(10.0,50.0)/10.0)

    def open_or_close(self, t, first_open, second_open=False):
        if first_open:
            self.first_reserve += self.inflow[t]-self.first_outflow
            # Check for overflow in first reserve
            if self.first_reserve > self.first_reserve_max:
                if second_open:
                    self.second_reserve += (self.first_reserve - self.first_reserve) + self.first_outflow - self.second_outflow
                else:
                    self.second_reserve += (self.first_reserve - self.first_reserve) + self.first_outflow
                # Check for overflow in second reserve
                if self.second_reserve > self.second_reserve_max:
                    self.second_reserve = self.second_reserve_max
                self.first_reserve = self.first_reserve_max
            else:
                if second_open:
                    self.second_reserve += self.first_outflow - self.second_outflow
                else:
                    self.second_reserve += self.first_outflow
                # Check for overflow in second reserve
                if self.second_reserve > self.second_reserve_max:
                    self.second_reserve = self.second_reserve_max
        else:
            self.first_reserve += self.inflow[t]
            # Check for overflow in first reserve
            if self.first_reserve > self.first_reserve_max:
                if second_open:
                    self.second_reserve += (self.first_reserve - self.first_reserve_max) - self.second_outflow
                else:
                    self.second_reserve += (self.first_reserve - self.first_reserve_max)
                # Check for overflow in second reserve
                if self.second_reserve > self.second_reserve_max:
                    self.second_reserve = self.second_reserve_max
                self.first_reserve = self.first_reserve_max

        return self.first_reserve

    def get_waterlevel(self):
        return self.first_reserve, self.second_reserve

    def set_waterlevel(self):
        self.first_reserve = 0.0
        self.second_reserve = 0.0


class Judge:
    def __init__(self):
        self.reward_prob = 0.0
        self.max_profit = 75.0
        self.nr_of_iteration_since_change = 0

    def set_max_profit(self, max):
        if max*1.1 < max+15 :
            self.max_profit = max+15
        else :
            self.max_profit = max*1.1
        self.nr_of_iteration_since_change = 0

    def unchanged_iteration(self):
        self.nr_of_iteration_since_change += 1
        return self.nr_of_iteration_since_change

    def reset_unchanged_iteration(self):
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