import pygame
import numpy as np
import time
import copy
import sys
import multiprocessing as mp


class setup:
    def __init__(self, _settings):
        self._settings = _settings

        # [gen, day, people]
        self.stats = np.zeros((0, 3)).astype('int')

        # [id, colony_id, age, strength, reproduction_value, disease, x, y, dead]
        self.people = np.zeros((0, 9)).astype('int')

        # [id, name, color]
        self.colonies = np.zeros((0, 3)).astype('int')

        self.c_id = 0
        self.p_id = 0

        # init people and colonies
        for colony in self._settings['colonies']:
            self.colonies = np.append(self.colonies, np.array(
                [[self.c_id, colony[0], colony[1]]]), axis=0)
            for i in range(colony[2]):
                self.people = np.append(self.people, np.array([[self.p_id, self.c_id, 0, np.random.randint(self._settings['p_strength'][0], self._settings['p_strength'][1]), np.random.randint(
                    self._settings['p_reproductionValue'][0], self._settings['p_reproductionValue'][1]), np.random.randint(2), colony[3][0], colony[3][1], False]]), axis=0)
                self.p_id += 1
            self.c_id += 1
        self.p_id += 1

        # get 3d pixel array
        self._pixel_arr = pygame.surfarray.array3d(
            pygame.image.load(self._settings['map_path']))

        # set image dimensions
        self.h = self._pixel_arr.shape[0]
        self.w = self._pixel_arr.shape[1]

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
        pool = mp.Pool(mp.cpu_count())

        # foreach day
        for i in range(self._settings['days_per_generation']):
            results = pool.map(self.render_person, self.people)
            # foreach person
            # for person in self.people:
            #     self.render_person(person)

            # remove dead people
            dead_people_index = np.where(self.people[:, 8])[0]
            if dead_people_index.size != 0:
                self.people = np.delete(self.people, dead_people_index, axis=0)

            # update self.stats
            self.stats = np.append(
                self.stats, [[gen, i, copy.deepcopy(self.people)]], axis=0)

    def render_person(self, person):
        if person[8]:
            return
        delete_person = 0
        # age
        if person[2] > person[3]:
            person[8] = True
            delete_person = 1
        else:
            person[2] += 1

        # reproduction
        if person[4] > self._settings['p_reproductionThreshold']:
            # --------------------
            # mutations <-- here -->
            # --------------------

            # person reproduces
            self.people = np.append(self.people, np.asarray(
                [[self.p_id, person[1], 0, person[3], 0, person[5], person[6], person[7], False]]), axis=0)
            self.p_id += 1
            person[4] = 0
        else:
            person[4] += 1

        # --------------------
        # disease <-- here -->
        # --------------------

        # get rnd neighbour
        neighbour_dir = self.getRandomNeighbour()
        neighbour = (person[6] + neighbour_dir[0],
                     person[7] + neighbour_dir[1])

        # check if neighbour is water
        if delete_person == 0 and not np.array_equal(self._pixel_arr[neighbour[0], neighbour[1]], self._settings['world_pixel']['water']) and neighbour != (-1, -1):
            # check if neighbour field is empty
            indices = np.where(
                np.all(self.people[:, 6:8] == neighbour, axis=1))[0]

            if indices.size != 0:
                if self.people[indices[0]][1] != person[1]:
                    # fight
                    avg_enemie_strength = np.average(
                        np.sum(self.people[indices][:, 3]))
                    # if enemie strength is bigger than person strength
                    if avg_enemie_strength > person[3]:
                        # person dies
                        delete_person = 1
                        person[8] = True
                    else:
                        # enemie dies
                        enemie = self.people[indices[0]]
                        delete_person = -1
                        enemie[8] = True
                        if len(np.where(np.all(self.people[:, 6:8] == neighbour, axis=1))[0]) == 0:
                            person[6] = neighbour[0]
                            person[7] = neighbour[1]
            if delete_person != -1:
                # if field is empty, move
                person[6] = neighbour[0]
                person[7] = neighbour[1]

        if delete_person == 0 or delete_person == 1:
            self.people[np.where(self.people[:, 0] == person[0])[
                0][0]] = person
        elif delete_person == -1:
            self.people[np.where(self.people[:, 0] == enemie[0])[
                0][0]] = enemie

    def getRandomNeighbour(self):
        positions = [
            (0, 1),  # oben
            (1, 0),  # rechts
            (0, -1),  # unten
            (-1, 0),  # link
        ]
        pos = positions[np.random.randint(len(positions))]
        return pos
