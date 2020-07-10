import os
import random
import yaml
import json

import numpy as np
# import cv2
from collections import defaultdict
import matplotlib.pyplot as plt

from data.Map import Graph, parse_json
from data.Human import Human, HealthState


ORIGINAL_COUNT = 50
BROAD_RATE = 0.8
SHADOW_TIME = 14
u = 0.99

CURRENT_FOLDER = os.path.join(os.path.abspath('.'), "data")


def dist(a, b):
    return np.linalg.norm(a - b)


class DataGenerator:
    def __init__(self, map: Graph, total_cnt=5000, original_cnt=50, broad_rate=0.8, shadow_time=7, move_value=0.99, move_dis=5, move_std=1, safe_dist=5, cure_time=10, freeze_rate=0.8):
        self.people = self._init_people(map, total_cnt, original_cnt, move_value, move_dis, move_std)
        # self.infected, self.shadow, self.confirmed, self.freeze = {}
        self.map = map
        self.infectedMap = self._get_infectedMap()
        self.broad_rate = broad_rate
        self.shadow_time = shadow_time
        self.safe_dist = safe_dist
        self.freeze_rate = freeze_rate
        self.move_value = move_value
        self.move_dis, self.move_std = move_dis, move_std
        self.tick = 0
        self.cure_time = cure_time

    def _init_people(self, map, total_cnt, original_cnt, move_value, move_dis, move_std):
        people = [Human(_, map, move_value, move_dis, move_std) for _ in range(total_cnt)]
        infected = random.sample(people, original_cnt)
        for h in infected:
            h.change_state(HealthState.SHADOW)
        print("{} get infected at tick 0".format(','.join([str(h.id) for h in infected])))
        self.infected = {p.id for p in infected}
        self.normal = {i for i in range(total_cnt)}.difference(self.infected)
        self.freeze, self.shadow, self.confirmed = set(), self.infected.copy(), set()
        return people

    def _get_infectedMap(self):
        infectedMap = {k: set() for k in self.map.getVertices()}
        for p in self.people:
            find = self.map.findVertex(p.getPos())
            p.pos_id = find
            if find == -1:
                continue
            infectedMap[find].add(p.getId())
            if p.state == HealthState.CONFIRMED:
                print(p)
        return infectedMap

    def cal_infection_index(self, pos):
        if not pos in self.infectedMap:
            return -1

        population = len(self.infectedMap[pos])
        population_index = min(1, (population / 100) ** 3)

        confirmed = 0
        for p in self.infectedMap[pos]:
            if self.people[p].state == HealthState.CONFIRMED:
                confirmed += 1
        confirmed_index = min(1, confirmed ** 3)

        infection_index = confirmed_index * 0.6 + population_index * 0.4
        return infection_index

    def _is_in_infection_area(self, p):
        for i in self.infected:
            if p.getDis(self.people[i]) < self.safe_dist:
                return True
        return False

    def _update(self, shadow_rm, confimed_rm, freeze_rm, normal_rm, shadow_a, confimed_a, freeze_a, normal_a):
        self.shadow = self.shadow.union(shadow_a).difference(shadow_rm)
        self.confirmed = self.confirmed.union(confimed_a).difference(confimed_rm)
        self.freeze = self.freeze.union(freeze_a).difference(freeze_rm)
        self.normal = self.normal.union(normal_a).difference(normal_rm)

    def act(self, verbose=False):
        for p in self.people:
            p(self.tick)

        shadow_rm, confimed_rm, freeze_rm, normal_rm = set(), set(), set(), set()
        shadow_a, confimed_a, freeze_a, normal_a = set(), set(), set(), set()

        for p in self.shadow:
            if self.tick - self.people[p].infectedTime >= self.shadow_time:
                self.people[p].change_state(HealthState.CONFIRMED, self.tick)
                shadow_rm.add(p)
                confimed_a.add(p)
                if verbose:
                    print(f"Tick {self.tick}\t{p} is confirmed")

        for p in self.confirmed:
            if self.tick - self.people[p].confirmedTime >= 3:
                if random.uniform(0, 1) <= self.freeze_rate:
                    self.people[p].change_state(HealthState.FREEZE, self.tick)
                    pos = np.array(self.map.randomCamp())
                    self.people[p].quarantine(pos, self.tick)
                    freeze_a.add(p)
                    confimed_rm.add(p)
                    if verbose:
                        print(f"Tick {self.tick}\t{p} get isolated")

        for p in self.freeze:
            if self.tick - self.people[p].freezeTime >= self.cure_time:
                self.people[p].change_state(HealthState.NORMAL, self.tick)
                freeze_rm.add(p)
                normal_a.add(p)
                if verbose:
                    print(f"Tick {self.tick}\t{p} get cured")

        for p in self.normal:
            if random.random() > self.broad_rate:
                continue
            if self._is_in_infection_area(self.people[p]):
                self.people[p].change_state(HealthState.SHADOW, self.tick)
                shadow_a.add(p)
                normal_rm.add(p)
                if verbose:
                    print(f"Tick {self.tick}\t{p} get infected")

        self._update(shadow_rm, confimed_rm, freeze_rm, normal_rm, shadow_a, confimed_a, freeze_a, normal_a)
        self.infected = self.shadow.union(self.confirmed)

        self.tick += 1
        add = {"CONFIRMED": confimed_a, "NORMAL": normal_a, "FREEZE": freeze_a}
        return add

    def draw(self):
        ax = self.map.draw()
        def draw_people(lst, marker, c, size=1):
            x, y = [self.people[p].pos[0] for p in lst], [self.people[p].pos[1] for p in lst]
            ax.scatter(x, y, s=[size] * len(lst), marker=marker, c=c)

        draw_people(self.normal, 'o', 'k')
        draw_people(self.confirmed, 'o', 'r', 5)
        draw_people(self.shadow, 'o', 'y')
        draw_people(self.freeze, 'o', 'b')
        return ax

    def stats(self):
        state_cnt = defaultdict(int)
        population_cnt = defaultdict(int)
        for p in self.people:
            state_cnt[p.state.value] += 1
            population_cnt[p.pos_id] += 1
        return state_cnt, population_cnt


