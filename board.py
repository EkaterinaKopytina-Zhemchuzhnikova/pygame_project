import pygame, os, sys
from random import randint, choice

pygame.init()
size = WIDTH, HEIGHT = 1000, 450
screen = pygame.display.set_mode(size)


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def start_screen():
    x, y = None, None
    intro_text = ["Игра 'Морской бой'", "",
                  "Правила игры",
                  "Помощь"]
    menu_border = pygame.sprite.Group()

    fon = pygame.transform.scale(load_image('start screen.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 100
    for line in intro_text:
        sprite = pygame.sprite.Sprite()
        sprite.string_rendered = font.render(line, 1, pygame.Color('black'))
        sprite.intro_rect = sprite.string_rendered.get_rect()
        menu_border.add(sprite)
        text_coord += 10
        sprite.intro_rect.top = text_coord
        sprite.intro_rect.x = 10
        text_coord += sprite.intro_rect.height
        screen.blit(sprite.string_rendered, sprite.intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for spr in menu_border:
                    if spr.intro_rect.collidepoint(event.pos):
                        index_in_nenu = menu_border.sprites().index(spr)
                        if index_in_nenu == 0:
                            return
                        elif index_in_nenu == 2:
                            readfile('data/Rules.txt')
                        elif index_in_nenu == 3:
                            readfile('data/Help.txt')
            elif event.type == pygame.KEYDOWN:
                return
        pygame.display.flip()


def readfile(filename):
    screen.fill(pygame.Color("#4682B4"))
    text_coord = 3
    font = pygame.font.Font(None, 25)
    with open(filename, 'rt') as f:
        read_data = list(map(str.strip, f.readlines()))
        for line in read_data:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


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
        self.cnt_hit_my_board = 0
        self.cnt_boat = 10

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
                if self.board[y][x] == -1:
                    pygame.draw.line(screen, pygame.Color("red"),
                                     (self.x_0 + x * self.cell_size + 2, self.y_0 + y * self.cell_size + 2),
                                     (self.x_0 + x * self.cell_size - 2 + self.cell_size,
                                      self.y_0 + y * self.cell_size - 2 + self.cell_size), 2)
                    pygame.draw.line(screen, pygame.Color("red"),
                                     (self.x_0 + x * self.cell_size + 2,
                                      self.y_0 + y * self.cell_size + self.cell_size - 2),
                                     (self.x_0 + x * self.cell_size - 2 + self.cell_size,
                                      self.y_0 + y * self.cell_size + 2), 2)
                if self.board[y][x] == -2:
                    pygame.draw.rect(screen, pygame.Color('red'), (
                        x * self.cell_size + self.cell_size // 2 + self.x_0,
                        y * self.cell_size + self.cell_size // 2 + self.y_0, 3, 3))
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

    def on_click(self, cell):  # по клику мышкой ставим свои корабли
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
            self.cnt_boat -= 1
        if two and right and not x + 1 == 10:
            if not self.number_of_neighbors(x, y) and not self.number_of_neighbors(x_end,
                                                                                   y_end) and self.cnt_double_decks:
                self.board[y][x] = 2
                self.board[y_end][x_end] = 2
                self.cnt_double_decks -= 1
                self.cnt_boat -= 1
        elif two and not right and not y + 1 == 10:
            if not self.number_of_neighbors(x, y) and not self.number_of_neighbors(x_end,
                                                                                   y_end) and self.cnt_double_decks:
                self.board[y][x] = 2
                self.board[y_end][x_end] = 2
                self.cnt_double_decks -= 1
                self.cnt_boat -= 1

        if three and right and x + 2 < 10:
            if not self.number_of_neighbors(x, y) and not self.number_of_neighbors(x_end,
                                                                                   y_end) and self.cnt_three_deck:
                self.board[y][x] = 3
                self.board[y_end][x_end] = 3
                self.board[y_end][x_end - 1] = 3
                self.cnt_three_deck -= 1
                self.cnt_boat -= 1
        elif three and not right and y + 2 < 10:
            if not self.number_of_neighbors(x, y) and not self.number_of_neighbors(x_end,
                                                                                   y_end) and self.cnt_three_deck:
                self.board[y][x] = 3
                self.board[y_end][x_end] = 3
                self.board[y_end - 1][x_end] = 3
                self.cnt_three_deck -= 1
                self.cnt_boat -= 1

        if four and right and x + 3 < 10:
            if not self.number_of_neighbors(x, y) and not self.number_of_neighbors(x_end, y_end) and self.cnt_four_deck:
                self.board[y][x] = 4
                self.board[y_end][x_end] = 4
                self.board[y_end][x_end - 1] = 4
                self.board[y_end][x_end - 2] = 4
                self.cnt_four_deck -= 1
                self.cnt_boat -= 1
        elif four and not right and y + 3 < 10:
            if not self.number_of_neighbors(x, y) and not self.number_of_neighbors(x_end, y_end) and self.cnt_four_deck:
                self.board[y][x] = 4
                self.board[y_end][x_end] = 4
                self.board[y_end - 1][x_end] = 4
                self.board[y_end - 2][x_end] = 4
                self.cnt_four_deck -= 1
                self.cnt_boat -= 1
        if not self.cnt_boat:
            global can_arrange
            can_arrange = False

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
        self.cnt_hit_enemy_board = 0
        self.hitting_the_ship = False
        self.battle_dict = {1: 4, 2: 3, 3: 2, 4: 1}
        self.likely_positions = []
        self.next_step = False
        self.ships_coord = []

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

                if self.board[y][x] == -1:
                    pygame.draw.line(screen, pygame.Color("red"),
                                     (self.left + x * self.cell_size + 2, self.top + y * self.cell_size + 2),
                                     (self.left + x * self.cell_size - 2 + self.cell_size,
                                      self.top + y * self.cell_size - 2 + self.cell_size), 2)
                    pygame.draw.line(screen, pygame.Color("red"),
                                     (self.left + x * self.cell_size + 2,
                                      self.top + y * self.cell_size + self.cell_size - 2),
                                     (self.left + x * self.cell_size - 2 + self.cell_size,
                                      self.top + y * self.cell_size + 2), 2)
                if self.board[y][x] == -2:
                    pygame.draw.rect(screen, pygame.Color('red'), (
                        x * self.cell_size + self.cell_size // 2 + self.left,
                        y * self.cell_size + self.cell_size // 2 + self.top, 3, 3))
                pygame.draw.rect(screen, pygame.Color(255, 255, 255),
                                 (x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                                  self.cell_size), 1)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        global move
        print(move)
        if move:
            cell = self.get_cell(mouse_pos)
            move = not move
            print(move)
            self.on_click(cell)
            self.attack()

    def on_click(self, cell):
        x, y = cell
        if self.board[y][x] and self.board[y][x] != -2:
            self.board[y][x] = -1
            self.cnt_hit_enemy_board += 1
        else:
            self.board[y][x] = -2

    def attack(self):
        global move
        if not move:
            move = not move
            if not self.next_step:
                cell = self.get_random_position()
                if cell:
                    x, y = cell
                    if my_board.board[y][x] and my_board.board[y][x] != -2 and my_board.board[y][x] != -1:
                        self.rang = my_board.board[y][x]
                        my_board.board[y][x] = -1
                        self.hitting_the_ship = True
                        self.hitting_pos = y, x
                    elif not my_board.board[y][x]:
                        my_board.board[y][x] = -2
            # elif self.next_step:
            #     my_board.board[self.step[1]][self.step[0]] = -1

            if self.hitting_the_ship:
                self.answer_the_questions_enemy(self.hitting_pos)

    def answer_the_questions_enemy(self, coord):
        global move
        y, x = coord
        print("координаты переданные в функцию", coord)
        if coord not in self.ships_coord:
            self.ships_coord.append(coord)
        answer = input('убит, ранен или мимо?')
        if answer == "убит":
            self.hitting_the_ship = False
            for y, x in self.ships_coord:
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                            continue
                        if my_board.board[y + dy][x + dx] == 0:
                            print(my_board.board[y + dy][x + dx])
                            my_board.board[y + dy][x + dx] = -2
                        elif my_board.board[y + dy][x + dx] > 0:
                            print(my_board.board[y + dy][x + dx])
                            my_board.board[y + dy][x + dx] = -1
            self.battle_dict[len(self.ships_coord)] -= 1
            self.likely_positions.clear()
            self.ships_coord.clear()
            self.next_step = False

        elif answer == "ранен":
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    # ходим по вертикали либо горизонтали
                    if dx * dy != 0:
                        continue
                    # за пределы поля не выходим
                    if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                        continue
                    if my_board.board[y + dy][x + dx] == self.rang:
                        print(my_board.board[y + dy][x + dx], my_board.board[y][x])
                        self.likely_positions.append((y + dy, x + dx))
            if self.likely_positions:
                self.step = self.likely_positions.pop(0)
                self.ships_coord.append(self.step)
                print("очередной шаг", self.step)
                print("вероятные позиции", self.likely_positions)
                self.next_step = True
            print('сейчас в списке палубы', self.ships_coord)

        # elif answer == "мимо":
        #     self.ships_coord -= self.ships_coord[-1]

    def number_of_neighbors_of_enemy(self, x, y):  # считаем количество соседей
        result = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                    continue
                result += self.board[y + dy][x + dx]
        return result

    def take_a_cage(self):  # рандомно ставим корабли противника
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
        while True:
            x = randint(0, self.width)
            y = randint(0, self.height)
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                continue
            return x, y


def congradulations(winner):
    message = "Вы выиграли! Поздравляем!" if winner == "people" else "Вы проиграли!"
    font = pygame.font.Font(None, 50)
    text = font.render(message, True, pygame.Color("#000080"))
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()

    create_particles((text_x, text_y, text_w, text_h))

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.fill(pygame.Color("#4682B4"))
        screen.blit(text, (text_x, text_y))
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(20)
        pygame.display.flip()


all_sprites = pygame.sprite.Group()


class Particle(pygame.sprite.Sprite):
    img = [load_image("fei2.png", -1)]
    for scale in (5, 10, 20):
        img.append(pygame.transform.scale(img[0], (scale, scale)))

    def __init__(self, dx, dy, mess_rect):
        super().__init__(all_sprites)
        self.image = choice(self.img)
        self.rect = self.image.get_rect()
        self.mess_rect = mess_rect
        while True:
            self.rect.x, self.rect.y = randint(0, WIDTH - self.rect.w), randint(0, HEIGHT - self.rect.h)
            if not self.rect.colliderect(self.mess_rect):
                break

    def update(self):
        self.rect.y = self.rect.y - 1
        if self.rect.colliderect(self.mess_rect):
            self.kill()


def create_particles(mess_rect):
    particle_count = 30
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(choice(numbers), choice(numbers), mess_rect)


start_screen()
my_board = MyBoard(10, 10)
my_board.set_view(10, 10, 40)
en_board = EnemyBoard(10, 10)
en_board.set_view(450, 10, 40)
en_board.take_a_cage()
running = True
one = two = three = four = right = None
move = True
can_arrange = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if can_arrange:
                my_board.get_click(event.pos)
            else:
                en_board.get_click(event.pos)
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
terminate()
