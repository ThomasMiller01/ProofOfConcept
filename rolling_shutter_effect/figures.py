import numpy as np


def star(t, points=5):
    alpha = (2 * np.pi) / (points * 2)
    radius = 12
    starXY = [100, 100]
    tmp_pts = []
    for i in range(0, points * 2 + 1):
        r = radius * ((points * 2 + 1 - i) % 2 + 0.2) / 2
        omega = alpha * (points * 2 + 1 - i)
        x = r * np.sin(omega) + starXY[0]
        y = r * np.cos(omega) + starXY[1]
        tmp_pts.append(rotatePt((x, y), starXY, t))
    return tmp_pts


def triangle(t):
    cx = 100
    cy = 100

    coords = [(90, 90), (110, 90), (100, 110)]

    tmp_pts = []

    for coord in coords:
        tmp_pts.append(rotatePt(coord, (cx, cy), t))
    tmp_pts.append(rotatePt(coords[0], (cx, cy), t))
    return tmp_pts


def rectangle(t):
    cx = 100
    cy = 100
    width = 20

    coords = [(cx - width / 2, cy - width / 2), (cx + width / 2, cy - width / 2),
              (cx + width / 2, cy + width / 2), (cx - width / 2, cy + width / 2)]
    tmp_pts = []

    for coord in coords:
        tmp_pts.append(rotatePt(coord, (cx, cy), t))

    tmp_pts.append(rotatePt(coords[0], (cx, cy), t))

    return tmp_pts


def rotatePt(pt, centerPt, angle):
    tempX = pt[0] - centerPt[0]
    tempY = pt[1] - centerPt[1]

    rotatedX = tempX * np.cos(angle) - tempY * np.sin(angle)
    rotatedY = tempX * np.sin(angle) + tempY * np.cos(angle)

    x = rotatedX + centerPt[0]
    y = rotatedY + centerPt[1]
    return (x, y)
