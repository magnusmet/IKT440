import random



class Production:
    def __init__(self):
        self.price = [15,15,8,14,9,10,7,14,13,9,12,11,10,10,8,5,5,14,9,5,8,9,10,7]
        #self.price = [7,7,7,7,7,7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8,8,8,8]
        self.max_profit = 15*24 #maxprice*24h
        self.efficiency = []

    def production(self, t, water_level):
        if water_level == 0:
            return 0
        efficiency = water_level/50.0 #max_wl/wl

        profit = self.price[t]*efficiency

        return profit





class WaterLevel:
    def __init__(self):

        self.water_level = 0.0
        self.outflow = 4.0
        self.inflow = []


        for i in range(0,24):
            self.inflow.append(random.randrange(10.0,50.0)/10.0)


    def openOrClose(self, t, open):
        if open:
            if self.inflow[t] > self.outflow:
                difference = self.inflow[t] - self.outflow
                if self.water_level >= 50.0:
                    self.water_level = 50.0

                else:
                    self.water_level += difference

            if self.outflow > self.inflow[t]:
                difference = self.outflow - self.inflow[t]
                if self.water_level == 0:
                    return -1
                else:
                    self.water_level -= difference

        else:
            self.water_level += self.inflow[t]
            if self.water_level >= 50.0:
                self.water_level = 50.0

        return self.water_level

    def waterLevel(self, production):

        if self.inflow>self.outflow:
            difference = self.inflow-self.outflow
            if self.water_level >= 50.0:
                self.water_level = 50.0
                return self.water_level
            else:
                self.water_level+=difference
                return self.water_level
        if self.outflow>self.inflow:
            difference = self.outflow-self.inflow
            if self.water_level==0:
                return -1
            else:
                self.water_level -= difference
                return self.water_level

        if production == True:
            self.water_level -= self.outflow
            return self.water_level
        else:
            return self.water_level

    def getWaterlevel(self):
        return self.water_level

    def setWaterlevel(self):
        self.water_level = 0.0

class Judge:
    def __init__(self):
        self.reward_prob = 0.0

    def reward_probability(self, profit):
        self.reward_prob = profit/(100) #profit/maxprofit


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