import tkinter as tk

WIDTH, HEIGHT = 800, 500
FPS = 60


class Game:
    def __init__(self, root):
        self.root = root
        root.title("Ping Pong")
        root.resizable(False, False)
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black", highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_line(WIDTH // 2, 0, WIDTH // 2, HEIGHT, fill="gray", dash=(8, 8))

    def update(self):
        pass

    def loop(self):
        self.update()
        self.root.after(1000 // FPS, self.loop)


if __name__ == "__main__":
    root = tk.Tk()
    Game(root).loop()
    root.mainloop()
