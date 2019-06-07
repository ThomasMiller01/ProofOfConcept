from tkinter import *
import math
from random import randint
import numpy as np
from numpy import cross
from numpy.linalg import norm
from numpy import interp
import colorsys


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
    def __init__(self, x, y, angleMin, angleMax, walls, canvas2d):
        self.ray_casts = []
        self.rays = []
        self.canvas2d = canvas2d
        self.length = 10
        self.angleMin = angleMin
        self.angleMax = angleMax
        self.update(x, y, self.angleMin, self.angleMax, walls)

    def look(self, walls):
        for ray in self.rays:
            closest = None
            record = float("inf")
            for wall in walls:
                _wall = wall.wall
                _pt = ray.cast(wall.wall)
                if _pt:
                    ax = self.pt[0] - _pt[0]
                    ay = self.pt[1] - _pt[1]
                    d = math.sqrt(ax**2 + ay**2)
                    if d < record:
                        record = d
                        closest = _pt
            if closest:
                setattr(ray, 'distance', d)
                [ray if ray.ray_obj == ray.ray_obj else ray for ray in self.rays]
                self.ray_casts.append([[self.canvas2d.create_line(self.pt[0], self.pt[1], round(closest[0]), round(closest[1])), d], self.canvas2d.create_oval(
                    round(closest[0]) - 2, round(closest[1]) - 2, round(closest[0]) + 2, round(closest[1]) + 2)])

    def delete(self):
        self.canvas2d.delete(self.pt_obj)
        for ray in self.rays:
            self.canvas2d.delete(ray.ray_obj)
        for ray_cast in self.ray_casts:
            self.canvas2d.delete(ray_cast[0][0])
            self.canvas2d.delete(ray_cast[1])
        self.rays = []
        self.pt_obj = None
        self.pt = []
        self.ray_casts = []

    def update(self, x, y, angleMin, angleMax, walls):
        self.pt_obj = self.canvas2d.create_oval(x - 5, y - 5, x + 5, y + 5)
        self.pt = [x, y]
        self.angleMin = angleMin
        self.angleMax = angleMax

        for angle in range(self.angleMin, self.angleMax):
            self.rays.append(Ray(self.pt[0], self.pt[1], round(
                math.cos(math.radians(angle)) * self.length + self.pt[0]), round(math.sin(math.radians(angle)) * self.length + self.pt[1]), self.canvas2d))

        for ray in self.rays:
            ray.draw()
        self.look(walls)


pt = None
walls = None
canvas2d = None
canvas3d = None
angleMin = None
angleMax = None
canvas_width = None
canvas_height = None

canvas3d_rays = []


def motion(event):
    x, y = event.x, event.y
    pt.delete()
    pt.update(x, y, angleMin, angleMax, walls)


def move(event):
    coords = pt.pt
    angleMin = pt.angleMin
    angleMax = pt.angleMax
    pt.delete()
    if event.keysym == 'Up':
        pt.update(coords[0], coords[1] - 10, angleMin, angleMax, walls)
    elif event.keysym == 'Down':
        pt.update(coords[0], coords[1] + 10, angleMin, angleMax, walls)
    elif event.keysym == 'Right':
        pt.update(coords[0] + 10, coords[1], angleMin, angleMax, walls)
    elif event.keysym == 'Left':
        pt.update(coords[0] - 10, coords[1], angleMin, angleMax, walls)
    update3dCanvas()


def rotate(event):
    coords = pt.pt
    angleMin = pt.angleMin
    angleMax = pt.angleMax
    pt.delete()
    if event.keysym == 'a':
        pt.update(coords[0], coords[1], angleMin - 5, angleMax - 5, walls)
    else:
        pt.update(coords[0], coords[1], angleMin + 5, angleMax + 5, walls)
    update3dCanvas()


def close(event):
    canvas2d.destroy()
    sys.exit(0)


def update3dCanvas():
    global canvas3d_rays
    for ray in canvas3d_rays:
        canvas3d.delete(ray)
        canvas3d_rays = []
    rays = pt.rays
    for i in range(0, rays.__len__()):
        ray = rays[i]
        if hasattr(ray, 'distance'):
            sq = ray.distance**2
            wSq = canvas_width**2
            brightness = interp(sq, [0, wSq], [1, 0])
            height = interp(ray.distance, [0, canvas_height], [
                canvas_height, 0])
        else:
            brightness = 0
            height = canvas_height

        hue = 0
        saturation = 1.0

        r, g, b = colorsys.hls_to_rgb(hue, brightness / 10.0, saturation)

        color = '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))

        x1 = i * 10
        x2 = x1 + 10
        y1 = canvas_height / 2 + height / 2
        y2 = canvas_height / 2 - height / 2

        canvas3d_rays.append(canvas3d.create_rectangle(
            x1, y1, x2, y2, fill=color))


if __name__ == "__main__":
    canvas_width = 800
    canvas_height = 800

    angleMin = 0
    angleMax = 80

    walls = []

    tk2d = Tk()
    tk3d = Tk()

    # creating 2d canvas
    canvas2d = Canvas(tk2d,
                      width=canvas_width,
                      height=canvas_height)
    canvas2d.pack()

    # creating 3d canvas
    canvas3d = Canvas(tk3d,
                      width=canvas_width,
                      height=canvas_height)
    canvas3d.pack()
    canvas3d.configure(background="black")

    for i in range(0, 5):
        x1 = randint(0, canvas_width)
        x2 = randint(0, canvas_width)
        y1 = randint(0, canvas_height)
        y2 = randint(0, canvas_height)
        walls.append(Wall(x1, y1, x2, y2, canvas2d))

    for wall in walls:
        wall.draw()

    pt = Particle(400, 400, angleMin, angleMax, walls, canvas2d)
    update3dCanvas()

    # canvas2d.bind('<Motion>', motion)
    tk2d.bind('<Left>', move)
    tk2d.bind('<Right>', move)
    tk2d.bind('<Up>', move)
    tk2d.bind('<Down>', move)
    tk2d.bind('a', rotate)
    tk2d.bind('d', rotate)
    tk2d.bind('<Escape>', close)
    tk3d.bind('<Escape>', close)

    # starting mainloop
    mainloop()
