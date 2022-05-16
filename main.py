from re import X
import pygame
import random
import math


def setup():
    global WN, first_press, font, font1, font2, font3, SCREEN_HEIGHT, SCREEN_WIDTH, colors, pressed
    first_press = True
    pressed = False
    pygame.init()
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 1000
    font = pygame.font.SysFont("Comic Sans MS", 60)
    font1 = pygame.font.SysFont("Comic Sans MS", 60)
    font2 = pygame.font.SysFont("Comic Sans MS", 50)
    font3 = pygame.font.SysFont("Comic Sans MS", 40)
    WN = pygame.display.set_mode((1000, 1000))
    colors = [randclr() for i in range(40)]
    # print(colors)


def randclr():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def resetGame():
    return


def draw():
    # Fill background
    WN.fill("black")
    # Draw squares And Numbers
    for y, row in enumerate(game.grid):
        for x, block in enumerate(row):
            if game.grid[y][x] == "":
                continue
            lx, ly = (x * (SCREEN_WIDTH - 10) / game.size[0]) + 5, (
                y * (SCREEN_WIDTH - 10) / game.size[1]
            ) + 5
            pygame.draw.rect(
                WN,
                (0, 255, 0),
                pygame.Rect(
                    lx, ly, SCREEN_WIDTH / game.size[0], SCREEN_HEIGHT / game.size[1]
                ),
                3,
            )
            n = game.grid[y][x]
            # DRAW TEXT
            if int(game.grid[y][x]) > 120:
                text = font3.render(str(n), True, colors[int(math.log(n, 2))])
            else:
                text = font.render(str(n), True, colors[int(math.log(n, 2))])
            text_rect = text.get_rect(center=((lx + 45, ly + 45)))
            WN.blit(text, text_rect)
    if len(selected) >= 2:
        points = list(
            map(
                lambda cord: (tuple(map(lambda p: ((p + 1) * 100) - 50, cord))),
                selected,
            )
        )
        for i, point in enumerate(points):
            if i - 1 == -1:
                continue
            pygame.draw.line(WN, (0, 0, 255), point, points[i - 1], 10)

    mouseCalculations()
    pygame.display.update()
    return


def mouseCalculations():
    mouse = pygame.mouse.get_pressed()
    global first_press, last_press, pressed
    if mouse[0] and not pressed:
        pressed = True
    elif not mouse[0]:
        pressed = False
    if mouse[0] and selected:
        pygame.draw.line(
            WN,
            (0, 0, 255),
            cfi(),
            pygame.mouse.get_pos(),
            10,
        )
    if mouse[2]:
        selected.clear()


def mouseCalc():
    return tuple(n // 100 for n in pygame.mouse.get_pos())


def cfi():  # Cords from index
    return tuple(map(lambda p: ((p + 1) * 100) - 50, selected[-1]))


def eventHandling():
    events = pygame.event.get()
    for ev in events:
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit("Game Closed")


selected = []


def logic():
    # print(tuple(n//100 for n in pygame.mouse.get_pos()))
    x, y = mouseCalc()
    if not (x, y) in selected and pygame.mouse.get_pressed()[0]:
        if selected:
            lx, ly = selected[0]
            kx, ky = selected[-1]

            current_block = 2 ** math.floor(
                math.log(sum(list(map(lambda c: (game.grid[c[1]][c[0]]), selected))), 2)
            )
            if (
                (
                    game.grid[y][x] == current_block
                    or game.grid[y][x] == game.grid[ky][kx]
                )
                and -1 <= x - kx <= 1
                and -1 <= y - ky <= 1
            ):
                selected.append((x, y))
        else:
            selected.append((x, y))
    if not pressed:
        if len(selected) >= 2:
            kx, ky = selected[-1]
            tot = sum(list(map(lambda c: (game.grid[c[1]][c[0]]), selected)))
            tot = 2 ** math.floor(math.log(tot, 2))
            game.grid[ky][kx] = tot
            # print(tot)
            for c in selected[:-1]:
                game.grid[c[1]][c[0]] = ""
        selected.clear()
    if not "" in str(game.grid):
        return
    for y, row in enumerate(game.grid):
        for x, cel in enumerate(row):
            if cel == "":
                if y - 1 < 0:
                    game.grid[y][x] = 1 << random.randrange(*game.range)
                else:
                    game.grid[y][x] = game.grid[y - 1][x]
                    game.grid[y - 1][x] = ""


class Game:
    def __init__(self, rang, size):
        self.range = rang
        self.size = size
        self.grid = []
        self.setup()

    def setup(self):
        for y in range(self.size[0]):
            self.grid.append([])
            for x in range(self.size[1]):
                self.grid[y].append(2 ** random.randrange(*self.range))
        # print(list(self.grid))


setup()

gameLoop = True
game = Game((2, 6), [10, 10])
while gameLoop:
    draw()
    logic()
    eventHandling()
    clock = pygame.time.Clock()
    clock.tick(120)
