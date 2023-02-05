import pygame
import math as m
from ant import Worker, WARRIOR_IMAGE, center_rotate_blit

WARRIOR_DETECTION_RADIUS = 100


def get_closest_ant(origin, ant_list, colony_they_must_not_be):
    closest_distance = float("inf")
    closest_ant = None

    for a in ant_list:
        if a.colony != colony_they_must_not_be:
            distance = m.dist((origin.x, origin.y), (a.x, a.y))
            if distance < closest_distance:
                closest_distance = distance
                closest_ant = a
    return closest_ant


class Warrior(Worker):
    def __init__(self, x, y, colony, underground):
        super().__init__(x, y, colony)
        self.underground = underground
        self.state = "follow trail"
        self.target = None
        self.steps = 0

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

        if self.state == "following trail":
            strongest = self.get_strongest_pheromones_in_front(game, game.fight_pheromones, half_width=100)
            if strongest is None:
                self.state = "returning"
            else:
                self.direction = m.atan2(strongest.y - self.y, strongest.x - self.x)
            self.move(game.w_width, game.w_height)

            """Checking for nearby enemies to pursue"""
            if self.underground:
                qt = game.uqAnts
            else:
                qt = game.qAnts

            nearbys = qt.instersect(bbox=[self.x - WARRIOR_DETECTION_RADIUS, self.y - WARRIOR_DETECTION_RADIUS,
                                          self.x + WARRIOR_DETECTION_RADIUS, self.y + WARRIOR_DETECTION_RADIUS])

            self.target = get_closest_ant(self, nearbys, self.colony)
            if self.target is not None:
                self.state = "pursue"
                self.steps = 0  # To start the step counter, so we do not chase too far

        if self.state == "pursue":
            self.steps += 1
            self.direction = m.atan2(self.target.y - self.y, self.target.x - self.x)
            if not self.underground:
                self.move(game.w_width, game.w_height)
            else:
                ahead = (self.x + m.cos(self.direction) * 5, self.y + m.sin(self.direction) * 5)
                if game.tunnel_system.is_open(ahead[0], ahead[1]):
                    self.move(game.w_width, game.w_height)
                else:
                    self.state = "returning"

            """Dealing proximity damage"""

            distance = m.dist((self.x, self.y), (self.target.x, self.target.y))
            if distance < 50:
                self.target.health -= 1
                if isinstance(self.target, Warrior):
                    pass  # It is up to the enemy warrior to hurt you
                    self.target.health -= 1
                else:
                    self.health -= .5

        if self.state == "returning":
            pygame.draw.circle(game.debug_layer, (0, 255, 0), (self.x - game.cam_x, self.y - game.cam_y), 2)

            if len(self.tether) < 1:
                """Made it back to the nest"""
                # self.state = "tunneling"
                self.energy = 100
                self.distance_stepped = 0
                self.tether = []
                self.state = "tunneling"
                self.holding_dirt = False
            else:
                nx, ny = self.tether[-1]
                self.direction = m.atan2(ny - self.y, nx - self.x)
                self.x, self.y = nx, ny
                self.tether.pop(-1)

        else:
            """Tether connects them to the last entrance point they have been near"""
            self.tether.append((self.x, self.y))
            self.distance_stepped += 1
            if self.distance_stepped > self.energy * 10 + 10:
                # Start returning
                self.state = "returning"

    def draw(self, game):
        """Draws a warrior ant"""
        pygame.draw.circle(game.underground_ant_layer, (0, 255, 255), (self.x - game.cam_x, self.y - game.cam_y), 3)
        pygame.draw.line(game.underground_ant_layer, (0, 255, 0), (self.x - game.cam_x, self.y - game.cam_y),
                         (self.x + m.cos(self.direction) * 10 - game.cam_x,
                          self.y + m.sin(self.direction) * 10 - game.cam_y))
        # center_rotate_blit(game.underground_ant_layer, WORKER_IMAGE, (self.x - game.cam_x, self.y - game.cam_y), self.direction)
        # center_rotate_blit(game.ant_layer, WARRIOR_IMAGE, (self.x - game.cam_x, self.y - game.cam_y), self.direction)
