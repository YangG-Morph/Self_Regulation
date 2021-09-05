



class Caret:
    def __init__(self, size):
        self.size = size
        self.position = {"left": 0, "right": 0, "up": 0, "down": 0}
        self._x = 0

    def left(self):
        self.position["left"] -= 1

    def right(self):
        self.position["right"] += 1

    def up(self):
        self.position["up"] -= 1

    def down(self):
        self.position["down"] += 1

    @property
    def x(self):
        #print(self.position["left"], " and ", self.position["right"])
        return self._x#self.position["left"] + self.position["right"]

    @x.setter
    def x(self, value):
        #print("Before: ", self._x)
        self._x = value
        #print("After: ", self._x)

    @property
    def y(self):
        return self.position["up"] + self.position["down"]
