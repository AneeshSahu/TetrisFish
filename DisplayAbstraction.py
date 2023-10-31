import random

import pygame
import copy


class subject:
    def __init__(self):
        self.observers = []

    def register(self, observer):
        self.observers.append(observer)

    def notify(self):
        for observer in self.observers:
            observer.update()


class DisplayAbstraction(subject):
    tetronome = {0: "L", 1: "J", 2: "T", 3: "S", 4: "Z", 5: "I", 6: "O"}
    tetronomeShape = (
        (4, 5, 6, 14), (4, 5, 6, 16), (4, 5, 6, 15), (5, 6, 14, 15), (4, 5, 15, 16), (3, 4, 5, 6), (4, 5, 14, 15))
    spawnpoint = 3

    placedcolour = (0, 0, 255)
    currentcolour = (255,105,180)
    white = (255, 255, 255)

    def __init__(self):
        super().__init__()
        self.AI = False
        self.moves = []
        pygame.init()
        pygame.font.init()
        #pygame.mixer.music.load("Korobeiniki.mp3")
        #pygame.mixer.music.play(-1)

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

        # self.counter = 0 # counts up to a second in ticks
        # self.lastframe = 0

    def CheckLegality(self,direction):
        return DisplayAbstraction.CheckLegalityAbsolute(self.board,self.shape,direction)
    @staticmethod
    def CheckLegalityAbsolute(board,shape,direction):
        start, end, step = 0, 0, 0
        move = 0
        if direction == "Right":
            start = shape[0] - 1
            end = shape[0] * shape[1]
            step = shape[0]
            move = 1
        elif direction == "Left":
            start = 0
            end = shape[0] * shape[1]
            step = shape[0]
            move = -1
        elif direction == "Down":
            start = shape[0] * shape[1] - shape[0]
            end = shape[0] * shape[1]
            step = 1
            move = shape[0]
        for i in range(start, end, step):
            if board[i] == 1:
                return False
        for i in range(0, shape[0] * shape[1]):
            if board[i] == 1:
                if i + move >= shape[0] * shape[1] or i + move < 0:
                    return False
                elif board[i + move] == 2:
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
            self.Rotate(True)
        elif event['scancode'] == 44:  # Space
            self.moveToEnd()
        elif event['scancode'] == 6:  # c
            self.swap()

    def swap(self):
        if not self.swapped:
            if self.hold == None:
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
        #self.board = self.moveToEndAbsolute(self.board,self.shape)

        while self.CheckLegality("Down"):
            self.MoveCurrentBlockDown()
        self.MoveCurrentBlockDown()  # extra to take block from 1 to 2
    @staticmethod
    def moveToEndAbsolute(board,shape):
        board = copy.deepcopy(board) # deepcopy board. No mutators allowed
        while DisplayAbstraction.CheckLegalityAbsolute(board,shape,"Down"):
            board = DisplayAbstraction.MoveAbsolute(board,"Down",shape)
        board = [x if x != 1 else 2 for x in board]
        return board


    def Rotate(self, move=False):
        ret , orientation, board = DisplayAbstraction.RotateAbsolute(self.board,self.currentTetronome,self.currentOrientation,self.shape)
        if move and ret:
            self.board = board
            self.currentOrientation = orientation
        return ret

    @staticmethod
    def RotateAbsolute(board, currentTetronome, currentOrientation, shape):
        # {0: "L", 1: "J", 2: "T", 3: "S" , 4: "Z", 5 : "I", 6: "O"}
        board = copy.deepcopy(board) # deepcopy board. No mutators allowed
        ret = True
        found = board.index(1)
        newPeice = []
        oldPeice = []
        newOrientation = currentOrientation
        if currentTetronome == 0:
            if currentOrientation == 0:
                oldPeice = [found, found + 1, found + 2, found + shape[0]]
                newPeice = [found - shape[0], found - shape[0] + 1, found + 1, found + 1 + shape[0]]
                newOrientation = 1
            if currentOrientation == 1:
                oldPeice = [found, found + 1, found + shape[0] + 1, found + 2 * shape[0] + 1]
                newPeice = [found + 2, found + 2 + shape[0], found + 1 + shape[0], found + shape[0]]
                newOrientation = 2
                if found % 10 == 8:  # last row:
                    newPeice = [x - 1 for x in newPeice]
                    # rerange cause else stuff gets deleted
                    newPeice[0], newPeice[1], newPeice[2] = newPeice[2], newPeice[0], newPeice[1]
                pass
            if currentOrientation == 2:
                # coded this wrong. Fix :
                found = found - 2 + shape[0]
                oldPeice = [found, found + 1, found + 2, found + 2 - shape[0]]
                newPeice = [found + 1 - shape[0], found + 1, found + 1 + shape[0], found + 2 + shape[0]]
                newOrientation = 3
                pass
            if currentOrientation == 3:
                oldPeice = [found, found + shape[0], found + 2 * shape[0], found + 2 * shape[0] + 1]
                if found % 10 == 0:  # first row
                    found += 1
                newPeice = [found + shape[0] + 1, found + shape[0], found + shape[0] - 1,
                            found + 2 * shape[0] - 1]
                newOrientation = 0
                pass
        elif currentTetronome == 1:
            if currentOrientation == 0:
                oldPeice = [found, found + 1, found + 2, found + 2 + shape[0]]
                newPeice = [found + 1 - shape[0], found + 1, found + 1 + shape[0], found + shape[0]]
                newOrientation = 1
            elif currentOrientation == 1:
                oldPeice = [found, found + shape[0], found + 2 * shape[0], found + 2 * shape[0] - 1]
                if found % 10 == 9:
                    found -= 1
                newPeice = [found - 1, found + shape[0] - 1, found + shape[0], found + shape[0] + 1]
                newOrientation = 2
            elif currentOrientation == 2:
                oldPeice = [found, found + shape[0], found + shape[0] + 1, found + shape[0] + 2]
                newPeice = [found + 1, found + 2, found + shape[0] + 1, found + 2 * shape[0] + 1]
                newOrientation = 3
            elif currentOrientation == 3:
                oldPeice = [found + shape[0], found, found + 1, found + 2 * shape[0]]
                if found % 10 == 0:
                    found += 1
                newPeice = [found + 2 * shape[0] + 1, found + shape[0] + 1, found + shape[0],
                            found + shape[0] - 1]
                newOrientation = 0
        elif currentTetronome == 2:
            if currentOrientation == 0:
                oldPeice = [found, found + 1, found + 2, found + 1 + shape[0]]
                newPeice = [found, found + 1, found + 1 + shape[0], found - shape[0] + 1]
                newOrientation = 1
            elif currentOrientation == 1:
                oldPeice = [found, found + shape[0], found + shape[0] - 1, found + 2 * shape[0]]
                if found % 10 == 9:
                    found -= 1
                newPeice = [found, found + shape[0], found + shape[0] - 1, found + shape[0] + 1]
                newOrientation = 2
            elif currentOrientation == 2:
                oldPeice = [found, found + shape[0], found + shape[0] - 1, found + 1 + shape[0]]
                newPeice = [found, found + shape[0], found + 1 + shape[0], found + 2 * shape[0]]
                newOrientation = 3
            elif currentOrientation == 3:
                oldPeice = [found, found + shape[0], found + 2 * shape[0], found + shape[0] + 1]
                if found % 10 == 0:
                    found += 1
                newPeice = [found + shape[0], found + shape[0] - 1, found + shape[0] + 1,
                            found + 2 * shape[0]]
                newOrientation = 0
        elif currentTetronome == 3:
            if currentOrientation == 0:
                oldPeice = [found, found + 1, found + shape[0], found + shape[0] - 1]
                newPeice = [found - shape[0], found, found + 1, found + shape[0] + 1]
                newOrientation = 1
            elif currentOrientation == 1:
                oldPeice = [found, found + shape[0], found + shape[0] + 1, found + 2 * shape[0] + 1]
                if found % 10 == 0:
                    found += 1
                newPeice = [found + shape[0], found + shape[0] + 1, found + 2 * shape[0],
                            found + 2 * shape[0] - 1]
                newOrientation = 0
        elif currentTetronome == 4:
            if currentOrientation == 0:
                oldPeice = [found, found + 1, found + shape[0] + 1, found + shape[0] + 2]
                newPeice = [found - shape[0] + 2, found + 2, found + 1, found + shape[0] + 1]
                newOrientation = 1
            elif currentOrientation == 1:
                oldPeice = [found, found + shape[0], found + shape[0] - 1, found + 2 * shape[0] - 1]
                if found % 10 == 1:
                    found += 1
                newPeice = [found + shape[0] - 2, found + shape[0] - 1, found + 2 * shape[0] - 1,
                            found + 2 * shape[0]]
                newOrientation = 0
        elif currentTetronome == 5:
            if currentOrientation == 0:
                newPeice = [found - shape[0] * 2 + 2, found - shape[0] + 2, found + 2,
                            found + 2 + shape[0]]
                oldPeice = [found, found + 1, found + 2, found + 3]
                newOrientation = 1
            elif currentOrientation == 1:
                newPeice = [found + (2 * shape[0]) - 2, found + (2 * shape[0]) - 1,
                            found + (2 * shape[0]), found + (2 * shape[0]) + 1]
                oldPeice = [found, found + shape[0], found + 2 * shape[0], found + 3 * shape[0]]
                newOrientation = 0
                # edge case :
                if found % 10 == 0:  # first column
                    newPeice = [found + (2 * shape[0]) + 3, found + (2 * shape[0]) + 1,
                                found + (2 * shape[0]) + 2, found + (2 * shape[0])]
                elif found % 10 == 9:  # last column
                    newPeice = [found + (2 * shape[0]) - 3, found + (2 * shape[0]) - 2,
                                found + (2 * shape[0]) - 1, found + (2 * shape[0])]
        elif currentTetronome == 6:
            ret = False

        if ret:
            for i in range(4):
                if board[newPeice[i]] == 2:
                    ret = False
            if ret:
                for i in range(4):
                    board[oldPeice[i]] = 0
                for i in range(4):
                    board[newPeice[i]] = 1
                currentOrientation = newOrientation
        return ret , currentOrientation , board



    def Move(self, direction):
        print(direction)
        self.board = DisplayAbstraction.MoveAbsolute(self.board,direction,self.shape)
    @staticmethod
    def MoveAbsolute(board, direction,shape):
        board = copy.deepcopy(board) # deepcopy board. No mutators allowed
        if direction == "Down":
            for x in range(shape[0]):
                for y in range(shape[1] - 1, -1, -1):
                    if board[x + y * shape[0]] == 1:
                        board[x + (y + 1) * shape[0]], board[x + y * shape[0]] = 1, 0
        elif direction == "Right":
            for x in range(shape[0] - 1, -1, -1):
                for y in range(shape[1]):
                    if board[x + y * shape[0]] == 1:
                        board[x + 1 + y * shape[0]], board[x + y * shape[0]] = 1, 0
        elif direction == "Left":
            for x in range(shape[0]):
                for y in range(shape[1]):
                    if board[x + y * shape[0]] == 1:
                        board[x - 1 + y * shape[0]], board[x + y * shape[0]] = 1, 0
        return board
    def SpawnATetronome(self):
        if len(self.spawnBag) == 0:
            self.spawnBag = [i for i in range(7)]
            self.spawnBag.append(random.randint(0, 6))
            random.shuffle(self.spawnBag)
        self.currentTetronome = self.spawnBag.pop(0)
        self.currentOrientation = 0
        for i in self.tetronomeShape[self.currentTetronome]:
            if self.board[i] == 2:
                print("Game Over")
                pygame.quit()
                quit()
            self.board[i] = 1
        self.notify()  # notify observer

    def draw(self):
        for x in range(self.shape[0]):
            for y in range(self.shape[1]):
                if self.board[x + y * self.shape[0]] == 1:
                    colour = DisplayAbstraction.currentcolour
                elif self.board[x + y * self.shape[0]] == 2:
                    colour = DisplayAbstraction.placedcolour
                else:
                    colour = DisplayAbstraction.white
                pygame.draw.rect(self.screen, colour, (x * 50, (y - 2) * 50, x * 50 + 50, (y - 2) * 50 + 50))

                # hold
        pygame.draw.rect(self.screen, (0, 0, 0), (500, 0, 800, 1000))
        pygame.draw.rect(self.screen, (255, 255, 255), (550, 200, 200, 300))

        myfont = pygame.font.SysFont("monospace", 20)
        label = myfont.render("HOLD", 1, (0, 0, 0))
        self.screen.blit(label, (625, 200))

        if self.hold != None:
            for i in self.tetronomeShape[self.hold]:
                if self.hold == 5:  # SPECIAL FOR LINE
                    pygame.draw.rect(self.screen, DisplayAbstraction.currentcolour, (550 + (50 * (i - 3)), 300, 50, 50))
                elif i // 10 == 0:
                    pygame.draw.rect(self.screen, DisplayAbstraction.currentcolour, (575 + (50 * (i - 4)), 300, 50, 50))
                else:
                    pygame.draw.rect(self.screen, DisplayAbstraction.currentcolour, (575 + (50 * (i - 14)), 350, 50, 50))
        label = myfont.render(f"SCORE : {self.score}", 1, (0, 255, 0))
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
            self.score += 40
        if len(fullrows) == 2:
            self.score += 100
        if len(fullrows) == 3:
            self.score += 300
        if len(fullrows) == 4:
            self.score += 1200
        if len(fullrows) != 0:
            print(f'The score is {self.score}')
        for i in fullrows[::-1]:
            self.deleterow(i)

    @staticmethod
    def checkRowsAbsolute(board,shape):
        fullrows = []
        for i in range(shape[1] - 1, -1, -1):
            full = True
            for j in range(shape[0]):
                if board[j + i * shape[0]] != 2:
                    full = False
            if full:
                fullrows.append(i)
        return len(fullrows)

    def deleterow(self, row):
        for row in range(row, 0, -1):
            for column in range(self.shape[0]):
                self.board[column + row * self.shape[0]] = self.board[column + (row - 1) * self.shape[0]]
        for column in range(self.shape[0]):
            self.board[column] = 0

    def run(self):
        self.SpawnATetronome()  # spawn first block
        counter = 0
        while (True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    self.Keypress(event.dict)
            if pygame.time.get_ticks() % (1000 // self.tickrate) == 0:
                counter += 1
                if counter == (1000 // self.tickrate):
                    # print(counter)
                    counter = 0
                    # print(time.time())
                if counter == 5:
                    self.MoveCurrentBlockDown()
                    pass
                if self.AI:
                    if len(self.moves) == 0: # all moves used
                        self.Keypress({'scancode': 44}) # swap
                    else:
                        move = self.moves.pop(0)
                        if move == "Up":
                            self.Keypress({'scancode': 82})
                        elif move == "Left":
                            self.Keypress({'scancode': 80})
                        elif move == "Right":
                            self.Keypress({'scancode': 79})
                        elif move == "Down":
                            self.Keypress({'scancode': 81})


                self.draw()
                # print(counter)
            pygame.display.flip()

            self.clock.tick(self.tickrate)


def main():
    dis = DisplayAbstraction()
    dis.run()


if __name__ == "__main__":
    main()
