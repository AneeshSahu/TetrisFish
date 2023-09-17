import random

import pygame
import time


class DisplayAbstraction():
    tetronome = {0: "L", 1: "J", 2: "T", 3: "S" , 4: "Z", 5 : "I", 6: "O"}
    tetronomeShape = ((4,5,6,14),(4,5,6,16),(4,5,6,15),(5,6,14,15),(4,5,15,16),(3,4,5,6),(4,5,14,15))
    spawnpoint = 3

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((500,1000))

        self.shape = (10, 22)
        self.board = [0 for i in range(self.shape[0] * self.shape[1])]
        self.objects = []
        self.objects.append(pygame.draw.rect(self.screen, (255, 255, 255), (0, 0, 500, 1000)))
        self.currentTetronome = 0
        self.clock = pygame.time.Clock()
        self.tickrate = 100 # ms

        self.SpawnATetronome()

        #self.counter = 0 # counts up to a second in ticks
        #self.lastframe = 0

    def CheckLegality(self,direction):
        start, end,step = 0,0,0
        move = 0
        if direction == "Right":
            start = self.shape[0] - 1
            end = self.shape[0] * self.shape[1]
            step = self.shape[0]
            move = 1
        elif direction == "Left":
            start = 0
            end = self.shape[0] * self.shape[1]
            step = self.shape[0]
            move = -1
        elif direction == "Down":
            start = self.shape[0] * self.shape[1] - self.shape[0]
            end = self.shape[0] * self.shape[1]
            step = 1
            move = self.shape[0]
        for i in range(start, end, step):
            if self.board[i] == 1:
                return False
        for i in range(0, self.shape[0]*self.shape[1]):
            if self.board[i] == 1:
                if i + move >= self.shape[0]*self.shape[1] or i + move < 0:
                    return False
                elif self.board[i + move] == 2:
                    return False
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
        elif event['scancode'] == 44:  # Space
            while self.CheckLegality("Down"):
                self.Move("Down")

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

    def SpawnATetronome(self):
        self.currentTetronome = random.randint(0,6)
        for i in self.tetronomeShape[self.currentTetronome]:
            if self.board[i] == 2:
                print("Game Over")
                pygame.quit()
                quit()
            self.board[i] = 1


    def draw(self):
        for x in range(self.shape[0]):
            for y in range(self.shape[1]):
                if self.board[x + y * self.shape[0]] == 1:
                    colour = (255,0,0)
                elif self.board[x + y * self.shape[0]] == 2:
                    colour = (0,0,0)
                else:
                    colour = (255,255,255)
                pygame.draw.rect(self.screen, colour,(x * 50, (y-2) * 50, x * 50 + 50, (y-2) * 50 + 50))
    def MoveCurrentBlockDown(self):
        if self.CheckLegality("Down"):
            self.Move("Down")
        else:
            self.board = [x if x != 1 else 2 for x in self.board]
            self.SpawnATetronome()

    def checkRows(self):
        for i in range (self.shape[1]-1,-1,-1):
            full = True
            for j in range (self.shape[0]):
                if self.board[j + i * self.shape[0]] != 2:
                    full = False
            if full:
                #print("Row " + str(i) + " is full")
                self.deleterow(i)

    def deleterow(self,row):
        for row in range(row,0,-1):
            for column in range(self.shape[0]):
                self.board[column + row * self.shape[0]] = self.board[column + (row-1) * self.shape[0]]
        for column in range(self.shape[0]):
            self.board[column] = 0

    def run (self):
        counter = 0
        while (True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    self.Keypress(event.dict)
            #print(pygame.time.get_ticks() / 1000)
            if pygame.time.get_ticks() % (1000 // self.tickrate) == 0:
                counter+=1
                if counter == (1000 // self.tickrate):
                    counter = 0
                    #print(time.time())
                if counter == 5:
                    self.MoveCurrentBlockDown()
                self.checkRows()
                self.draw()
                #print(counter)
            pygame.display.flip()

            self.clock.tick(self.tickrate)





dis = DisplayAbstraction()
dis.run()
