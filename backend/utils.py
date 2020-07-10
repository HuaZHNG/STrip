import numpy as np


class Position:
    def __init__(self, id, pos):
        self.id = id
        self.pos = pos
        self.have = set()

    def remove(self, human):
        self.have.remove(human.human_id)

    def add(self, human):
        self.have.add(human.human_id)


class Building(Position):
    def __init__(self, id, pos):
        super(Building, self).__init__(id, pos)


class Road(Position):
    def __init__(self, id, pos):
        super(Road, self).__init__(id, pos)



class Map:
    def __init__(self, build_lst):
        pass

    def get(self, timestep):
        pass


class Human:
    def __init__(self, human_id, state, pos: Position):
        self.human_id = human_id
        self.state = state
        self.traces = []
        self.current_pos = pos

    def change_state(self, new_state):
        self.state = new_state

    def move(self, to, timestep):
        self.current_pos.remove(self)
        to.add(self)
        self.current_pos = to
        self.traces.append([timestep, to])