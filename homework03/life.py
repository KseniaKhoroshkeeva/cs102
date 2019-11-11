import pathlib
import random
import copy

from typing import List, Optional, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:
    
    def __init__(
        self,
        size: Tuple[int, int],
        randomize: bool=True,
        max_generations: Optional[float]=float('inf')
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool=False) -> Grid:
        grid = []
        for i in range(self.rows):
            grid.append([0]*self.cols)
        if randomize:
            for i in range(self.rows):
                for j in range(self.cols):
                    grid[i][j] = random.randint(0, 1)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        n = []

        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i >= 0) and (i <= self.rows - 1) and (j >= 0) and (j <= self.cols - 1) and not (i == cell[0] and j == cell[1]):
                    n.append(self.curr_generation[i][j])

        return n

    def get_next_generation(self) -> Grid:
        new_grid = copy.deepcopy(self.curr_generation)
        for i in range(self.rows):
            for j in range(self.cols):
                pos = (i, j)
                neigh = 0
                for k in range(len(self.get_neighbours(pos))):
                    if self.get_neighbours(pos)[k] == 1:
                        neigh += 1
                if self.curr_generation[i][j] == 1:
                    if neigh != 2 and neigh != 3:
                        new_grid[i][j] = 0
                else:
                    if neigh == 3:
                        new_grid[i][j] = 1
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = copy.deepcopy(self.curr_generation)
        self.curr_generation = self.get_next_generation()
        self.generations +f= 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations > self.generations:
            return True
        else:
            return False
    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.curr_generation != self.prev_generation:
            return True
        else:
            return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        i = 0
        grid = []
        with open(filename) as f:
            for line in f:
                grid.append([int(x) for x in line if x in '01'])
                i += 1
        j = len(grid[0])
        game = GameOfLife((i, j))
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        f = open(filename, "w")
        for i in range(self.rows):
            for j in range(self.cols):
                f.write(str(self.curr_generation[i][j]))
            f.write('\n')
        f.close()
