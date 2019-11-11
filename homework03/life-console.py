import curses

from life import GameOfLife
from ui import UI


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.addch(0, 0, '+')
        screen.addch(self.life.rows + 1, self.life.cols + 1, '+')
        screen.addch(0, self.life.cols + 1, '+')
        screen.addch(self.life.rows + 1, 0, '+')

        for y in range(self.life.rows):
            screen.addch(y + 1, 0, '|')
            screen.addch(y + 1, self.life.cols + 1, '|') 

        for x in range(self.life.cols):
            screen.addch(0, x + 1, '-')
            screen.addch(self.life.rows + 1, x + 1, '-')

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for y in range(self.life.rows):
            for x in range(self.life.cols):
                if self.life.curr_generation[y][x] == 0:
                    screen.addch(y + 1, x + 1, ' ')
                else:
                    screen.addch(y + 1, x + 1, '*')

    def run(self) -> None:
        screen = curses.initscr()
        self.draw_borders(screen)
        screen.refresh()
        while self.life.is_max_generations_exceeded and self.life.is_changing:
            self.draw_grid(screen)
            screen.refresh()
            self.life.step()
        curses.endwin()
