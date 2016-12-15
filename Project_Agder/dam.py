

class Dam:
    def __init__(self, water_level=0.0, max_capacity=50.0, outflow=4.0):
        self.water_level = water_level
        self.max_capacity = max_capacity
        self.outflow = outflow

    def get_water(self, inflow, open):
        self.water_level += inflow
        if open == 1:
            if self.water_level - self.outflow < 0:
                outflow = self.water_level
                self.water_level = 0.0
                return outflow
            self.water_level -= self.outflow
            if self.water_level > self.max_capacity:
                overflow_and_outflow = self.outflow + (self.water_level - self.max_capacity)
                self.water_level = self.max_capacity
                return overflow_and_outflow
            else:
                return self.outflow
        else:
            if self.water_level > self.max_capacity:
                overflow = self.water_level - self.max_capacity
                self.water_level = self.max_capacity
                return overflow
            else:
                return 0

    def set_water_level(self, water_level=0.0):
        self.water_level = water_level

    def get_water_level(self):
        if self.water_level < 0 or self.water_level > self.max_capacity:
            print 'Invalid water level'
            assert False
        return self.water_level

    def set_max_capacity(self, max_capacity):
        self.max_capacity = max_capacity

    def set_outflow(self, outflow):
        self.outflow = outflow

    def get_outflow(self):
        return self.outflow
