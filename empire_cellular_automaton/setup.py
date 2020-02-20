import pygame
import sys
import random
import numpy as np
import main


def draw_map():
    display_surface.blit(pygame.transform.smoothscale(pygame.surfarray.make_surface(_pixel_arr[int(zoom_dim[0][0]):int(
        zoom_dim[0][1]), int(zoom_dim[1][0]):int(zoom_dim[1][1])]), (_pixel_arr.shape[0], _pixel_arr.shape[1])), (0, 0))

    surface = font_2.render("Placing Colonies ...", True, (255, 255, 255))
    display_surface.blit(surface, (_pixel_arr.shape[0] / 2 - 40, 10))

    surface = font_1.render("Press Enter to start ..", True, (255, 255, 255))
    display_surface.blit(surface, (_pixel_arr.shape[0] / 2 - 33, 30))

    y = 0
    for colony in colonies:
        y += 10
        surface = font_1.render(
            'Colony ' + colony[0] + ', [' + str(colony[3][0]) + ', ' + str(colony[3][1]) + ']', True, colony[1])
        display_surface.blit(surface, (10, y))

    pygame.display.update()


display_map = True
map_path = 'map.jpg'
world_pixel = {'water': [3, 0, 168], 'empty': [5, 124, 0]}
colonies = []

# init pygame
pygame.init()
pygame.font.init()

clock = pygame.time.Clock()

# font for stats
font_1 = pygame.font.SysFont('calibri', 15)
font_2 = pygame.font.SysFont('calibri', 20)

# load image
_image = pygame.image.load(map_path)

# get 3d pixel array
_pixel_arr = pygame.surfarray.array3d(_image)

h = _pixel_arr.shape[0]
w = _pixel_arr.shape[1]


# create display surface
display_surface = pygame.display.set_mode((h, w))

scale = 1
zoom_dim = [(0, h), (0, w)]

# set the pygame window name
pygame.display.set_caption('Empire - Cellular Automaton')
pygame.mouse.set_cursor(*pygame.cursors.broken_x)

draw_map()

# main loop for interacting with the world
start = False
while not start:
    # pygame events
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        old_zoom_dim = zoom_dim
        zoom_dim = [(zoom_dim[0][0] + 10, zoom_dim[0][1] - 10),
                    (zoom_dim[1][0] + 7, zoom_dim[1][1] - 7)]
        scale += 0.5
        if zoom_dim[0][0] > zoom_dim[0][1] or zoom_dim[1][0] > zoom_dim[1][1] or zoom_dim[0][0] == zoom_dim[0][1] or zoom_dim[1][0] == zoom_dim[1][1]:
            zoom_dim = old_zoom_dim
        if zoom_dim[0][0] <= 0 or zoom_dim[0][1] >= w and zoom_dim[1][0] <= 0 or zoom_dim[1][1] >= h:
            zoom_dim = [(0, h), (0, w)]
            scale = 1
        draw_map()
    elif keys[pygame.K_s]:
        zoom_dim = [(zoom_dim[0][0] - 10, zoom_dim[0][1] + 10),
                    (zoom_dim[1][0] - 7, zoom_dim[1][1] + 7)]
        scale -= 0.5
        if zoom_dim[0][0] > zoom_dim[0][1] or zoom_dim[1][0] > zoom_dim[1][1] or zoom_dim[0][0] == zoom_dim[0][1] or zoom_dim[1][0] == zoom_dim[1][1]:
            zoom_dim = old_zoom_dim
        if zoom_dim[0][0] <= 0 or zoom_dim[0][1] >= w and zoom_dim[1][0] <= 0 or zoom_dim[1][1] >= h:
            zoom_dim = [(0, h), (0, w)]
            scale = 1
        draw_map()
    elif keys[pygame.K_UP]:
        zoom_dim = [
            (zoom_dim[0][0], zoom_dim[0][1]), (zoom_dim[1][0] - 20 / scale, zoom_dim[1][1] - 20 / scale)]
        if zoom_dim[0][0] <= 0 or zoom_dim[0][1] >= w and zoom_dim[1][0] <= 0 or zoom_dim[1][1] >= h:
            zoom_dim = [(0, h), (0, w)]
        draw_map()
    elif keys[pygame.K_DOWN]:
        zoom_dim = [
            (zoom_dim[0][0], zoom_dim[0][1]), (zoom_dim[1][0] + 20 / scale, zoom_dim[1][1] + 20 / scale)]
        if zoom_dim[0][0] <= 0 or zoom_dim[0][1] >= w and zoom_dim[1][0] <= 0 or zoom_dim[1][1] >= h:
            zoom_dim = [(0, h), (0, w)]
        draw_map()
    elif keys[pygame.K_LEFT]:
        zoom_dim = [
            (zoom_dim[0][0] - 20 / scale, zoom_dim[0][1] - 20 / scale), (zoom_dim[1][0], zoom_dim[1][1])]
        if zoom_dim[0][0] <= 0 or zoom_dim[0][1] >= w and zoom_dim[1][0] <= 0 or zoom_dim[1][1] >= h:
            zoom_dim = [(0, h), (0, w)]
        draw_map()
    elif keys[pygame.K_RIGHT]:
        zoom_dim = [
            (zoom_dim[0][0] + 20 / scale, zoom_dim[0][1] + 20 / scale), (zoom_dim[1][0], zoom_dim[1][1])]
        if zoom_dim[0][0] <= 0 or zoom_dim[0][1] >= w and zoom_dim[1][0] <= 0 or zoom_dim[1][1] >= h:
            zoom_dim = [(0, h), (0, w)]
        draw_map()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)
            elif event.key == pygame.K_RETURN:
                if colonies:
                    start = True
                else:
                    print("[Error] missing colonies ...")
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            pos_mapped = (int(np.interp(pos[0], (0, h), (zoom_dim[0][0], zoom_dim[0][1]))), int(np.interp(
                pos[1], (0, w), (zoom_dim[1][0], zoom_dim[1][1]))))
            c_color = [random.randint(0, 255), random.randint(
                0, 255), random.randint(0, 255)]
            _pixel_arr[pos_mapped[0], pos_mapped[1]] = c_color
            colonies.append([str(len(colonies)),
                             c_color, 100, [pos_mapped[0], pos_mapped[1]]])
            draw_map()

pygame.mouse.set_cursor(*pygame.cursors.arrow)

settings = {
    'p_strength': [0, 100],
    'p_reproductionValue': [0, 70],
    'p_reproductionThreshold': 50,
    'maxGen': 100,
    'display_map': display_map,
    'colonies': colonies,
    'world_pixel': world_pixel,
    'days_per_generation': 100,
    'map_path': map_path
}

_setup = main.setup(settings)

_setup.run()
