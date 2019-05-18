# import pygame module in this program
import pygame


def getPixelArray(filename):
    image = pygame.image.load(filename)
    return pygame.surfarray.array3d(image)


# activate the pygame library .
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()

# define the RGB value
# for white colour
white = (255, 255, 255)

# assigning values to X and Y variable
X = 1000
Y = 700

# create the display surface object
# of specific dimension..e(X, Y).
display_surface = pygame.display.set_mode((X, Y))

# set the pygame window name
pygame.display.set_caption('Image')

# create a surface object, image is drawn on it.
image = pygame.image.load("empire_cellular_automaton/map.jpg")

i = 0
j = 0

# infinite loop
while True:

    # completely fill the surface object
    # with white colour
    display_surface.fill(white)

    # copying the image surface object
    # to the display surface object at
    # (0, 0) coordinate.

    # iterate over the list of Event objects
    # that was returned by pygame.event.get() method.
    for event in pygame.event.get():

        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if event.type == pygame.QUIT:

            # deactivates the pygame library
            pygame.quit()

            # quit the program.
            quit()

        pixels = getPixelArray("empire_cellular_automaton/map.jpg")

        pixels[i][j] = [255, 255, 255]
        i += 1
        j += 1

        surface = pygame.surfarray.make_surface(pixels)

        display_surface.blit(surface, (0, 0))

        # Draws the surface object to the screen.
        pygame.display.update()
