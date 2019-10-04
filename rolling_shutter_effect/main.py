import matplotlib.pyplot as plt
import numpy as np
from numpy import ones, vstack
from numpy.linalg import lstsq

import figures

corner_pts = []
corner_funcs = []

line_func = None


def init(t):
    global corner_pts
    corner_pts = figures.star(t, 8)


def init_func():
    global corner_pts
    global line_func
    for i in range(0, corner_pts.__len__()-1):
        points = [corner_pts[i], corner_pts[i+1]]

        m = (points[1][1] - points[0][1]) / (points[1][0] - points[0][0])
        b = points[0][1] - m * points[0][0]

        # print(f"f(x)={m}*x+{b}")
        corner_funcs.append([[m, b], points])

    # init marker line func
    line_func = np.amax(np.asarray(corner_pts), axis=0)[1]


def show_plot(red_pts=None, red_pts_only=False):
    global line_func
    if not red_pts_only:
        # show star points
        ptsX = []
        ptsY = []
        n = []
        j = 0
        for corner in corner_pts:
            ptsX.append(corner[0])
            ptsY.append(corner[1])
            j = j + 1
            n.append(j)
        plt.scatter(ptsX, ptsY, s=100)
        for i, txt in enumerate(n):
            plt.annotate(txt, (ptsX[i], ptsY[i]))
        i = 0

    if red_pts:
        rPtsX = []
        rPtsY = []
        for rPt in red_pts:
            rPtsX.append(rPt[0])
            rPtsY.append(rPt[1])
        plt.scatter(rPtsX, rPtsY, s=10)

    # show star lines
    if corner_funcs and not red_pts_only:
        for func in corner_funcs:
            x = np.linspace(func[1][0][0], func[1][1][0], 100)
            i = i + 1
            plt.plot(x, func[0][0]*x+func[0][1], '-r',
                     label=str(i) + ' - ' + str(i + 1))

    # show marker line
    if line_func and not red_pts_only:
        minX = np.amin(np.asarray(corner_pts), axis=0)[0]
        maxX = np.amax(np.asarray(corner_pts), axis=0)[0]
        x = np.linspace(minX, maxX, 100)
        plt.plot(x, 0*x+line_func, '-b', label='marker-line')

    # plt.legend(loc='upper left')
    plt.gca().set_aspect("equal")
    plt.show()


def get_intersection():
    # get func
    func = []
    for _func in corner_funcs:
        y1 = _func[1][0][1]
        y2 = _func[1][1][1]
        if y1 < y2:
            if line_func >= y1 and line_func <= y2:
                func.append(_func)
        else:
            if line_func >= y2 and line_func <= y1:
                func.append(_func)

    pts = []
    for f in func:
        # get pt
        s = np.vstack([f[1][0], f[1][1], [0, line_func], [1, line_func]])
        h = np.hstack((s, np.ones((4, 1))))
        l1 = np.cross(h[0], h[1])
        l2 = np.cross(h[2], h[3])
        x, y, z = np.cross(l1, l2)
        if z == 0:
            pts.append((float('inf'), float('inf')))
        else:
            pts.append((x/z, y/z))
    return pts


if __name__ == '__main__':
    degree = 0
    init(degree * np.pi / 180)
    init_func()
    intersections = []
    minX = np.amin(np.asarray(corner_pts), axis=0)[1]
    maxX = np.amax(np.asarray(corner_pts), axis=0)[1]
    timestamps = np.linspace(maxX, minX, 500)
    jump = 360 / timestamps.__len__()
    for t in timestamps:
        corner_pts.clear()
        corner_funcs.clear()
        degree = degree + jump
        init(degree * np.pi / 180)
        init_func()
        line_func = t
        intersection = get_intersection()
        intersections.extend(intersection)
    # show_plot(intersections)
    show_plot(intersections, True)
