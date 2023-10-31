import copy

import DisplayAbstraction



class observer:
    def __init__(self):
        pass
    def update(self):
        pass


class Tetrisfish(observer):
    def __init__(self):
        super().__init__()
        self.dis = DisplayAbstraction.DisplayAbstraction()
        self.dis.AI = True
        self.dis.register(self)

    @staticmethod
    def count_holes_and_max_height(tetris_board):
        tetris_grid = [tetris_board[i:i + 10] for i in range(0, len(tetris_board), 10)]

        # Initialize hole count and maximum height
        hole_count = 0
        max_height = 0

        # Iterate through the rows from bottom to top
        for i in range(len(tetris_grid) - 1, 0, -1):
            for j in range(10):
                # Check for an empty space (0) surrounded by placed blocks (2)
                if tetris_grid[i][j] == 0:
                    # Check if the space is surrounded by placed blocks
                    if (i < len(tetris_grid) - 1 and tetris_grid[i + 1][j] == 2) and \
                      ((j > 0 and tetris_grid[i][j - 1] == 2) or (j < 9 and tetris_grid[i][j + 1] == 2)):
                        hole_count += 1
                elif tetris_grid[i][j] == 2:
                    # Update the maximum height of placed blocks
                    max_height = max(max_height, len(tetris_grid) - i)
        #print(hole_count,max_height)
        return hole_count, max_height
    @staticmethod
    def count_covered_holed(tetris_board):
        count = 0
        for i in range (10):
            rowcap = False
            for j in range(22):
                if tetris_board[j*10+i] == 2 and not rowcap:
                    rowcap = True
                elif tetris_board[j*10+i] == 0 and rowcap:
                    count += 1
        return count

    def generateAllPosibilities(self):
        boards = []
        origin = self.dis.board
        shape = self.dis.shape
        cur = copy.deepcopy(origin)
        cur = self.dis.MoveAbsolute(cur, "Down", shape)
        # all possible moves. no rotations :
        move = "Left"

        # {0: "L", 1: "J", 2: "T", 3: "S" , 4: "Z", 5 : "I", 6: "O"}
        # tetronomeShape = (
        #         (4, 5, 6, 14), (4, 5, 6, 16), (4, 5, 6, 15), (5, 6, 14, 15), (4, 5, 15, 16), (3, 4, 5, 6), (4, 5, 14, 15))
        if self.dis.currentTetronome == 0:
            moveLeft = 4
            moveRight = 8
        elif self.dis.currentTetronome == 1:
            moveLeft = 4
            moveRight = 8
        elif self.dis.currentTetronome == 2:
            moveLeft = 4
            moveRight = 8
        elif self.dis.currentTetronome == 3:
            moveLeft = 4
            moveRight = 8
        elif self.dis.currentTetronome == 4:
            moveLeft = 4
            moveRight = 8
        elif self.dis.currentTetronome == 5:
            cur = self.dis.MoveAbsolute(cur, "Down", shape)
            cur = self.dis.RotateAbsolute(cur, self.dis.currentTetronome, 0, shape)[2]
            moveLeft = 3
            moveRight = 7
        else : #self.dis.currentTetronome == 6:
            moveLeft = 4
            moveRight = 9

        path = []
        for i in range(moveLeft): # move as left as possible
            cur = self.dis.MoveAbsolute(cur,move,shape)
            path.append(move)
            #print_colored_2d_array(cur)
            #print()

        move = "Right"
        for i in range(moveRight): # move as right as possible while generating moves
            if self.dis.currentTetronome in [0, 1, 2]:
                for j in range(4):
                    cur = self.dis.RotateAbsolute(cur, self.dis.currentTetronome, j, shape)[2]
                    #print_colored_2d_array(cur)
                    #print("move rotate")
                    path.append("Up")
                    boards.append((cur,norm(path,self.dis.currentTetronome)))
            elif self.dis.currentTetronome in [3, 4,5]:
                for j in range(2):
                    cur = self.dis.RotateAbsolute(cur, self.dis.currentTetronome, j if self.dis.currentTetronome in [3,4] else 1-j, shape)[2]
                    #print_colored_2d_array(cur)
                    path.append("Up")
                    boards.append((cur,norm(path,self.dis.currentTetronome)))
            else:  # 6
                #print_colored_2d_array(cur)

                boards.append((cur,norm(path,self.dis.currentTetronome)))

            #print("move right")
            cur = self.dis.MoveAbsolute(cur, move, shape)
            path.append(move)

        return boards
        #print(len(boards))

    def update(self):
        print(f"Spawn {self.dis.currentTetronome}")
        boards = self.generateAllPosibilities()
        results = self.generateAllEndStatesAndScores(boards)
        print(results)
        self.dis.moves = results
        #Tetrisfish.count_holes_and_max_height(self.dis.board)

    def run(self):
        self.dis.run()

    def generateAllEndStatesAndScores(self, boards):
        shape = self.dis.shape
        result = []
        bestscore = float("-inf")
        bestpath = None
        for board , path in boards:
                board = self.dis.moveToEndAbsolute(board,shape)
                holes , height = self.count_holes_and_max_height(board)
                row = self.dis.checkRowsAbsolute(board,shape)
                covered = self.count_covered_holed(board)
                score = row*row - covered - height/2
                if score > bestscore:
                    bestscore = score
                    besthoal = holes
                    bestheight = height
                    bestrow = row
                    bestcovered = covered
                    bestpath = path
        print(f"score :{bestscore} , holes {besthoal}, height {bestheight}, row {bestrow} cpvered {bestcovered}")
        return bestpath




def norm(directions, tetronome):
    result = []
    up_count = 0
    right_count = 0
    left_count = 0

    for direction in directions:
        if direction == "Up":
            up_count += 1
            if up_count == 4 and tetronome in [0, 1, 2]:
                up_count = 0
            elif up_count == 2:
                up_count = 0
        elif direction == "Right":
            if left_count > 0:
                left_count -=1
            else:
                right_count += 1
        elif direction == "Left":
            if right_count > 0:
                right_count -=1
            else:
                left_count += 1

    result.append("Down")
    result.append("Down")

    while right_count > 0:
        result.append("Right")
        right_count -= 1
    while left_count > 0:
        result.append("Left")
        left_count -= 1
    while up_count > 0:
        result.append("Up")
        up_count -= 1

    return result
def print_colored_2d_array(arr):
    color_map = {
        0: '\033[91m',  # Red for 0
        1: '\033[92m',  # Green for 1
        2: '\033[94m',  # Blue for 2
        'reset': '\033[0m'  # Reset color to default
    }
    for row in range(22):
        for column in range(10):
            print(color_map[arr[row*10+ column]], arr[row*10 + column], color_map['reset'], end='')
        print()

t = Tetrisfish()
t.run()