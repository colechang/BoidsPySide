class Boundary:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def contains_point(self, point):
        return (point.x >= self.x - self.width and
                point.x < self.x + self.width and
                point.y >= self.y - self.height and
                point.y < self.y + self.height)

    def intersects(self, other):
        return not (other.x - other.width > self.x + self.width or
            other.x + other.width < self.x - self.width or
            other.y - other.height > self.y + self.height or
            other.y + other.height < self.y - self.height)
