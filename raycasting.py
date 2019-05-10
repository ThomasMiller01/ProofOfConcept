from tkinter import *
import math
from random import randint
import numpy as np
from numpy import cross
from numpy.linalg import norm


class Wall:
    def __init__(self, x1, y1, x2, y2, canvas2d):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.canvas2d = canvas2d

    def draw(self):
        self.wall = self.canvas2d.coords(self.canvas2d.create_line(
            self.x1, self.y1, self.x2, self.x2))


class Ray:
    def __init__(self, x1, y1, x2, y2, canvas2d):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.canvas2d = canvas2d

    def cast(self, wall):
        x1 = wall[0]
        y1 = wall[1]
        x2 = wall[2]
        y2 = wall[3]

        x3 = self.x1
        y3 = self.y1
        x4 = self.x2
        y4 = self.y2

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0:
            return None

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
        if t > 0 and t < 1 and u > 0:
            pt = []
            pt.append(x1 + t * (x2 - x1))
            pt.append(y1 + t * (y2 - y1))
            return pt
        else:
            return None

    def draw(self):
        self.ray_obj = self.canvas2d.create_line(
            self.x1, self.y1, self.x2, self.y2)


class Particle:
    def __init__(self, x, y, canvas2d):
        self.ray_casts = []
        self.rays = []
        self.canvas2d = canvas2d
        self.length = 30

        self.pt_obj = self.canvas2d.create_oval(x - 2, y - 2, x + 2, y + 2)

        self.pt = self.canvas2d.coords(self.pt_obj)

        for angle in range(0, 360):
            if angle % 4 == 0:
                self.rays.append(Ray(self.pt[0], self.pt[1], round(
                    math.cos(math.radians(angle)) * self.length + self.pt[0]), round(math.sin(math.radians(angle)) * self.length + self.pt[1]), self.canvas2d))

        for ray in self.rays:
            ray.draw()

    def look(self, walls):
        for ray in self.rays:
            closest = None
            record = float("inf")
            for wall in walls:
                _wall = wall.wall
                _pt = ray.cast(wall.wall)
                if _pt:
                    p1 = np.array([_wall[0], _wall[1]])
                    p2 = np.array([_wall[2], _wall[3]])
                    p3 = np.array([_pt[0], _pt[1]])
                    d = norm(cross(p1-p2, p1-p3)) / norm(p2-p1)
                    if d < record:
                        record = d
                        closest = _pt
            if closest:
                self.ray_casts.append([self.canvas2d.create_line(self.pt[0], self.pt[1], round(closest[0]), round(closest[1])), self.canvas2d.create_oval(
                    round(closest[0]) - 2, round(closest[1]) - 2, round(closest[0]) + 2, round(closest[1]) + 2)])

    def update(self, x, y, walls):
        self.canvas2d.delete(self.pt_obj)
        for ray in self.rays:
            self.canvas2d.delete(ray.ray_obj)
        for ray_cast in self.ray_casts:
            self.canvas2d.delete(ray_cast[0])
            self.canvas2d.delete(ray_cast[1])
        self.rays = []
        self.pt_obj = None
        self.pt = []
        self.ray_casts = []
        self.pt_obj = self.canvas2d.create_oval(x - 2, y - 2, x + 2, y + 2)

        self.pt = self.canvas2d.coords(self.pt_obj)

        for angle in range(0, 360):
            if angle % 4 == 0:
                self.rays.append(Ray(self.pt[0], self.pt[1], round(
                    math.cos(math.radians(angle)) * self.length + self.pt[0]), round(math.sin(math.radians(angle)) * self.length + self.pt[1]), self.canvas2d))

        for ray in self.rays:
            ray.draw()
        self.look(walls)


pt = None
walls = None


def motion(event):
    x, y = event.x, event.y
    pt.update(x, y, walls)


if __name__ == "__main__":
    canvas_width = 800
    canvas_height = 800

    walls = []

    tk2d = Tk()

    # creating canvas
    canvas2d = Canvas(tk2d,
                      width=canvas_width,
                      height=canvas_height)
    canvas2d.pack()

    pt = Particle(600, 200, canvas2d)

    for i in range(0, 5):
        x1 = randint(0, canvas_width)
        x2 = randint(0, canvas_width)
        y1 = randint(0, canvas_height)
        y2 = randint(0, canvas_height)
        walls.append(Wall(x1, y1, x2, y2, canvas2d))

    for wall in walls:
        wall.draw()
    pt.look(walls)
    canvas2d.bind('<Motion>', motion)

    # starting mainloop
    mainloop()
