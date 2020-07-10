import os
import random

import numpy as np
# import cv2
from enum import Enum


class HealthState(Enum):
    NORMAL = 0
    CONFIRMED = 3
    FREEZE = 4
    CURED = 5


def dist(a, b):
    return np.linalg.norm(a - b)


class Human:
    def __init__(self, id, pos, tick=0):
        self.id = id
        self.pos = pos
        self.state = HealthState.NORMAL
        self.confirmedTime, self.freezeTime = None, None
        self.traces = [[tick, pos]]
        self.periods = {}

    def changeState(self, new_state, time=0):
        self.state = new_state
        if new_state == HealthState.CONFIRMED:
            self.confirmedTime = time
        elif new_state == HealthState.FREEZE:
            self.freezeTime = time

    def getId(self):
        return self.id

    def getPos(self):
        return self.pos

    def getDis(self, p):
        return dist(self.pos, p.pos)

    def getTraces(self):
        return self.traces

    def getHistory(self):
        return self.periods

    def getPeriod(self, pos):
        if pos not in self.periods:
            return None
        return self.periods[pos]

    def isHealthy(self):
        return self.state == HealthState.NORMAL

    def isConfirmed(self):
        return self.state == HealthState.CONFIRMED

    def move(self, new_pos, time=0):
        if self.pos in self.periods:
            self.periods[self.pos].append([self.traces[-1][0], time])
        else:
            self.periods[self.pos] = [[self.traces[-1][0], time]]

        self.pos = new_pos
        self.traces.append([time, new_pos])

    def __str__(self):
        return f"State: {self.state}\tPos: {self.pos}\tConfirmed time: {self.confirmedTime}"


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