def init_generator(config_name):
    with open(os.path.join(CURRENT_FOLDER, "configs", f"{config_name}.yaml")) as f:
        config = yaml.load(f)

    # with open(os.path.join(CURRENT_FOLDER, "maps", config["MAP_FILE"] + ".json")) as f:
    #     example = json.load(f)
    places, connections = parse_json(os.path.join(CURRENT_FOLDER, "maps", config["MAP_FILE"] + ".csv"))
    map = Graph(places, connections)

    gen = DataGenerator(map, **config["PARAMS"])
    return gen


if __name__ == "__main__":
    # import json
    #
    # with open("map.json") as f:
    #     example = json.load(f)
    #
    # map = Graph(example["places"], example["connections"])
    # generator = DataGenerator(map, 500, 5)
    # for k in generator.infectedMap:
    #     print(generator.cal_infection_index(k))

    generator = init_generator("pku")

    for i in range(1000):
        generator.act()
        plt.close()
        ax = generator.draw()
        plt.show()
        plt.pause(0.03)


    # img = map.draw()
    # for p in generator.people:
    #     pos = p.getPos()
    #     pos = (int(pos[0]), int(pos[1]))
    #     if p.state == HealthState.CONFIRMED:
    #         cv2.circle(img, pos, 3, (0, 0, 255))
    #     else:
    #         cv2.circle(img, pos, 1, (0, 0, 0))
    #
    #
    #
    # cv2.imshow('1', img)
    # cv2.waitKey(0)
    print(generator.people[0].traces)

    cs, cp = generator.stats()
    print(cs)
    print(cp)
