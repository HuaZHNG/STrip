import random

import numpy as np
# import cv2
import pandas as pd
import matplotlib.pyplot as plt



class Vertex:
    INF = 1e30

    def __init__(self, id, bbox):
        '''

        :param id:
        :param bbox: [x, y, w, h]
        '''
        self.id = id
        self.bbox = bbox
        self.center = [bbox[0] + bbox[2] / 2, bbox[1] + bbox[3] / 2]
        self.connectedTo = {}
        self.index = 0

    def addNeighbor(self, nbr, dis=0):
        self.connectedTo[nbr] = dis

    def getNeighbors(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getDistance(self, nbr):
        if nbr in self.connectedTo:
            return self.connectedTo[nbr]
        else:
            return Vertex.INF

    def getIndex(self):
        return self.index

    def setIndex(self, index):
        self.index = index

    def contains(self, pos):
        return self.bbox[0] <= pos[0] <= self.bbox[0] + self.bbox[2] and self.bbox[1] <= pos[1] <= self.bbox[1] + self.bbox[3]

    def __str__(self):
        return '\t'.join([f'{k}: {v}' for k, v in self.connectedTo.items()])


class Graph:
    def __init__(self, places, connections, bbox=None):
        '''

        :param places: dict -- key: place id; value: bbox
        :param connections: list -- item: [src, dst, dist]
        '''
        self.vertList = self._init_graph(places, connections)
        self.vertKeys = list(self.vertList.keys())
        self.bbox = bbox if bbox is not None else self._init_bbox()
        self.camp = Vertex(-2, [116.305, 39.99, 0.0005, 0.0005])
        self.ax = self._init_canvas()
        self.canvas = self.draw()

    def _init_graph(self, places, connections):
        vertList = {int(k): Vertex(int(k), v) for k, v in places.items()}
        for src, dst, dist in connections:
            vertList[src].addNeighbor(dst, dist)
            vertList[dst].addNeighbor(src, dist)
        return vertList

    def _init_bbox(self):
        bbox_lst, center_lst = [], []
        index2id = {}
        for k, vert in self.vertList.items():
            bbox_lst.append(vert.bbox)
            center_lst.append(vert.center)
            index2id[len(index2id)] = k

        bbox_lst = np.array(bbox_lst)
        self.bbox_lst = bbox_lst
        self.center_lst = np.array(center_lst)
        self.index2id = index2id
        x, y = np.min(bbox_lst[:, 0]), np.min(bbox_lst[:, 1])
        w, h = np.max(bbox_lst[:, 0] + bbox_lst[:, 2]) - x, np.max(bbox_lst[:, 1] + bbox_lst[:, 3]) - y
        return [x, y, w, h]

    def __len__(self):
        return len(self.vertList)

    def setIndex(self, indexDict):
        for k, v in indexDict.items():
            self.vertList[k].setIndex(v)

    def contains(self, src):
        return src in self.vertList

    def findVertex(self, pos):
        for vert in self.vertList.values():
            if vert.contains(pos):
                return vert.getId()
        return -1

    def getVertices(self):
        return self.vertList.keys()

    def randomVertex(self):
        return random.choice(list(self.vertKeys))

    def randomPosition(self):
        while True:
            x = random.uniform(self.bbox[0], self.bbox[0] + self.bbox[2])
            y = random.uniform(self.bbox[1], self.bbox[1] + self.bbox[3])
            if self.findVertex([x, y]) >= 0:
                break
        return x, y

    def randomCamp(self):
        bbox = self.camp.bbox
        x = random.uniform(bbox[0], bbox[0] + bbox[2])
        y = random.uniform(bbox[1], bbox[1] + bbox[3])
        return x, y

    def getDistance(self, src, dst):
        if not (self.contains(src) and self.contains(dst)):
            return -1

        return self.vertList[src].getDistance(dst)

    def getPos(self):
        pos = {k: self.vertList[k].bbox[:2] for k in self.vertList}
        return pos

    def validate(self, pos):
        pos[0] = min(max(self.bbox[0], pos[0]), self.bbox[0] + self.bbox[2])
        pos[1] = min(max(self.bbox[1], pos[1]), self.bbox[1] + self.bbox[3])
        return pos

    def _init_canvas(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_xlabel('lng')
        ax.set_ylabel('lat')
        return ax

    def draw(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_xlabel('lng')
        ax.set_ylabel('lat')
        bbox_lst = self.bbox_lst
        ax.scatter([bbox[0] for bbox in bbox_lst], [bbox[1] for bbox in bbox_lst], s=[500] * len(bbox_lst), marker='H')
        ax.scatter([self.camp.bbox[0]], [self.camp.bbox[1]], s=[500], marker='s')

        # x, y = [], []
        # for i, bbox in enumerate(bbox_lst):
        #     idx = self.index2id[i]
        #     for nbr in self.vertList[idx].getNeighbors():
        #         x.append([bbox_lst[idx][0], bbox_lst[nbr][0]])
        #         y.append([bbox_lst[idx][1], bbox_lst[nbr][1]])
        # ax.plot(x, y, 'k--')
        return ax


def parse_json(path):
    df = pd.read_csv(path)
    places = {}
    connections = []
    for i, row in df.iterrows():
        pos = [getattr(row, " lng"), getattr(row, " lat"), 1e-4, 1e-4]
        places[i] = pos
        edges = getattr(row, " edge")
        conns = getattr(row, "distance")
        # print(edges)
        # if isinstance(edges, str):
        #     continue
        for to, dis in zip(eval(edges), eval(conns)):
            connections.append([i, to, dis])
    return places, connections



if __name__ == "__main__":
    import json
    # with open("map.json") as f:
    #     example = json.load(f)

    map = Graph(*parse_json("maps/data.csv"))
    # map = Graph(example["places"], example["connections"])
    print(map.vertList[0])
    print([_ for _ in map.vertList])
    print(len(map))
    print(map.getDistance(0, 5))
    print(map.getDistance(0, 1))
    print(map.getDistance(0, 6))
    print(map.randomVertex())
    print(map.bbox)
    map.draw()
    # parse_json("maps/data.csv")