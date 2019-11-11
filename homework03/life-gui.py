import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int=10, speed: int=10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.width = self.cell_size * self.life.cols
        self.height = self.cell_size * self.life.rows
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for j in range(self.life.rows):
            for i in range(self.life.cols):
                if self.life.curr_generation[j][i] == 1:
                    c = pygame.Color('green')                
                else:
                    c = pygame.Color('white')
                pygame.draw.rect(self.screen, c, (i * self.cell_size + 1, j * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        self.life.curr_generation = self.life.create_grid(True)


        pause = True
        running = True
        while running:
                    
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        pause = True
            self.draw_lines()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE
            self.draw_grid()
            pygame.display.flip()
            while pause:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        running = False
                        pause = False
                    elif event.type == MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        i = pos[1] // self.cell_size
                        j = pos[0] // self.cell_size
                        if self.life.curr_generation[i][j] == 1:
                            self.life.curr_generation[i][j] = 0
                        else:
                            self.life.curr_generation[i][j] = 1
                        self.draw_grid()
                        pygame.display.flip()
                    elif event.type == KEYDOWN:
                        if event.key == K_SPACE:
                            pause = False
            self.life.step()
            if (not self.life.is_max_generations_exceeded) or (not self.life.is_changing):
                running = False
            clock.tick(self.speed)
        pygame.quit()
