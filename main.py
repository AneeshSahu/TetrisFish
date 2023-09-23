

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
        self.dis.register(self)

    def update(self):
        print(f"Spawn {self.dis.currentTetronome}")

    def run(self):
        self.dis.run()

t = Tetrisfish()
t.run()