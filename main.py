import pygame, random, math

def setup():
    global WN, first_press, font, SCREEN_HEIGHT, SCREEN_WIDTH
    first_press = True
    pygame.init()
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 1000
    WN = pygame.display.set_mode( (1000, 1000) )
    font = pygame.font.SysFont("Comic Sans MS", 70)
    return

def resetGame():
    return

def draw():
    WN.fill("black")
    for y, row in enumerate(game.grid):
        for x, block in enumerate(game.grid):
            lx,ly = (y*100)+5,(x*100)+5
            pygame.draw.rect(WN, (0,255,0), pygame.Rect(ly,lx,90,90), 3)
            n = game.grid[y][x]
            text = font.render(str(n), True, (140,0,140))
            text_rect = text.get_rect(center=((lx+45, ly+45)))
            WN.blit(text, text_rect)


            # WN.blit(txt, (lx+25, ly+25))
    mouseCalculations()
    pygame.display.update()
    return

def mouseCalculations():
    global first_press, last_press
    if pygame.mouse.get_pressed()[0]:
        first_press = False
        last_press = tuple(map(lambda c: ((((c//100)+1)*100)-50),pygame.mouse.get_pos()))
    elif pygame.mouse.get_pressed()[2]:
        first_press = True

    if not first_press:
        # print(last_press)
        # print(WN, (0,0,255), last_press, pygame.mouse.get_pos(), 10)
        pygame.draw.line(WN, (0,0,255), tuple(map(lambda c: (c+0),last_press)), pygame.mouse.get_pos(), 10,)
        pygame.draw.circle(WN, (0,0,255), last_press, 5)
        
def mouseCalc():
    return tuple(map(lambda c: ((c//100)),pygame.mouse.get_pos()))

def eventHandling():
    events = pygame.event.get()
    for ev in events:
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit("Game Closed")

selected = []
def logic():

    x,y = mouseCalc()
    if not (y,x) in selected and pygame.mouse.get_pressed()[0]:
        if selected:
            ly, lx = selected[0]
            ky, kx = selected[-1]
            print(x-kx , y-ky)
            if game.grid[x][y] == game.grid[lx][ly] and -1 <= x-kx <= 1 and -1 <= y-ky <= 1:
                print("hello")
                selected.append((y,x)) 
        else:
            selected.append((y,x))
    if pygame.mouse.get_pressed()[2]:
        if len(selected) >= 2:
            ky, kx = selected[-1]
            tot = sum(list(map(lambda c: (game.grid[c[1]][c[0]]), selected)))
            tot = 2**math.floor(math.log(tot,2))
            game.grid[kx][ky] = tot
            print(tot)
            for c in selected[:-1]:
                game.grid[c[1]][c[0]] = 0
        selected.clear()
    # print(selected)

class Game():
    def __init__(self, rang, size):
        self.range = rang
        self.size = size
        self.grid = []
        self.setup()

    def setup(self):
        for y in range(self.size[0]):
            self.grid.append([])
            for x in range(self.size[1]):
                self.grid[y].append(2**random.randrange(0, self.range))
        print(list(self.grid))
setup()

gameLoop = True
game = Game(5, [10,10])
while gameLoop:
    draw()
    logic()
    eventHandling()