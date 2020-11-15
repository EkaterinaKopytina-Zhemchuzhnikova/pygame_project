import pygame
from random import randint

pygame.init()
size = 1000, 450
screen = pygame.display.set_mode(size)


class MyBoard:
    # создание поля игрока-человека
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.x_0, self.y_0, self.cell_size = 10, 10, 30
        self.cnt_single_decks = 4
        self.cnt_double_decks = 3
        self.cnt_three_deck = 2
        self.cnt_four_deck = 1

    # настройка внешнего вида
    def set_view(self, x_0, y_0, cell_size):
        self.x_0 = x_0
        self.y_0 = y_0
        self.cell_size = cell_size

    def render(self):

        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 1:
                    pygame.draw.rect(screen, pygame.Color('green'), (
                        x * self.cell_size + self.x_0, y * self.cell_size + self.y_0, self.cell_size, self.cell_size))
                if self.board[y][x] == 2:
                    pygame.draw.rect(screen, pygame.Color('green'), (
                        x * self.cell_size + self.x_0, y * self.cell_size + self.y_0, self.cell_size, self.cell_size))
                if self.board[y][x] == 3:
                    pygame.draw.rect(screen, pygame.Color('green'), (
                        x * self.cell_size + self.x_0, y * self.cell_size + self.y_0, self.cell_size, self.cell_size))
                if self.board[y][x] == 4:
                    pygame.draw.rect(screen, pygame.Color('green'), (
                        x * self.cell_size + self.x_0, y * self.cell_size + self.y_0, self.cell_size, self.cell_size))
                pygame.draw.rect(screen, pygame.Color(255, 255, 255), (
                    x * self.cell_size + self.x_0, y * self.cell_size + self.y_0, self.cell_size, self.cell_size), 1)

    def number_of_neighbors(self, x, y):  # считаем количество соседей
        result = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                    continue
                result += self.board[y + dy][x + dx]
        return result

    def on_click(self, cell): # по клику мышкой ставим свои корабли
        global right, one, two, three, four
        x, y = cell
        if right and two:
            x_end, y_end = x + 1, y
        elif right and three:
            x_end, y_end = x + 2, y
        elif right and four:
            x_end, y_end = x + 3, y
        elif not right and two:
            x_end, y_end = x, y + 1
        elif not right and three:
            x_end, y_end = x, y + 2
        elif not right and four:
            x_end, y_end = x, y + 3

        if one and not self.number_of_neighbors(x, y) and self.cnt_single_decks:
            self.board[y][x] = 1
            self.cnt_single_decks -= 1
        if two and right and not x + 1 == 10:
            if not self.number_of_neighbors(x, y) and not self.number_of_neighbors(x_end,
                                                                                   y_end) and self.cnt_double_decks:
                self.board[y][x] = 2
                self.board[y_end][x_end] = 2
                self.cnt_double_decks -= 1
        elif two and not right and not y + 1 == 10:
            if not self.number_of_neighbors(x, y) and not self.number_of_neighbors(x_end,
                                                                                   y_end) and self.cnt_double_decks:
                self.board[y][x] = 2
                self.board[y_end][x_end] = 2
                self.cnt_double_decks -= 1

        if three and right and x + 2 < 10:
            if not self.number_of_neighbors(x, y) and not self.number_of_neighbors(x_end,
                                                                                   y_end) and self.cnt_three_deck:
                self.board[y][x] = 3
                self.board[y_end][x_end] = 3
                self.board[y_end][x_end - 1] = 3
                self.cnt_three_deck -= 1
        elif three and not right and y + 2 < 10:
            if not self.number_of_neighbors(x, y) and not self.number_of_neighbors(x_end,
                                                                                   y_end) and self.cnt_three_deck:
                self.board[y][x] = 3
                self.board[y_end][x_end] = 3
                self.board[y_end - 1][x_end] = 3
                self.cnt_three_deck -= 1

        if four and right and x + 3 < 10:
            if not self.number_of_neighbors(x, y) and not self.number_of_neighbors(x_end, y_end) and self.cnt_four_deck:
                self.board[y][x] = 4
                self.board[y_end][x_end] = 4
                self.board[y_end][x_end - 1] = 4
                self.board[y_end][x_end - 2] = 4
                self.cnt_four_deck -= 1
        elif four and not right and y + 3 < 10:
            if not self.number_of_neighbors(x, y) and not self.number_of_neighbors(x_end, y_end) and self.cnt_four_deck:
                self.board[y][x] = 4
                self.board[y_end][x_end] = 4
                self.board[y_end - 1][x_end] = 4
                self.board[y_end - 2][x_end] = 4
                self.cnt_four_deck -= 1

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.x_0) // self.cell_size
        cell_y = (mouse_pos[1] - self.y_0) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)


