import random

import pygame
import time


class DisplayAbstraction():
    tetronome = {0: "L", 1: "J", 2: "T", 3: "S", 4: "Z", 5: "I", 6: "O"}
    tetronomeShape = (
        (4, 5, 6, 14), (4, 5, 6, 16), (4, 5, 6, 15), (5, 6, 14, 15), (4, 5, 15, 16), (3, 4, 5, 6), (4, 5, 14, 15))
    spawnpoint = 3

    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((800, 1000))

        self.shape = (10, 22)
        self.board = [0 for i in range(self.shape[0] * self.shape[1])]
        self.objects = []
        self.objects.append(pygame.draw.rect(self.screen, (255, 255, 255), (0, 0, 500, 1000)))
        self.currentTetronome = 0
        self.spawnBag = []
        self.currentOrientation = 0
        self.clock = pygame.time.Clock()
        self.tickrate = 100  # ms
        self.score = 0
        self.swapped = False
        self.hold = None

        self.SpawnATetronome()


        # self.counter = 0 # counts up to a second in ticks
        # self.lastframe = 0

    def CheckLegality(self, direction):
        start, end, step = 0, 0, 0
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
        for i in range(0, self.shape[0] * self.shape[1]):
            if self.board[i] == 1:
                if i + move >= self.shape[0] * self.shape[1] or i + move < 0:
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
            # found = self.board.index(1)
            # self.board[found - self.shape[0] ], self.board [found] = 1, 0
            self.rotate()
        elif event['scancode'] == 44:  # Space
            self.moveToEnd()
        elif event['scancode'] == 6 : # c
            self.swap()

    def swap(self):
        if not self.swapped or True:
            if self.hold == None :
                self.hold = self.currentTetronome
                self.board = [x if x != 1 else 0 for x in self.board]
                self.SpawnATetronome()
            else:
                self.spawnBag.insert(0, self.hold)
                self.hold = self.currentTetronome
                self.board = [x if x != 1 else 0 for x in self.board]
                self.SpawnATetronome()
            self.swapped = True

    def moveToEnd(self):
        while self.CheckLegality("Down"):
            self.MoveCurrentBlockDown()
        self.MoveCurrentBlockDown() # extra to take block from 1 to 2

    def rotate(self):
        if self.DoRotate(False):
            self.DoRotate(True)

    def DoRotate(self, move=False):
        # {0: "L", 1: "J", 2: "T", 3: "S" , 4: "Z", 5 : "I", 6: "O"}
        ret = True
        found = self.board.index(1)
        newPeice = []
        oldPeice = []
        newOrientation = self.currentOrientation
        if self.currentTetronome == 0:
            if self.currentOrientation == 0:
                oldPeice = [found, found+1,found+2,found+self.shape[0]]
                newPeice = [found-self.shape[0],found-self.shape[0] + 1 ,found+1, found+1+self.shape[0]]
                newOrientation = 1
            if self.currentOrientation == 1:
                oldPeice = [found, found + 1, found+self.shape[0]+1, found+2*self.shape[0]+1]
                newPeice = [found+2, found+2 + self.shape[0],found+1 + self.shape[0],found+ self.shape[0] ]
                newOrientation = 2
                if found % 10 == 8 : # last row:
                    newPeice = [x-1 for x in newPeice]
                    #rerange cause else stuff gets deleted
                    newPeice[0], newPeice[1], newPeice[2] = newPeice[2], newPeice[0], newPeice[1]
                pass
            if self.currentOrientation == 2:
                # coded this wrong. Fix :
                found = found - 2 + self.shape[0]
                oldPeice = [found,found+1, found+2, found+2 -self.shape[0]]
                newPeice = [found + 1 - self.shape[0] ,found + 1, found + 1 + self.shape[0] , found +2 +self.shape[0]]
                newOrientation = 3
                pass
            if self.currentOrientation == 3:
                oldPeice = [found,found+self.shape[0],found+2*self.shape[0],found+2*self.shape[0]+1]
                if found % 10 == 0: # first row
                    found+=1
                newPeice = [found+self.shape[0] +1, found+self.shape[0], found+self.shape[0] -1, found+2*self.shape[0]-1 ]
                newOrientation = 0
                pass
        elif self.currentTetronome == 1:
            if self.currentOrientation == 0 :
                oldPeice= [found, found+1,found+2,found+2+self.shape[0]]
                newPeice= [found+1 - self.shape[0],found+1,found+1 + self.shape[0],found + self.shape[0] ]
                newOrientation = 1
            elif self.currentOrientation == 1 :
                oldPeice= [found, found+self.shape[0] , found+2*self.shape[0], found+2*self.shape[0]-1]
                if found % 10 == 9:
                    found -=1
                newPeice= [found-1,found+self.shape[0]-1,found+self.shape[0],found+self.shape[0]+1 ]
                newOrientation = 2
            elif self.currentOrientation == 2 :
                oldPeice= [found,found+self.shape[0],found+self.shape[0]+1, found+self.shape[0]+2]
                newPeice= [found+1, found+2,found+self.shape[0]+1,found+2*self.shape[0]+1]
                newOrientation = 3
            elif self.currentOrientation == 3 :
                oldPeice= [found+self.shape[0],found,found+1,found+2*self.shape[0]]
                if found % 10 == 0:
                    found+=1
                newPeice= [found+2*self.shape[0]+1,found+self.shape[0]+1,found+self.shape[0],found+self.shape[0]-1 ]
                newOrientation = 0
        elif self.currentTetronome == 2:
            if self.currentOrientation == 0:
                oldPeice = [found, found+1, found+2, found+1+self.shape[0]]
                newPeice = [found, found+1 , found+1 +self.shape[0], found-self.shape[0]+1]
                newOrientation = 1
            elif self.currentOrientation == 1:
                oldPeice = [found,found+self.shape[0], found+ self.shape[0]-1, found+2*self.shape[0]  ]
                if found%10 == 9:
                    found -=1
                newPeice = [found,found+self.shape[0],found+self.shape[0]-1,found+self.shape[0]+1]
                newOrientation = 2
            elif self.currentOrientation == 2:
                oldPeice = [found, found +self.shape[0],found +self.shape[0] - 1, found + 1 + self.shape[0]]
                newPeice = [found, found + self.shape[0], found + 1 + self.shape[0], found +2*self.shape[0]]
                newOrientation = 3
            elif self.currentOrientation == 3:
                oldPeice = [found,found+self.shape[0],found+2*self.shape[0],found+self.shape[0]+1]
                if found%10 == 0:
                    found +=1
                newPeice = [found+self.shape[0],found+self.shape[0]-1, found+self.shape[0]+1 , found+2*self.shape[0]]
                newOrientation = 0
        elif self.currentTetronome == 3:
            if self.currentOrientation == 0:
                oldPeice = [found,found+1,found+self.shape[0],found+self.shape[0]-1]
                newPeice = [found-self.shape[0], found,found+1,found+self.shape[0]+1]
                newOrientation = 1
            elif self.currentOrientation == 1:
                oldPeice = [found,found+self.shape[0],found+self.shape[0]+1,found+2*self.shape[0]+1]
                if found%10 == 0 :
                    found+=1
                newPeice = [found+self.shape[0],found+self.shape[0]+1, found+2*self.shape[0],found+2*self.shape[0]-1 ]
                newOrientation = 0
        elif self.currentTetronome == 4:
            if self.currentOrientation == 0:
                oldPeice = [found,found+1,found+self.shape[0]+1,found+self.shape[0]+2]
                newPeice = [found-self.shape[0]+2, found+2,found+1,found+self.shape[0]+1]
                newOrientation = 1
            elif self.currentOrientation == 1:
                oldPeice = [found,found+self.shape[0],found+self.shape[0]-1,found+2*self.shape[0]-1]
                if found%10 == 1 :
                    found+=1
                newPeice = [found+self.shape[0]-2,found+self.shape[0]-1, found+2*self.shape[0]-1,found+2*self.shape[0]]
                newOrientation = 0
        elif self.currentTetronome == 5:
            if self.currentOrientation == 0:
                newPeice = [found - self.shape[0] * 2 + 2, found - self.shape[0] + 2, found + 2,
                            found + 2 + self.shape[0]]
                oldPeice = [found, found + 1, found + 2, found + 3]
                newOrientation = 1
            elif self.currentOrientation == 1:
                newPeice = [found + (2 * self.shape[0]) - 2, found + (2 * self.shape[0]) - 1,
                            found + (2 * self.shape[0]), found + (2 * self.shape[0]) + 1]
                oldPeice = [found, found + self.shape[0], found + 2 * self.shape[0], found + 3 * self.shape[0]]
                newOrientation = 0
                # edge case :
                if found % 10 == 0:  # first column
                    newPeice = [found + (2 * self.shape[0]) + 3, found + (2 * self.shape[0]) + 1,
                                found + (2 * self.shape[0]) + 2, found + (2 * self.shape[0])]
                elif found % 10 == 9:  # last column
                    newPeice = [found + (2 * self.shape[0]) - 3, found + (2 * self.shape[0]) - 2,
                                found + (2 * self.shape[0]) - 1, found + (2 * self.shape[0])]
        elif self.currentTetronome == 6:
            ret = False

        if ret:
            for i in range(4):
                if self.board[newPeice[i]] == 2:
                    ret = False
            if move and ret:
                for i in range(4):
                    self.board[oldPeice[i]] = 0
                for i in range(4):
                    self.board[newPeice[i]] = 1
                self.currentOrientation = newOrientation
        return ret

    def Move(self, direction):
        if direction == "Down":
            for x in range(self.shape[0]):
                for y in range(self.shape[1] - 1, -1, -1):
                    if self.board[x + y * self.shape[0]] == 1:
                        self.board[x + (y + 1) * self.shape[0]], self.board[x + y * self.shape[0]] = 1, 0
        elif direction == "Right":
            for x in range(self.shape[0] - 1, -1, -1):
                for y in range(self.shape[1]):
                    if self.board[x + y * self.shape[0]] == 1:
                        self.board[x + 1 + y * self.shape[0]], self.board[x + y * self.shape[0]] = 1, 0
        elif direction == "Left":
            for x in range(self.shape[0]):
                for y in range(self.shape[1]):
                    if self.board[x + y * self.shape[0]] == 1:
                        self.board[x - 1 + y * self.shape[0]], self.board[x + y * self.shape[0]] = 1, 0

    def SpawnATetronome(self):
        if len(self.spawnBag) ==0 :
            self.spawnBag = [i for i in range(7)]
            self.spawnBag.append(random.randint(0,6))
            random.shuffle(self.spawnBag)

        self.currentTetronome = self.spawnBag.pop(0)
        self.currentOrientation = 0
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
                    colour = (255, 0, 0)
                elif self.board[x + y * self.shape[0]] == 2:
                    colour = (0, 0, 0)
                else:
                    colour = (255, 255, 255)
                pygame.draw.rect(self.screen, colour, (x * 50, (y - 2) * 50, x * 50 + 50, (y - 2) * 50 + 50))

                # hold
        pygame.draw.rect(self.screen, (0, 0, 0), (500, 0, 800, 1000))
        pygame.draw.rect(self.screen, (255, 255, 255), (550, 200, 200, 300))

        myfont = pygame.font.SysFont("monospace", 20)
        label = myfont.render("HOLD", 1, (0, 0, 0))
        self.screen.blit(label, (625, 200))


        if self.hold != None:
            for i in self.tetronomeShape[self.hold]:
                if self.hold == 5: # SPECIAL FOR LINE
                    pygame.draw.rect(self.screen, (255, 0, 0), (550 + (50 * (i - 3)), 300, 50, 50))
                elif i//10 == 0:
                    pygame.draw.rect(self.screen, (255, 0, 0), (575 + (50*(i-4)), 300, 50, 50))
                else:
                    pygame.draw.rect(self.screen, (255, 0, 0), (575 + (50 * (i - 14)), 350, 50, 50))
        label = myfont.render(f"SCORE : {self.score}", 1, (0,255,0))
        self.screen.blit(label, (590, 100))




    def MoveCurrentBlockDown(self):
        if self.CheckLegality("Down"):
            self.Move("Down")
        else:
            self.board = [x if x != 1 else 2 for x in self.board]
            self.checkRows()
            self.SpawnATetronome()
            self.swapped = False

    def checkRows(self):
        fullrows = []
        for i in range(self.shape[1] - 1, -1, -1):
            full = True
            for j in range(self.shape[0]):
                if self.board[j + i * self.shape[0]] != 2:
                    full = False
            if full:
                fullrows.append(i)
                # print("Row " + str(i) + " is full")
        if len(fullrows) == 1:
            self.score+=40
        if len(fullrows) == 2:
            self.score+=100
        if len(fullrows) == 3:
            self.score+=300
        if len(fullrows) == 4:
            self.score+=1200
        if len(fullrows) != 0:
            print(f'The score is {self.score}')
        for i in fullrows[::-1]:
            self.deleterow(i)


    def deleterow(self, row):
        for row in range(row, 0, -1):
            for column in range(self.shape[0]):
                self.board[column + row * self.shape[0]] = self.board[column + (row - 1) * self.shape[0]]
        for column in range(self.shape[0]):
            self.board[column] = 0

    def run(self):
        counter = 0
        while (True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    self.Keypress(event.dict)
            # print(pygame.time.get_ticks() / 1000)
            if pygame.time.get_ticks() % (1000 // self.tickrate) == 0:
                counter += 1
                if counter == (1000 // self.tickrate):
                    # print(counter)
                    counter = 0
                    # print(time.time())
                if counter == 5:
                    self.MoveCurrentBlockDown()
                self.draw()
                # print(counter)
            pygame.display.flip()

            self.clock.tick(self.tickrate)


dis = DisplayAbstraction()
dis.run()
