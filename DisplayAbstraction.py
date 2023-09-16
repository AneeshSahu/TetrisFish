import pygame
import time


class DisplayAbstraction():
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((500,1000))

        self.shape = (10, 22)
        self.board = [0 for i in range(self.shape[0] * self.shape[1])]
        self.objects = []
        self.objects.append(pygame.draw.rect(self.screen, (255, 255, 255), (0, 0, 500, 1000)))
        self.board[self.shape[0]*2 + 1] = 1

        self.clock = pygame.time.Clock()
        self.tickrate = 60

        #self.counter = 0 # counts up to a second in ticks
        #self.lastframe = 0

    def CheckLegality(self,direction):
        start, end,step = 0,0,0
        if direction == "Right":
            start = self.shape[0] - 1
            end = self.shape[0] * self.shape[1]
            step = self.shape[0]
        elif direction == "Left":
            start = 0
            end = self.shape[0] * self.shape[1]
            step = self.shape[0]
        elif direction == "Down":
            start = 0
            end = self.shape[0] * self.shape[1] - self.shape[0]
            step = 1
        for i in range(start, end, step):
            if self.board[i] == 1:
                print(f"This move is illegal")
                return False
        print("This move is legal")
        return True

    def Keypress(self, event):
        if event['scancode'] == 81 and self.CheckLegality("Down"):  # Down
            self.Move("Down")
        elif event['scancode'] == 79 and self.CheckLegality("Right"):  # Right
            self.Move("Right")
        elif event['scancode'] == 80 and self.CheckLegality("Left"):  # Left
            self.Move("Left")
        elif event['scancode'] == 82:  # Up
            found = self.board.index(1)
            self.board[found - self.shape[0] ], self.board [found] = 1, 0

    def Move(self, direction):
        if direction == "Down":
            for x in range(self.shape[0]):
                for y in range(self.shape[1]-1, -1, -1):
                    if self.board[x + y * self.shape[0]] == 1:
                        self.board[x + (y+1) * self.shape[0]], self.board[x + y * self.shape[0]] = 1, 0
        elif direction == "Right" :
            for x in range(self.shape[0]-1, -1, -1):
                for y in range(self.shape[1]):
                    if self.board[x + y * self.shape[0]] == 1:
                        self.board[x+1 + y * self.shape[0]], self.board[x + y * self.shape[0]] = 1, 0
        elif direction == "Left" :
            for x in range(self.shape[0]):
                for y in range(self.shape[1]):
                    if self.board[x + y * self.shape[0]] == 1:
                        self.board[x-1 + y * self.shape[0]], self.board[x + y * self.shape[0]] = 1, 0

    def draw(self):
        for x in range(self.shape[0]):
            for y in range(self.shape[1]):
                if self.board[x + y * self.shape[0]] == 1:
                    colour = (255,0,0)
                else:
                    colour = (255,255,255)
                pygame.draw.rect(self.screen, colour,(x * 50, (y-2) * 50, x * 50 + 50, (y-2) * 50 + 50))
    def run (self):
        while (True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    self.Keypress(event.dict)
            if pygame.time.get_ticks() % (1000 // self.tickrate) == 0:
                self.draw()
            pygame.display.flip()
            self.clock.tick(self.tickrate)




dis = DisplayAbstraction()
dis.run()
