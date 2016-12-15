

class Production:
    def __init__(self, price=[]):
        if len(price) == 0:
            self.price = [15,15,8,14,9,10,7,14,13,9,12,11,10,10,8,5,5,14,9,5,8,9,10,7]
        else:
            self.price = price

    def production(self, t, water_level, outflow):
        if water_level == 0:
            return 0
        efficiency = water_level/50.0 #max_wl/wl

        profit = self.price[t]*efficiency*outflow

        return profit / 4.0  # Divide by 4 to keep familiar results
