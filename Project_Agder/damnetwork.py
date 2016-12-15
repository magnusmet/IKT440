from dam import Dam


class DamNetwork:
    def __init__(self, inflow=[], dams=[]):
        if len(inflow) == 0:
            self.main_inflow = [2.7, 4.1, 4.4, 4.2, 2.0, 4.8,
                                1.9, 2.3, 2.2, 4.4, 1.4, 4.1,
                                1.6, 4.9, 4.3, 1.5, 3.2, 2.9,
                                2.6, 4.8, 4.9, 4.8, 4.0, 1.0]
        else:
            self.main_inflow = inflow
        if len(dams) == 0:
            self.dams = [Dam()]
        else:
            self.dams = dams

    def add_dam(self, dam):
        self.dams.append(dam)

    def run_network(self, t, dams_open):
        next_inflow = self.dams[0].get_water(self.main_inflow[t], dams_open[0])
        for i in range(1, len(self.dams)):
            next_inflow = self.dams[i].get_water(next_inflow, dams_open[i])

    def get_dams(self):
        return self.dams

    def set_dams(self, dams):
        self.dams = dams

    def get_dam(self, i):
        try:
            return self.dams[i]
        except:
            return self.dams[len(self.dams)-1]

    def set_dam(self, i, dam):
        try:
            self.dams[i] = dam
        except:
            self.add_dam(dam)

    def set_main_inflow(self, main_inflow):
        self.main_inflow = main_inflow

    def get_main_inflow(self):
        return self.main_inflow