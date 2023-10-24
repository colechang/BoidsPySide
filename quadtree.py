from boundary import Boundary
class Quadtree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary  # The boundary of this quadtree node
        self.capacity = capacity  # The maximum number of boids a node can hold
        self.boids = []  # The boids stored in this node
        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None

    # Method to insert a boid into the quadtree
    def insert(self, boid):
        if not self.boundary.contains_point(boid):
            return False  # Boid is not within the boundary, so we won't add it

        if len(self.boids) < self.capacity:
            self.boids.append(boid)
            return True  # Added the boid to this node

        if self.nw is None:
            self.subdivide()  # Split this node into four child nodes if it's not already

        # Try adding the boid to the appropriate child node(s)
        if self.nw.insert(boid):
            return True
        if self.ne.insert(boid):
            return True
        if self.sw.insert(boid):
            return True
        if self.se.insert(boid):
            return True
    def clear(self):
        self.boids = []
    # Method to subdivide the current node into four child nodes
    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.width / 2
        h = self.boundary.height / 2
        ne_boundary = Boundary(x + w, y + h, w, h)
        nw_boundary = Boundary(x - w, y + h, w, h)
        se_boundary = Boundary(x + w, y - h, w, h)
        sw_boundary = Boundary(x - w, y - h, w, h)
        self.ne = Quadtree(ne_boundary, self.capacity)
        self.nw = Quadtree(nw_boundary, self.capacity)
        self.se = Quadtree(se_boundary, self.capacity)
        self.sw = Quadtree(sw_boundary, self.capacity)

    # Method to query boids within a given boundary
    def query(self, search_boundary):
        found_boids = []
        if not self.boundary.intersects(search_boundary):
            return found_boids

        for boid in self.boids:
            if search_boundary.contains_point(boid):
                found_boids.append(boid)

        if self.nw is None:
            return found_boids

        found_boids.extend(self.nw.query(search_boundary))
        found_boids.extend(self.ne.query(search_boundary))
        found_boids.extend(self.sw.query(search_boundary))
        found_boids.extend(self.se.query(search_boundary))

        return found_boids