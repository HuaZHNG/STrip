import os

import numpy as np

from data.Generator import init_generator
from run.Human import Human, HealthState


UPDATE_INT = 1


class Queue:
    def __init__(self, maxlen=7):
        self.lst = [-1 for _ in range(maxlen)]
        self.pos = 0
        self.maxlen = maxlen

    def add(self, value):
        self.lst[self.pos] = value
        self.pos = (self.pos + 1) % self.maxlen

    def getAll(self):
        out = []
        s = (self.pos + self.maxlen - 1) % self.maxlen
        e = self.pos
        while s != e:
            out.append(self.lst[s])
            s = (s + self.maxlen - 1) % self.maxlen
        out.append(self.lst[s])
        return out


class Monitor:
    def __init__(self, map, people=None):
        self.map = map
        self.people = {}
        self.nodes = map.getVertices()
        self.pos = map.getPos()
        self.infection_index = {k: 0 for k in self.nodes}
        self.infection_history = Queue(7)
        self.tick = 0
        self.confirmed = set()
        if not people is None:
            self._init_people(people)
        else:
            self._init_people([])

    def _init_people(self, lst):
        people = {}
        distribution = {k: set() for k in self.nodes}
        distribution[-1] = set()

        for id, pos in lst:
            people[id] = Human(id, pos)
            distribution[pos].add(id)

        self.people = people
        self.distribution = distribution

    def addPeople(self, id=None, pos=None):
        if id is None:
            id = len(self.people)

        if pos is None:
            pos = -1

        self.people[id] = Human(id, pos)
        self.distribution[pos].add(id)

    def cal_infection_index(self, pos):
        if not pos in self.nodes:
            return -1

        population = len(self.distribution[pos])
        population_index = min(1, (population / 10) ** 3)

        confirmed = 0
        for id in self.distribution[pos]:
            if self.people[id].isConfirmed():
                confirmed += 1
        confirmed_index = min(1, confirmed ** 3)

        new_infection_index = (confirmed_index * 0.6 + population_index * 0.4) * 10
        infection_index = self.infection_index[pos] * 0.01 + new_infection_index * 0.99
        self.infection_index[pos] = infection_index
        return infection_index

    def _index2str(self, infection_index):
        lst = []
        for k, v in infection_index.items():
            lst.append({
                "lat": self.pos[k][1],
                "lng": self.pos[k][0],
                "weight": '%.2f' % v
            })
        return str(lst)

    def updateTick(self):
        self.tick += 1
        print("tick: ", self.tick)
        if self.tick % UPDATE_INT == 0:
            for node in self.nodes:
                self.cal_infection_index(node)
            self.infection_history.add(self._index2str(self.infection_index))

    def getInfectionMap(self):
        return self.infection_index, self.map

    def getInfectionList(self):
        lst = [s for s in self.infection_history.getAll() if s != -1]
        text = '[' + ',\n'.join(lst) + ']'
        return text.replace('\'', '\"')

    def updatePeoplePos(self, id, new_pos, verbose=False):
        if not id in self.people:
            return -1

        old_pos = self.people[id].getPos()
        if new_pos == old_pos:
            return

        if verbose:
            print(f"{id}\tPos: {old_pos} => {new_pos}")
        self.people[id].move(new_pos, self.tick)
        self.distribution[old_pos].remove(id)
        self.distribution[new_pos].add(id)

    def updatePeopleState(self, id, new_state, verbose=False):
        if not id in self.people:
            return -1

        if isinstance(new_state, str):
            new_state = getattr(HealthState, new_state)

        if verbose:
            print(id, self.people[id].state, new_state)

        self.people[id].changeState(new_state, self.tick)
        if new_state == HealthState.CONFIRMED:
            self.confirmed.add(id)
        elif new_state != HealthState.FREEZE:
            self.confirmed.remove(id)

    def findContacts(self, id):
        if not id in self.people:
            return -1

        out = {}

        p = self.people[id]
        healthy = set(self.people.keys()).difference(self.confirmed)
        for pos, periods in p.getHistory().items():
            for h in healthy:
                timeline = self.people[h].getPeriod(pos)
                if timeline is None:
                    continue
                inter, time = intersection(periods, timeline)
                if inter > 0:
                    out[h] = pos, time

        return out



def intersection(lst_a, lst_b):
    maxInter = 0
    time = ()

    pt_a, pt_b = 0, 0
    while pt_a < len(lst_a) and pt_b < len(lst_b):
        if lst_a[pt_a][1] <= lst_b[pt_b][0]:
            pt_a += 1
        elif lst_b[pt_b][1] <= lst_a[pt_a][0]:
            pt_b += 1
        else:
            s = max(lst_a[pt_a][0], lst_b[pt_b][0])
            e = min(lst_a[pt_a][1], lst_b[pt_b][1])
            inter = e - s

            if inter > maxInter:
                maxInter = inter
                time = s, e

            if lst_a[pt_a][1] > lst_b[pt_b][1]:
                pt_b += 1
            else:
                pt_a += 1

    return maxInter, time




if __name__ == "__main__":
    q = Queue(4)
    q.add(1)
    q.add(2)
    print(q.getAll())
    q.add(3)
    print(q.getAll())
    q.add(0)
    print(q.getAll())
    q.add(4)
    print(q.getAll())