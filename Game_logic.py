from collections import defaultdict
import pygame
import random
from collections import deque
import configs as c
from math import log, floor
from Cube import Cube
from pygame.locals import USEREVENT

from collections import namedtuple
CubePos = namedtuple('CubePos' , ['x', 'y'])

class GameLogic:
    def __init__(self, board_size, information_field, timeout, cube_size, colors_count):
        pygame.init()
        self.surface = pygame.display.set_mode((board_size + information_field, board_size))
        self.surface.fill((255, 255, 255))
        pygame.display.set_caption("Cubes")
        self.font = pygame.font.SysFont("LucidaConsole", 15, True)

        self.is_moving = False
        self.cubes_to_delete = defaultdict(lambda: []) # Координата - кубики для удаления по этой координате
        self.timer = pygame.time.set_timer(USEREVENT + 1, timeout)
        self.cube_size = cube_size
        self.board_size = board_size
        self.information_field = information_field
        self.colors = []
        for i in range(colors_count):
            self.colors.append(c.COLORS[i])

        self.points = 0
        self._init_board(board_size, board_size, cube_size)

        self.current_color = (0, 0, 0)
        self.colored_cubes = []


    def _init_board(self, board_width, board_height, cube_size):
        self.board =[]
        for i in range(0, board_width//cube_size):
            self.board.append([])
            for j in range(0, board_height//cube_size):
                self.board[i].append(Cube(i, j, cube_size, self.colors[random.randint(0, len(self.colors) - 1)]))

    def choose_cubes(self, pos):
        if pos[0] < 0 or\
                pos[0] >= self.board_size or\
                pos[1] < 0 or\
                pos[1] >= self.board_size:
            return
        x = pos[0] // self.cube_size
        y = pos[1] // self.cube_size
        if self.board[x][y].state == 0:
            self.current_color = (0, 0, 0)
            if len(self.colored_cubes) > 0:
                for e in self.colored_cubes:
                    e.state = 1
            self.colored_cubes.clear()
            return
        if self.current_color == self.board[x][y].color \
                or (x, y) in self.colored_cubes:
            return
        else:
            self.current_color = self.board[x][y].color
            if len(self.colored_cubes) > 0:
                for e in self.colored_cubes:
                    e.state = 1
                self.colored_cubes.clear()
            self.colored_cubes = self.find_chosen_neighbors(x, y)

    def find_chosen_neighbors(self, x, y):
        result = []
        queue = deque()
        queue.append(CubePos(x, y))
        self.current_color = self.board[x][y].color
        while len(queue) != 0:
            cube = queue.popleft()
            if cube.x < 0 or\
                    cube.x >= len(self.board) or\
                    cube.y < 0 or\
                    cube.y >= len(self.board[0]):
                continue
            if self.board[cube.x][cube.y].color != self.current_color:
                continue
            if self.board[cube.x][cube.y].state == 2 or self.board[cube[0]][cube[1]].state == 0:
                continue
            if self.board[cube.x][cube.y].state != 0:
                self.board[cube.x][cube.y].state = 2
            result.append(self.board[cube.x][cube.y])
            for dx in range(-1, 2, 1):
                for dy in range(-1, 2, 1):
                    if dx != 0 and dy != 0:
                        continue
                    else:
                        queue.append(CubePos(cube.x + dx, cube.y + dy))
        return result

    def delete_cubes(self):
        if len(self.colored_cubes) < 2:
            return
        current_cubes = []
        for e in self.colored_cubes:
            current_cubes.append(CubePos(e.X, e.Y))
        current_cubes = sorted(current_cubes, key=lambda cube: cube.x)
        for e in current_cubes:
            self.cubes_to_delete[e.x].append(e)
        for k, v in self.cubes_to_delete.items():
            self.cubes_to_delete[k] = sorted(v, key=lambda cube: cube.y)

        self.add_points(len(self.colored_cubes))
        for e in self.colored_cubes:
            e.state = 0
        self.colored_cubes.clear()

    def add_points(self, count):
        self.points += self.calculate_points(count)

    @staticmethod
    def calculate_points(count):
        if count > 0:
            return floor(log(count, 2))
        else:
            return 0

    def move_down(self):
        points = self.cubes_to_delete.popitem()
        for e in points[1]:
            self.move_column(e.x, e.y)
            self.board[e[0]][0].state = 0

    def move_column(self, x, y):
        for i in range(y, 0, -1):
            self.board[x][i].state = self.board[x][i - 1].state
            self.board[x][i].color = self.board[x][i - 1].color

    def need_move_left(self):
        for x in range(len(self.board) - 1):
            empty = 0
            full = 0
            for y in range(len(self.board[0])):
                if self.board[x][y].state == 0:
                    empty += 1
                if self.board[x + 1][y].state == 1:
                    full += 1
            if empty == len(self.board[0]) and full > 0:
                return x
        return None

    def move_left(self, x):
        for i in range(x, len(self.board) - 1):
            for j in range(len(self.board[0])):
                self.board[i][j].state = self.board[i + 1][j].state
                self.board[i][j].color = self.board[i + 1][j].color
        for j in range(len(self.board[0])):
            self.board[len(self.board) - 1][j].state = 0

    def find_neighbors(self, x, y, color):
        result = []
        queue = deque()
        queue.append((x, y))
        while len(queue) != 0:
            cube = queue.popleft()
            if cube[0] < 0 or cube[0] >= len(self.board) or cube[1] < 0 or cube[1] >= len(self.board[0]):
                continue
            if self.board[cube[0]][cube[1]].color != color:
                continue
            if self.board[cube[0]][cube[1]].state == 0 or cube in result:
                continue
            result.append(cube)
            for dx in range(-1, 2, 1):
                for dy in range(-1, 2, 1):
                    if (dx != 0 and dy != 0) or cube[0] + dx < 0 or cube[0] + dx >= len(self.board) or\
                        cube[1] + dy < 0 or cube[1] + dy >= len(self.board[0]) or (dx == 0 and dy == 0):
                        continue
                    else:
                        queue.append((cube[0] + dx, cube[1] + dy))

        return result

    def has_steps(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j].state != 0:
                    steps = len(self.find_neighbors(i, j, self.board[i][j].color))
                    if steps >= 2:
                        return True
        return False