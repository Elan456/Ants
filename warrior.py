import pygame
import math as m
from ant import Worker, warrior_images, center_rotate_blit

WARRIOR_DETECTION_RADIUS = 100

# Calculates the distance squared, so the sqrt is never calculated to save time
def dist_sq(p1, p2):
    return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2


def get_closest_ant(origin, ant_list, colony_they_must_not_be):
    closest_distance_sq = float("inf")
    closest_ant = None

    for a in ant_list:
        if a.colony != colony_they_must_not_be:
            distance_sq = dist_sq(origin, a)
            if distance_sq < closest_distance_sq:
                closest_distance_sq = distance_sq
                closest_ant = a
    return closest_ant


class Warrior(Worker):
    def __init__(self, x, y, colony, underground):
        super().__init__(x, y, colony)
        self.underground = underground
        self.state = "following trail"
        self.target = None
        self.steps = 0
        self.tether = []
        self.speed = 1.5

    def update(self, game):
        """
        States:
        Following trail (fight pheromone)
            - Check for nearby enemies
            - If underground check for lack of Space
            - Maintain tether
        pursue
            - Move straight towards selected enemy
            - Keep track of steps since leaving trail
            - If steps get too large return
            - Deal proximity damage and deal it to yourself
            - If hit a wall return
        Returning
            - Follow your tether
            - At end of tether mark yourself as not active
        """

        # print(self.state)
        self.check_being_held()

        if self.state == "following trail":
            self.steps += 1

            strongest = self.get_strongest_pheromones_in_front(game, self.colony.fight_pheromones, half_width=100)
            if strongest is None:
                pass
                # self.state = "returning"
            else:
                self.direction = m.atan2(strongest.y - self.y, strongest.x - self.x)
            # print("move is being called")
            self.move(game.w_width, game.w_height)

            """Checking for nearby enemies to pursue"""
            qBox = [self.x - WARRIOR_DETECTION_RADIUS, self.y - WARRIOR_DETECTION_RADIUS,
                    self.x + WARRIOR_DETECTION_RADIUS, self.y + WARRIOR_DETECTION_RADIUS]
            nearbys = []
            if not self.underground:
                for c in game.colonies:
                    if c != self.colony:
                        nearbys += c.qAnts.intersect(qBox)

            self.target = get_closest_ant(self, nearbys, self.colony)
            if self.target is not None:
                self.state = "pursue"
                self.steps = 0  # To start the step counter, so we do not chase too far

        if self.state == "pursue":

            # else:
            #     ahead = (self.x + m.cos(self.direction) * 5, self.y + m.sin(self.direction) * 5)
            #     if game.tunnel_system.is_open(ahead[0], ahead[1]):
            #         self.move(game.w_width, game.w_height)
            #     else:
            #         self.state = "returning"

            """Dealing proximity damage"""

            distance = m.dist((self.x, self.y), (self.target.x, self.target.y))
            if distance < 15:
                if len(self.tether) > 0:
                    self.tether.pop(-1)  # Do not record these steps
                self.target.health -= 1
                if self.target.held is None:
                    self.target.held = self
                if self.target.health < 0:
                    self.target.active = False
                    self.state = "following trail"
                if isinstance(self.target, Warrior):
                    pass  # It is up to the enemy warrior to hurt you
                else:
                    self.health -= 1
                    if self.health < 0:
                        self.active = False
            else:
                # Too far from target to grab and hurt
                if self.target.held == self:  # If I was the ant holding this ant down
                    self.target.held = None  # Now I am not holding the ant

                # Moving towards them
                self.steps += 1
                self.direction = m.atan2(self.target.y - self.y, self.target.x - self.x)
                if not self.underground:
                    self.move(game.w_width, game.w_height)

        if self.state == "returning":

            if len(self.tether) < 1:
                """Made it back to the nest"""

                # Putting food back into the nest
                ep = sorted(self.colony.entrance_points, key=lambda p: m.dist((p.x, p.y), (self.x, self.y)))[0]
                ep.food += 10
                self.active = False
            else:
                nx, ny = self.tether[-1]
                self.direction = m.atan2(ny - self.y, nx - self.x)
                self.x, self.y = nx, ny
                self.tether.pop(-1)

        else:
            """Tether connects them to the last entrance point they have been near"""
            self.tether.append((self.x, self.y))
            if self.steps > 500:
                # print("Ran out of steps")
                self.state = "returning"

    def draw(self, game):
        """Draws a warrior ant"""
        center_rotate_blit(game.gameDisplay, warrior_images[self.colony.num],
                           (self.x - 5 - game.cam_x, self.y - 10 - game.cam_y),
                           m.degrees(self.direction + m.pi / 2))
        # center_rotate_blit(game.underground_ant_layer, WORKER_IMAGE, (self.x - game.cam_x, self.y - game.cam_y), self.direction)
        # center_rotate_blit(game.ant_layer, WARRIOR_IMAGE, (self.x - game.cam_x, self.y - game.cam_y), self.direction)
