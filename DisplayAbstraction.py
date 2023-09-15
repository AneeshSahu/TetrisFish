import tkinter as tk


class DisplayAbstraction(tk.Tk):
    def __init__(self):
        super().__init__()
        self.canvas = tk.Canvas(self, width=500, height=1000)
        self.canvas.pack()
        self.shape = (10, 22)
        self.board = [0 for i in range(self.shape[0] * self.shape[1])]
        self.objects = None
        self.counter = 0 # counts up to a second in ticks
        # self.draw_rectangle()

        self.setup()

    def setup(self):
        self.board[0] = 1

        self.bind("<Right>", self.Keypress)
        self.bind("<Left>", self.Keypress)
        self.bind("<Up>", self.Keypress)
        self.bind("<Down>", self.Keypress)

        self.tick()

    def draw_rectangle(self, x1, x2, y1, y2):
        self.objects = self.canvas.create_rectangle(x1, y2, x1, y2, outline="black", fill="red")

    # def delete_rectangle(self,event):
    #   self.canvas.delete(self.objects[-1])
    #   self.objects.pop()
    def Keypress(self, event):
        found = self.board.index(1)
        if event == "<Down>" or event.keycode == 40 :  # Down
            self.board[found + self.shape[0] ], self.board [found] = 1, 0
        elif event.keycode == 39:  # Right
            self.board[found + 1 ], self.board [found] = 1, 0
            #self.canvas.move(self.objects, 50, 0)
        elif event.keycode == 37:  # Left
            self.board[found - 1 ], self.board [found] = 1, 0
        elif event.keycode == 38:  # Up
            self.board[found - self.shape[0] ], self.board [found] = 1, 0

    def tick(self):
        self.counter += 1
        if self.counter == 20:
            self.counter = 0
        if self.counter % 10 ==0:
            self.Keypress("<Down>");
        self.draw()
        self.after(50, self.tick)
    def draw(self):
        for x in range(self.shape[0]):
            for y in range(self.shape[1]):
                if self.board[x + y * self.shape[0]] == 1:
                    colour = "red"
                else:
                    colour = "white"
                self.canvas.create_rectangle(x * 50, (y-2) * 50, x * 50 + 50, (y-2) * 50 + 50, outline="black", fill=colour)

    def start(self):
        self.mainloop()



dis = DisplayAbstraction()
dis.start()
