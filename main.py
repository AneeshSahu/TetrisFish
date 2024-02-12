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
    def count_max_height(tetris_board):
        tetris_grid = [tetris_board[i:i + 10] for i in range(0, len(tetris_board), 10)]

        # Initialize hole count and maximum height
        hole_count = 0
        max_height = 0
        for i in range(len(tetris_grid)):
            #print(tetris_grid[i])
            if 2 in tetris_grid[i]:
                max_height = len(tetris_grid) - i
                break

        return max_height

    @staticmethod
    def count_covered_holes(tetris_board):
        tetris_grid = [tetris_board[i:i + 10] for i in range(0, len(tetris_board), 10)]
        count = 0

        for i in range(len(tetris_grid[0])):
            temp = 0
            for j in range(len(tetris_grid)-1, -1,-1):
                if tetris_grid[j][i] == 0:
                    temp += 1
                elif tetris_grid[j][i] == 2:
                    #print(f"{i} is covered, found {temp} holes")
                    count += temp
                    temp = 0
        return count

    def generateAllPosibilities(self):

        # {0: "L", 1: "J", 2: "T", 3: "S" , 4: "Z", 5 : "I", 6: "O"}
        # tetronomeShape = (
        #         (4, 5, 6, 14), (4, 5, 6, 16), (4, 5, 6, 15), (5, 6, 14, 15), (4, 5, 15, 16), (3, 4, 5, 6), (4, 5, 14, 15))

        boards = []
        origin = self.dis.board
        shape = self.dis.shape
        cur = copy.deepcopy(origin)
        if self.dis.currentTetronome in [0,1,2] :
            cur = self.dis.MoveAbsolute(cur, "Down",shape)
            boards.append((cur, "Down"))
            boards.append(
                (DisplayAbstraction.DisplayAbstraction.RotateAbsolute(boards[0][0],self.dis.currentTetronome,0,shape)[2],
                 "Down,Up"))
            boards.append((
                DisplayAbstraction.DisplayAbstraction.RotateAbsolute(boards[1][0], self.dis.currentTetronome, 1, shape)[2],
                "Down,Up,Up"))
            boards.append((
                DisplayAbstraction.DisplayAbstraction.RotateAbsolute(boards[2][0], self.dis.currentTetronome, 2, shape)[2],
                "Down,Up,Up,Up"))
            left = 5
            right = 4
            orientations = 4
        elif self.dis.currentTetronome in [3,4]:
            cur = self.dis.MoveAbsolute(cur, "Down", shape)
            boards.append((cur, "Down"))
            boards.append(
                (DisplayAbstraction.DisplayAbstraction.RotateAbsolute(boards[0][0], self.dis.currentTetronome, 0, shape)[2],
                 "Down,Up"))
            left = 5
            right = 3
            orientations = 2
        elif self.dis.currentTetronome == 5:
            cur = self.dis.MoveAbsolute(cur, "Down", shape)
            cur = self.dis.MoveAbsolute(cur, "Down", shape)
            boards.append((cur, "Down,Down"))
            boards.append(
                (
                DisplayAbstraction.DisplayAbstraction.RotateAbsolute(boards[0][0], self.dis.currentTetronome, 0, shape)[
                    2],
                "Down,Down,Up"))
            left = 5
            right = 4
            orientations = 2
        else:
            boards.append((cur, ""))
            left = 4
            right = 4
            orientations = 1



        for origin,path in boards[:orientations]:
            cur = origin
            curpath = path
            # left
            for j in range(left):
                cur = self.dis.MoveAbsolute(cur, "Left", shape)
                curpath += ",Left"
                boards.append((cur, curpath))
            cur = origin
            curpath = path
            for j in range(right):
                cur = self.dis.MoveAbsolute(cur, "Right", shape)
                curpath += ",Right"
                boards.append((cur,curpath))

        #for i,path in boards:
        #    print_colored_2d_array(i)
        #    print(path)
        return boards
        # print(len(boards))

    def update(self):
        print(f"Spawn {self.dis.currentTetronome}")
        boards = self.generateAllPosibilities()
        results = self.generateAllEndStatesAndScores(boards).split(",")
        if results[0]== "":
            results = results[1:]
        self.dis.moves = results
        # Tetrisfish.count_holes_and_max_height(self.dis.board)

    def run(self):
        self.dis.run()

    def generateAllEndStatesAndScores(self, boards):
        shape = self.dis.shape
        result = []
        bestscore = float("-inf")
        bestpath = None
        bestboard = None
        bestcovered = None
        for board,path in boards:
            board,drop = self.dis.moveToEndAbsolute(board, shape,True)
            #print_colored_2d_array(board)
            height = self.count_max_height(board)
            row = self.dis.checkRowsAbsolute(board, shape)
            covered = self.count_covered_holes(board)
            score = drop - 2*covered #5*(row * row) + 2* drop - height - (3*covered)
            if score > bestscore:
                bestscore = score
                bestheight = height
                bestrow = row
                bestcovered = covered
                bestboard = board
                bestpath = path
        #print(f"score :{bestscore} , height {bestheight}, row {bestrow} cpvered {bestcovered}, path {bestpath}")
        #print_colored_2d_array(bestboard)
        #self.count_covered_holes(bestboard)
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
                left_count -= 1
            else:
                right_count += 1
        elif direction == "Left":
            if right_count > 0:
                right_count -= 1
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
            print(color_map[arr[row * 10 + column]], arr[row * 10 + column], color_map['reset'], end='')
        print()
    print()


t = Tetrisfish()
t.run()