class EnemyBoard:
    # создание поля
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left, self.top, self.cell_size = 50, 10, 30
        self.cnt_one = 4
        self.cnt_two = 3
        self.cnt_three = 2
        self.cnt_four = 1

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 1:
                    pygame.draw.rect(screen, pygame.Color('green'), (
                        x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size))
                if self.board[y][x] == 2:
                    pygame.draw.rect(screen, pygame.Color('green'), (
                        x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                        self.cell_size))
                if self.board[y][x] == 3:
                    pygame.draw.rect(screen, pygame.Color('green'), (
                        x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size))
                if self.board[y][x] == 4:
                    pygame.draw.rect(screen, pygame.Color('green'), (
                        x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size))
                pygame.draw.rect(screen, pygame.Color(255, 255, 255),
                                 (x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                                  self.cell_size), 1)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def number_of_neighbors_of_enemy(self, x, y):  # считаем количество соседей
        result = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                    continue
                result += self.board[y + dy][x + dx]
        return result

    def take_a_cage(self): # рандомно ставим корабли противника
        while self.cnt_four:
            cell = self.get_random_position()
            direction = randint(0, 1)
            if direction and cell and cell[0] + 3 < 10:
                x, y = cell
                x_end, y_end = x + 3, y
                x_pre_end, y_pre_end = x + 2, y
                x_next, y_next = x + 1, y
            elif not direction and cell and cell[1] + 3 < 10:
                x, y = cell
                x_end, y_end = x, y + 3
                x_pre_end, y_pre_end = x, y + 2
                x_next, y_next = x, y + 1
            else:
                continue
            if not self.number_of_neighbors_of_enemy(x, y) and not self.number_of_neighbors_of_enemy(x_end, y_end):
                self.board[y][x] = 4
                self.board[y_end][x_end] = 4
                self.board[y_pre_end][x_pre_end] = 4
                self.board[y_next][x_next] = 4
                self.cnt_four -= 1

        while self.cnt_three:
            cell = self.get_random_position()
            direction = randint(0, 1)
            if direction and cell and cell[0] + 2 < 10:
                x, y = cell
                x_end, y_end = x + 2, y
                x_next, y_next = x + 1, y
            elif not direction and cell and cell[1] + 2 < 10:
                x, y = cell
                x_end, y_end = x, y + 2
                x_next, y_next = x, y + 1
            else:
                continue
            if not self.number_of_neighbors_of_enemy(x, y) and not self.number_of_neighbors_of_enemy(x_end, y_end):
                self.board[y][x] = 3
                self.board[y_end][x_end] = 3
                self.board[y_next][x_next] = 3
                self.cnt_three -= 1

        while self.cnt_two:
            cell = self.get_random_position()
            direction = randint(0, 1)
            if direction and cell and cell[0] + 1 < 10:
                x, y = cell
                x_end, y_end = x + 1, y
            elif not direction and cell and cell[1] + 1 < 10:
                x, y = cell
                x_end, y_end = x, y + 1
            else:
                continue
            if not self.number_of_neighbors_of_enemy(x, y) and not self.number_of_neighbors_of_enemy(x_end, y_end):
                self.board[y][x] = 2
                self.board[y_end][x_end] = 2
                self.cnt_two -= 1

        while self.cnt_one:
            cell = self.get_random_position()
            if cell:
                x, y = cell
                if not self.number_of_neighbors_of_enemy(x, y):
                    self.board[y][x] = 1
                    self.cnt_one -= 1

    def get_random_position(self):
        x = randint(0, self.width)
        y = randint(0, self.height)
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        return x, y


my_board = MyBoard(10, 10)
my_board.set_view(10, 10, 40)
en_board = EnemyBoard(10, 10)
en_board.set_view(450, 10, 40)
en_board.take_a_cage()
running = True
one = two = three = four = right = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            my_board.get_click(event.pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                right = True
            elif event.key == pygame.K_DOWN:
                right = False
            elif event.key == pygame.K_1:
                one, two, three, four = True, False, False, False
            elif event.key == pygame.K_2:
                one, two, three, four = False, True, False, False
            elif event.key == pygame.K_3:
                one, two, three, four = False, False, True, False
            elif event.key == pygame.K_4:
                one, two, three, four = False, False, False, True

    screen.fill((0, 0, 0))
    my_board.render()
    en_board.render()
    pygame.display.flip()
