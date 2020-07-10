import random

import numpy as np
# import cv2



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

    def getPos(self):
        pos = {k: self.vertList[k].bbox[:2] for k in self.vertList}
        return pos

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
        bbox = self.vertList[-2].bbox
        x = random.uniform(bbox[0], bbox[0] + bbox[2])
        y = random.uniform(bbox[1], bbox[1] + bbox[3])
        return x, y

    def getDistance(self, src, dst):
        if not (self.contains(src) and self.contains(dst)):
            return -1

        return self.vertList[src].getDistance(dst)

    def validate(self, pos):
        pos[0] = min(max(self.bbox[0], pos[0]), self.bbox[0] + self.bbox[2])
        pos[1] = min(max(self.bbox[1], pos[1]), self.bbox[1] + self.bbox[3])
        return pos


if __name__ == "__main__":
    import json
    with open("map.json") as f:
        example = json.load(f)

    map = Graph(example["places"], example["connections"])
    print(map.vertList[0])
    print([_ for _ in map.vertList])
    print(len(map))
    print(map.getDistance(0, 5))
    print(map.getDistance(0, 1))
    print(map.getDistance(0, 6))
    print(map.randomVertex())
    print(map.bbox)
    map.draw()