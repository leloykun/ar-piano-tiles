import random
import time

class Game:
    def __init__(self, num_tiles=4, num_layers=4, single_colored=True, double_prob=0.20):
        self.num_tiles = num_tiles
        self.num_layers = num_layers
        self.single_colored = single_colored
        self.double_prob = double_prob
        self.build_tiles()
        self.start_time = None
        self.score = 0

    def build_tiles(self):
        self.tiles = [self.gen_random_line() for _ in range(self.num_layers)]
        for i in range(self.num_layers):
            random.shuffle(self.tiles[i])

    def restart(self):
        # self.build_tiles()
        self.start_time = time.time()
        self.score = 0

    def print_tiles(self):
        print("\n".join("".join(map(str, line)) for line in self.tiles))

    def gen_random_line(self):
        line = []
        if self.single_colored or (not self.single_colored and random.random() > self.double_prob):
            line = [1] + [0 for _ in range(self.num_tiles-1)]
        else:
            line = [1, 1] + [0 for _ in range(self.num_tiles-2)]
        random.shuffle(line)
        return line

    def next(self):
        for i in range(self.num_layers-1,0,-1):
            self.tiles[i] = self.tiles[i-1]
        self.tiles[0] = self.gen_random_line()
        self.score += 1

    def ongoing(self, time_limit=30.0):
        if self.start_time is None:
            return False
        return time.time() <= self.start_time + time_limit
