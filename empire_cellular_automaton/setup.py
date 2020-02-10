import pygame
import numpy as np
import time
import copy
import sys
import settings


class setup:
    def __init__(self, _settings):
        self._settings = _settings

        # [gen, day, people]
        self.stats = np.zeros((0, 3)).astype('int')

        # init people and colonies array
        # [id, colony_id, age, strength, reproduction_value, disease, x, y]
        self.people = np.zeros((0, 8)).astype('int')
        # [id, name, color]
        self.colonies = np.zeros((0, 3)).astype('int')

        c_id = 0
        p_id = 0

        # init people and colonies
        for colony in settings.colonies:
            self.colonies = np.append(self.colonies, np.array(
                [[c_id, colony[0], colony[1]]]), axis=0)
            for i in range(colony[2]):
                self.people = np.append(self.people, np.array([[p_id, c_id, 0, np.random.randint(self._settings['p_strength'][0], self._settings['p_strength'][1]), np.random.randint(
                    self._settings['p_reproductionValue'][0], self._settings['p_reproductionValue'][1]), np.random.randint(2), colony[3][0], colony[3][1]]]), axis=0)
                p_id += 1
            c_id += 1

        if settings.display_map:
            # init pygame
            pygame.init()
            pygame.font.init()

            # font for stats
            self.font_size = 15
            self.font = pygame.font.SysFont('calibri', self.font_size)

        # load image
        self._image = pygame.image.load(settings.map_path)

        # get 3d pixel array
        self._pixel_arr = pygame.surfarray.array3d(self._image)

        # set image dimensions
        self.h = self._pixel_arr.shape[0]
        self.w = self._pixel_arr.shape[1]

        if settings.display_map:
            # create display surface
            self.display_surface = pygame.display.set_mode((self.h, self.w))

            # set the pygame window name
            pygame.display.set_caption('Empire - Cellular Automaton')

            # completely fill the surface object with white color
            self.display_surface.fill([255, 255, 255])
            self.updateMap()

            self._stats = {
                'gen': 0,
                'day': 0,
                'people': self.people
            }

    def run(self):
        start_time = time.time()

        for g in range(self._settings['maxGen']):
            print("gen " + str(g) + " started calculating ..")
            gen_start_time = time.time()

            # render gen
            self.render_gen(g)

            gen_end_time = time.time()
            print("gen " + str(g) + " rendered in " +
                  str(round(gen_end_time - gen_start_time, 4)) + "s")
            print("******")

        end_time = time.time()

        print("- finished calculating ...")
        print("- time elapsed: " + str(round(end_time - start_time, 4)) + "s")

        return self.stats

    def render_gen(self, gen):
        if settings.display_map:
            self._stats['gen'] = gen
        # foreach day
        for i in range(settings.days_per_generation):
            # foreach person
            for person in self.people:
                self.render_person(person, np.where(
                    self.people[:, 0] == person[0])[0][0])

            # update self.stats
            self.stats = np.append(
                self.stats, [[gen, i, copy.deepcopy(self.people)]], axis=0)

            if settings.display_map:
                self._stats['day'] = i
                self._stats['people'] = self.people
                self.updateMap()
                self.updateStats(self._stats)

                # pygame events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit(0)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit(0)

    def render_person(self, person, p_index):
        # age
        if person[2] > person[3]:
            self.set_pixel_color_back(person[6], person[7], person[0])
            self.people = np.delete(self.people, np.where(
                self.people[:, 0] == person[0])[0][0], axis=0)
            return
        else:
            person[2] += 1

        # reproduction
        if person[4] > self._settings['p_reproductionThreshold']:
            # person reproduces
            # do mutations
            self.people = np.append(self.people, np.asarray([[self.people[len(
                self.people) - 1][0] + 1, person[1], 0, person[3], 0, person[5], person[6], person[7]]]), axis=0)
            person[4] = 0
        else:
            person[4] += 1

        # disease
        # here

        # moving
        neighbour_found = False
        while not neighbour_found:
            # get rnd neighbour
            neighbour = self.getRandomNeighbour((person[6], person[7]))

            # check if neighbour is water
            if not np.array_equal(self._pixel_arr[neighbour[0], neighbour[1]], settings.world_pixel['water']):
                neighbour_found = True

        # check if neighbour field is empty
        indices_all = np.where(
            np.all(self.people[:, 6:] == neighbour, axis=1))[0]
        indices = np.unique(indices_all, return_index=True)[1]

        if indices.size == 0:
            self.set_pixel_color_back(person[6], person[7], person[0])
            self.updatePixel(neighbour[0], neighbour[1],
                             self.colonies[person[1]][2])
            person[6] = neighbour[0]
            person[7] = neighbour[1]
        else:
            own_colony = False
            for index in indices:
                if self.people[indices_all[index]][1] == person[1]:
                    self.set_pixel_color_back(person[6], person[7], person[0])
                    person[6] = neighbour[0]
                    person[7] = neighbour[1]
                    own_colony = True
                    break
            if not own_colony:
                # fight
                pass
        self.people[p_index] = person

    def set_pixel_color_back(self, x, y, p_id):
        # check if somebody remains on the other field, if not, color it empty
        old_indices_all = np.where(
            np.all(self.people[:, 6:] == [x, y], axis=1))[0]
        old_indices = np.unique(old_indices_all, return_index=True)[1]

        if old_indices.size == 1 and self.people[old_indices_all[old_indices[0]]][0] == p_id:
            # color field empty
            self.updatePixel(x, y, settings.world_pixel['empty'])

    def getRandomNeighbour(self, pixel):
        positions = [
            (pixel[0], pixel[1] + 1),  # oben
            (pixel[0] + 1, pixel[1] + 1),  # oben rechts
            (pixel[0] + 1, pixel[1]),  # rechts
            (pixel[0] + 1, pixel[1] - 1),  # unten rechts
            (pixel[0], pixel[1] - 1),  # unten
            (pixel[0] - 1, pixel[1] - 1),  # unten links
            (pixel[0] - 1, pixel[1]),  # link
            (pixel[0] - 1, pixel[1] + 1)  # oben links
        ]
        valid_pos = False
        pos = (-1, -1)
        while not valid_pos:
            pos = positions[np.random.randint(len(positions))]
            if not (pos[0] <= 0 or pos[0] >= self.w and pos[1] <= 0 or pos[1] >= self.h):
                valid_pos = True
        return pos

    def updateMap(self):
        surface = pygame.surfarray.make_surface(self._pixel_arr)
        self.display_surface.blit(surface, (0, 0))

    def updateStats(self, stats):
        x = 5
        y = 5
        # render generation
        surface = self.font.render(
            'Generation: ' + str(stats['gen']) + ', Day: ' + str(stats['day']), True, (255, 255, 255))

        self.display_surface.blit(surface, (x, y))

        # render colony data
        for i in range(0, len(self.colonies)):
            c_people = np.where(stats['people'][:, 1]
                                == self.colonies[i][0])[0]
            surface = self.font.render(
                'Colony ' + str(self.colonies[i][0]) + ': ' + str(len(c_people)), True, (255, 255, 255))
            self.display_surface.blit(
                surface, (x, 20 + y + self.font_size * i))

        pygame.display.update()

    def updatePixel(self, x, y, color):
        # set pixel color
        self._pixel_arr[x, y] = color
