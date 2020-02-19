import pygame
import sys
import random
import main


def draw_map():
    display_surface.blit(pygame.surfarray.make_surface(_pixel_arr), (0, 0))

    surface = font_2.render("Placing Colonies ...", True, (255, 255, 255))
    display_surface.blit(surface, (_pixel_arr.shape[0] / 2 - 40, 10))

    surface = font_1.render("Press Enter to start ..", True, (255, 255, 255))
    display_surface.blit(surface, (_pixel_arr.shape[0] / 2 - 33, 30))

    for colony in colonies:
        surface = font_3.render(colony[0], True, colony[1])
        display_surface.blit(surface, (colony[3][0], colony[3][1] - 10))

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
font_3 = pygame.font.SysFont('calibri', 10)

# load image
_image = pygame.image.load(map_path)

# get 3d pixel array
_pixel_arr = pygame.surfarray.array3d(_image)

# create display surface
display_surface = pygame.display.set_mode(
    (_pixel_arr.shape[0], _pixel_arr.shape[1]))

# set the pygame window name
pygame.display.set_caption('Empire - Cellular Automaton')
pygame.mouse.set_cursor(*pygame.cursors.broken_x)

draw_map()

# main loop for interacting with the world
start = False
while not start:
    # pygame events
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
            c_color = [random.randint(0, 255), random.randint(
                0, 255), random.randint(0, 255)]
            _pixel_arr[pos[0], pos[1]] = c_color
            colonies.append([str(len(colonies)),
                             c_color, 100, [pos[0], pos[1]]])
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
