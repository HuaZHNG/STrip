import os
import random

import numpy as np
# import cv2
from enum import Enum


class HealthState(Enum):
    NORMAL = 0
    SUSPECTED = 1
    SHADOW = 2
    CONFIRMED = 3
    FREEZE = 4
    CURED = 5


def dist(a, b):
    return np.linalg.norm(a - b)


class Human:

    def __init__(self, id, map, move_value=0.99, move_dis=5, move_std=1):
        self.id = id
        self.map = map
        self.pos = self.target = np.array(map.randomPosition())
        self.pos_id = map.findVertex(self.pos)
        self.move_value = move_value
        self.move_dis, self.move_std = move_dis, move_std
        self.state = HealthState.NORMAL
        self.infectedTime, self.confirmedTime = None, None
        self.freezeTime = None
        self.traces = []

    def change_state(self, new_state, time=0):
        self.state = new_state
        if new_state == HealthState.SHADOW:
            self.infectedTime = time
        elif new_state == HealthState.CONFIRMED:
            self.confirmedTime = time
        elif new_state == HealthState.FREEZE:
            self.freezeTime = time
        elif new_state == HealthState.CURED:
            self.target = self.map.randomPosition()

    def _wantToMove(self):
        value = self.move_value + random.gauss(0, 1/3)
        return value > 0

    def _new_target(self):
        dist = random.gauss(self.move_dis, self.move_std)
        theta = random.uniform(-np.pi, np.pi)
        targetX = self.pos[0] + dist * np.cos(theta)
        targetY = self.pos[1] + dist * np.sin(theta)
        targetX, targetY = self.map.validate([targetX, targetY])
        return np.array([targetX, targetY])

    def quarantine(self, pos, tick):
        self.pos = self.target = pos
        self.traces.append([tick, self.pos, -2])

    def __call__(self, tick):
        if self.state == HealthState.FREEZE:
            return

        if dist(self.pos, self.target) > self.move_std:              # not arrive
            self.pos[0] += (self.target[0] - self.pos[0]) / np.abs(self.target[0] - self.pos[0]) * self.move_std
            self.pos[1] += (self.target[1] - self.pos[1]) / np.abs(self.target[1] - self.pos[1]) * self.move_std
        else:                                             # arrive
            self.pos_id = self.map.findVertex(self.pos)
            self.traces.append([tick, self.pos, self.pos_id])          # save history

            if not self._wantToMove():                    # next move
                return

            self.target = self._new_target()
            # print(self.pos, self.target)

    def draw(self, ax):
        pos = int(self.pos[0]), int(self.pos[1])
        if self.state == HealthState.SHADOW:
            r = 2
            c = (0, 255, 255)
        elif self.state == HealthState.CONFIRMED:
            r = 4
            c = (0, 0, 255)
        elif self.state == HealthState.FREEZE:
            r = 3
            c = (255, 0, 0)
        else:
            r = 1
            c = (0, 0, 0)
        ax.scatter([pos[0]], [pos[1]], marker='o')
        return ax

    def getId(self):
        return self.id

    def getPos(self):
        return self.pos

    def getDis(self, p):
        return dist(self.pos, p.pos)

    def __str__(self):
        return f"State: {self.state}\tPos: {self.pos_id}-{self.pos}\tConfirmed time: {self.confirmedTime}"


if __name__ == "__main__":
    import json
    from data.Map import Graph

    with open("map.json") as f:
        example = json.load(f)
    map = Graph(example["places"], example["connections"])

    img = map.canvas.copy()
    human = Human(0, map)
    for i in range(10):
        im = human.draw(img)
        # cv2.imshow("1", im)
        # cv2.waitKey()
        human(i)
        print(human.pos, human.target)

    print(human.traces)
