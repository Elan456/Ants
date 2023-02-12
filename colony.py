import pygame
from pyqtree import Index
from warrior import Warrior
from forager import Forager
from tunneler import Tunneler
from nest import EntrancePoint


class Colony:
    def __init__(self, game, num, entrance_point_loc, num_foragers, num_tunnelers):
        self.num_tunnelers = num_tunnelers
        self.num_foragers = num_foragers
        self.entrance_point_loc = entrance_point_loc
        self.num = num

        self.above_ants = []
        for _ in range(num_foragers):
            self.above_ants.append(Forager(entrance_point_loc[0], entrance_point_loc[1], self))

        self.under_ants = []
        for _ in range(num_tunnelers):
            self.under_ants.append(Tunneler(entrance_point_loc[0], entrance_point_loc[1], self))

        self.entrance_points = [EntrancePoint(game, self, x=entrance_point_loc[0], y=entrance_point_loc[1])]

        self.qAnts = Index(bbox=[0, 0, game.w_width, game.w_height])

        self.ants_lost = 0

    def new_entrance_point(self, game, x, y):
        self.entrance_points.append(EntrancePoint(game, self, x, y))
        self.under_ants.append(Tunneler(x, y, self))

    def update(self, game):

        # Updating the above ground ants
        self.qAnts = Index(bbox=[0, 0, game.w_width, game.w_height], max_depth=5)
        old_ants = self.above_ants.copy()
        for a in old_ants:
            a.update(game)
            game.num_ants[self.num] += 1
            self.qAnts.insert(a, bbox=[a.x - .5, a.y - .5, a.x + .5, a.y + .5])
            if not game.underground:
                a.draw(game)

            if not a.active:
                self.above_ants.remove(a)
                if not isinstance(a, Warrior):
                    game.ants_killed[self.num] += 1

        # Updating the below ground ants
        old_ants = self.under_ants.copy()
        for a in old_ants:
            a.update(game)
            game.num_ants[self.num] += 1
            if game.underground:
                a.draw(game)

    def draw_entrance_points(self, game):
        for ep in self.entrance_points:
            ep.draw(game)

