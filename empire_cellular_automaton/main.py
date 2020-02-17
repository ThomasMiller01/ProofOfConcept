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

        # [id, colony_id, age, strength, reproduction_value, disease, x, y]
        self.people = np.zeros((0, 8)).astype('int')

        # [id, name, color]
        self.colonies = np.zeros((0, 3)).astype('int')

        self.c_id = 0
        self.p_id = 0

        # init people and colonies
        for colony in settings.colonies:
            self.colonies = np.append(self.colonies, np.array(
                [[self.c_id, colony[0], colony[1]]]), axis=0)
            for i in range(colony[2]):
                self.people = np.append(self.people, np.array([[self.p_id, self.c_id, 0, np.random.randint(self._settings['p_strength'][0], self._settings['p_strength'][1]), np.random.randint(
                    self._settings['p_reproductionValue'][0], self._settings['p_reproductionValue'][1]), np.random.randint(2), colony[3][0], colony[3][1]]]), axis=0)
                self.p_id += 1
            self.c_id += 1
        self.p_id += 1

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
        self._pixel_arr_copy = copy.deepcopy(self._pixel_arr)

        # set image dimensions
        self.h = self._pixel_arr.shape[0]
        self.w = self._pixel_arr.shape[1]

        if settings.display_map:
            self.scale = 0
            self.zoom_dim = [(0, self.h), (0, self.w)]

            # create display surface
            self.display_surface = pygame.display.set_mode(
                (self.zoom_dim[0][1] - self.zoom_dim[0][0], self.zoom_dim[1][1] - self.zoom_dim[1][0]))

            # set the pygame window name
            pygame.display.set_caption('Empire - Cellular Automaton')

            # completely fill the surface object with white color
            self.display_surface.fill([255, 255, 255])
            self.updateMap()

            self._stats = {
                'gen': 0,
                'day': 0,
                'people': copy.deepcopy(self.people)
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
            # reset world pixels
            self._pixel_arr = copy.deepcopy(self._pixel_arr_copy)

            # foreach person
            for person in self.people:
                p_index = np.where(self.people[:, 0] == person[0])[0]
                if len(p_index) != 0:
                    self.render_person(person, p_index[0])

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
                        elif event.key == pygame.K_w:
                            self.zoom_dim = [(self.zoom_dim[0][0] + 20, self.zoom_dim[0][1] - 20),
                                             (self.zoom_dim[1][0] + 14, self.zoom_dim[1][1] - 14)]
                            self.scale += 0.5
                        elif event.key == pygame.K_s:
                            self.zoom_dim = [(self.zoom_dim[0][0] - 20, self.zoom_dim[0][1] + 20),
                                             (self.zoom_dim[1][0] - 14, self.zoom_dim[1][1] + 14)]
                            self.scale -= 0.5
                        elif event.key == pygame.K_UP:
                            self.zoom_dim = [
                                (self.zoom_dim[0][0], self.zoom_dim[0][1]), (self.zoom_dim[1][0] - 20 / self.scale, self.zoom_dim[1][1] - 20 / self.scale)]
                        elif event.key == pygame.K_DOWN:
                            self.zoom_dim = [
                                (self.zoom_dim[0][0], self.zoom_dim[0][1]), (self.zoom_dim[1][0] + 20 / self.scale, self.zoom_dim[1][1] + 20 / self.scale)]
                        elif event.key == pygame.K_LEFT:
                            self.zoom_dim = [
                                (self.zoom_dim[0][0] - 20 / self.scale, self.zoom_dim[0][1] - 20 / self.scale), (self.zoom_dim[1][0], self.zoom_dim[1][1])]
                        elif event.key == pygame.K_RIGHT:
                            self.zoom_dim = [
                                (self.zoom_dim[0][0] + 20 / self.scale, self.zoom_dim[0][1] + 20 / self.scale), (self.zoom_dim[1][0], self.zoom_dim[1][1])]

    def render_person(self, person, p_index):
        delete_person = 0
        # age
        if person[2] > person[3]:
            delete_person = 1
        else:
            person[2] += 1

        # reproduction
        if person[4] > self._settings['p_reproductionThreshold']:
            # person reproduces
            self.people = np.append(self.people, np.asarray(
                [[self.p_id, person[1], 0, person[3], 0, person[5], person[6], person[7]]]), axis=0)
            self.p_id += 1
            person[4] = 0
        else:
            person[4] += 1

        # --------------------
        # disease <-- here -->
        # --------------------

        # get rnd neighbour
        neighbour = self.getRandomNeighbour((person[6], person[7]))

        # check if neighbour is water
        if delete_person == 0 and not np.array_equal(self._pixel_arr[neighbour[0], neighbour[1]], settings.world_pixel['water']):
            # check if neighbour field is empty
            indices = np.where(
                np.all(self.people[:, 6:] == neighbour, axis=1))[0]

            if indices.size != 0:
                if self.people[indices[0]][1] != person[1]:
                    # fight
                    avg_enemie_strength = np.average(
                        np.sum(self.people[indices][:, 3]))
                    # if enemie strength is bigger than person strength
                    if avg_enemie_strength > person[3]:
                        # person dies
                        delete_person = 1
                    else:
                        # enemie dies
                        enemie = self.people[indices[0]]
                        delete_person = -1
                        if len(np.where(np.all(self.people[:, 6:] == neighbour, axis=1))[0]) == 0:
                            person[6] = neighbour[0]
                            person[7] = neighbour[1]
            # if field is empty, move
            person[6] = neighbour[0]
            person[7] = neighbour[1]

        if delete_person == 0:
            self.updatePixel(person[6], person[7], self.colonies[person[1]][2])
            self.people[p_index] = person
        elif delete_person == 1:
            self.people = np.delete(self.people, np.where(
                self.people[:, 0] == person[0])[0][0], axis=0)
        elif delete_person == -1:
            self.people = np.delete(self.people, np.where(
                self.people[:, 0] == enemie[0])[0][0], axis=0)

    def set_pixel_color_back(self, x, y, p_id):
        pass
        # # check if somebody remains on the other field, if not, color it empty
        # old_indices = np.where(np.all(self.people[:, 6:] == [x, y], axis=1))[0]
        # if old_indices.size == 1 and self.people[old_indices[0]][0] == p_id:
        #     # color field empty
        #     self.updatePixel(x, y, settings.world_pixel['empty'])

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
        pos = (-1, -1)
        valid_pos = False
        while not valid_pos:
            pos = positions[np.random.randint(len(positions))]
            # if pos not exceeds the map
            if not (pos[0] <= 0 or pos[0] >= self.w and pos[1] <= 0 or pos[1] >= self.h):
                valid_pos = True
        return pos

    def updateMap(self):
        dim_x = (self.zoom_dim)
        self.display_surface.blit(
            pygame.transform.smoothscale(pygame.surfarray.make_surface(self._pixel_arr[int(self.zoom_dim[0][0]):int(self.zoom_dim[0][1]), int(self.zoom_dim[1][0]):int(self.zoom_dim[1][1])]), (self.h, self.w)), (0, 0))

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
                'Colony ' + str(self.colonies[i][1]) + ': ' + str(len(c_people)), True, (255, 255, 255))
            self.display_surface.blit(
                surface, (x, 20 + y + self.font_size * i))

        pygame.display.update()

    def updatePixel(self, x, y, color):
        # set pixel color
        self._pixel_arr[x, y] = color
