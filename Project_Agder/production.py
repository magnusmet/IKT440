

class Production:
    def __init__(self, price=[]):
        if len(price) == 0:
            self.price = [15,15,8,14,9,10,7,14,13,9,12,11,10,10,8,5,5,14,9,5,8,9,10,7]
        else:
            self.price = price

    def production(self, t, water_level, capacity, outflow):
        efficiency = water_level/capacity
        if outflow > water_level:
            outflow = water_level
        if water_level > capacity:
            print water_level
            assert False

        profit = self.price[t]*efficiency*outflow
        return profit
