import numpy as np


class Walker:
    def __init__(self, id, position, dims = 1):
        self.id         = id
        self.parents    = []
        self.position   = position
        self.dims       = dims
        self.distance   = self.get_distance_from_origin()
        self.merit      = 0

    def __str__(self):

        if self.dims == 3:
            return "Walker %d with x = [%f, %f, %f], m = %d" % (self.id, self.position[0],self.position[1], self.position[2], self.merit)
        elif self.dims == 1:
            return "Walker %d with x = [%f], m = %d" % (self.id, self.position[0], self.merit)
        else:
            return "Dimension not implemented."

    def get_distance_from_origin(self):
        """
        Calculates the Cartesian distance from the center of each walker, simply
        as d = x^2 + y^2 + z^2
        :return: Returns a non-negative scalar value
        """

        return np.linalg.norm(self.position, 2)

    def set_merit(self, merit):
        self.merit = merit