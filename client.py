"""Barnes-Hut Hierarchical N-Body Gravitational Engine.
100% Python Standard Library.
"""

import math

class BarnesHutNBody:
    """Barnes-Hut O(N log N) Gravitational N-Body simulation with Quadtree."""
    class QuadNode:
        def __init__(self, x, y, size):
            self.x = x
            self.y = y
            self.size = size
            self.mass = 0.0
            self.com_x = 0.0
            self.com_y = 0.0
            self.body = None
            self.children = None

        def is_leaf(self):
            return self.children is None

    def __init__(self, bodies, theta=0.5, G=1.0):
        self.bodies = bodies
        self.theta = theta
        self.G = G

    def _build_tree(self):
        min_x = min(b["x"] for b in self.bodies)
        max_x = max(b["x"] for b in self.bodies)
        min_y = min(b["y"] for b in self.bodies)
        max_y = max(b["y"] for b in self.bodies)
        size = max(max_x - min_x, max_y - min_y, 1.0) * 1.2
        root = self.QuadNode((min_x + max_x)/2 - size/2, (min_y + max_y)/2 - size/2, size)

        for b in self.bodies:
            self._insert(root, b)
        return root

    def _insert(self, node, b):
        if node.mass == 0.0:
            node.body = b
            node.mass = b["mass"]
            node.com_x = b["x"]
            node.com_y = b["y"]
            return

        if node.is_leaf():
            s = node.size / 2
            node.children = [
                self.QuadNode(node.x, node.y, s),
                self.QuadNode(node.x + s, node.y, s),
                self.QuadNode(node.x, node.y + s, s),
                self.QuadNode(node.x + s, node.y + s, s),
            ]
            old_b = node.body
            node.body = None
            for child in node.children:
                if child.x <= old_b["x"] < child.x + s and child.y <= old_b["y"] < child.y + s:
                    self._insert(child, old_b)
                    break

        s = node.size / 2
        for child in node.children:
            if child.x <= b["x"] < child.x + s and child.y <= b["y"] < child.y + s:
                self._insert(child, b)
                break

        total_m = node.mass + b["mass"]
        node.com_x = (node.com_x * node.mass + b["x"] * b["mass"]) / total_m
        node.com_y = (node.com_y * node.mass + b["y"] * b["mass"]) / total_m
        node.mass = total_m

    def _compute_force(self, node, b):
        if node.mass == 0.0 or node.body is b:
            return 0.0, 0.0

        dx = node.com_x - b["x"]
        dy = node.com_y - b["y"]
        dist = math.hypot(dx, dy)
        eps = 1e-4

        if node.is_leaf() or (node.size / (dist + eps) < self.theta):
            f = self.G * b["mass"] * node.mass / (dist**2 + eps**2)
            return f * (dx / (dist + eps)), f * (dy / (dist + eps))

        fx, fy = 0.0, 0.0
        if node.children:
            for child in node.children:
                cfx, cfy = self._compute_force(child, b)
                fx += cfx
                fy += cfy
        return fx, fy

    def step(self, dt=0.01):
        root = self._build_tree()
        forces = [self._compute_force(root, b) for b in self.bodies]
        for b, (fx, fy) in zip(self.bodies, forces):
            ax = fx / b["mass"]
            ay = fy / b["mass"]
            b["vx"] += ax * dt
            b["vy"] += ay * dt
            b["x"] += b["vx"] * dt
            b["y"] += b["vy"] * dt
