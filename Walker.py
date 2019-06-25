import numpy as np


class Walker:
    def __init__(self, id, electron, position = np.random.uniform(-1, 1, 3)):
        self.id = id
        self.electron = electron
        self.position = position
        self.distance = self.get_distance_from_origin()
        self.merit = 0

    def __str__(self):
        return "Walker {} of electron {] with x = [{}, {}, {}] = {}, m = {}".format(self.id,
                                                                                    self.electron,
                                                                                    self.position[0],
                                                                                    self.position[1],
                                                                                    self.position[2],
                                                                                    self.merit)

    def get_distance_from_origin(self):
        """
        Calculates the Cartesian distance from the center of each walker, simply
        as d = x^2 + y^2 + z^2
        :return: Returns a non-negative scalar value
        """
        d = 0

        for pos in self.position:
            d += pos*pos

        return np.sqrt(d)

    def set_merit(self, merit):
        self.merit = merit