#!/usr/bin/env python3

import pygame
from pygame.locals import USEREVENT
from arg_parser import ArgParser
from Records_saver import RecordsSaver
from Game_logic import GameLogic
from Saver import Saver, SavedInfo
import configs as c


class Game(GameLogic):
    def __init__(self, board_size, information_field, ticks,
                 cube_size, colors_count, records_saver, user_name):
        GameLogic.__init__(self, board_size, information_field, ticks,
                           cube_size, colors_count)
        self.game_over = False
        self.first = True
        self.records_saver = records_saver
        self.user_name = user_name

    def handler_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game_over = True
            elif event.type == pygame.QUIT:
                self.game_over = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                info = Saver.load(self.user_name)
                if info is not None:
                    self.board = info.board
                    self.points = info.points
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                info = SavedInfo(self.board, self.points)
                Saver.save(info, self.user_name)
            elif event.type == pygame.MOUSEMOTION \
                    and len(self.cubes_to_delete) == 0 \
                    and not self.is_moving:
                if self.first:
                    self.choose_cubes((0, 0))
                    self.first = False
                else:
                    self.choose_cubes(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN \
                    and len(self.cubes_to_delete) == 0 \
                    and not self.is_moving:
                self.delete_cubes()
            elif event.type == USEREVENT + 1:
                self.update()

    def update(self):
        if len(self.cubes_to_delete) > 0:
            self.move_down()
            self.update_colors()
            return
        if self.has_steps():
            x = self.need_move_left()
            if x is not None:
                self.is_moving = True
                self.move_left(x)
            else:
                self.is_moving = False
            self.update_colors()
        else:
            self.records_saver.add_records(self.points, self.user_name)
            self.game_over = True

    def update_colors(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                self.board[i][j].update_chosen_color()

    def _draw_points(self):
        self.points_text = self.font.render("Points: %s" % self.points, True, (10, 127, 143))
        self.surface.blit(self.points_text, (self.board_size + 10, 10))

    def _draw_next_points(self):
        self.next_points = self.calculate_points(len(self.colored_cubes))
        self.next_points_text = self.font.render("Next points: %s" % self.next_points, True, (10, 127, 143))
        self.surface.blit(self.next_points_text, (self.board_size + 10, 30))

    def draw(self):
        for line in self.board:
            for i in line:
                i.draw(self.surface)
        self._draw_points()
        self._draw_next_points()

    def run(self):
        pygame.mouse.set_pos(0, 0)
        while not self.game_over:
            self.surface.fill((255, 255, 255))
            self.handler_events()
            self.draw()
            pygame.display.update()


def main():
    parser = ArgParser()
    board_size, colors_count, show_records, name = parser.parse_arguments()
    records_saver = RecordsSaver("records.txt")
    if show_records:
        records_saver.get_records()
        return
    g = Game(board_size, c.INFORMATION_FIELD, c.TIMEOUT, c.CELL_SIZE,
             colors_count, records_saver, name)
    g.run()


if __name__ == '__main__':
    main()
