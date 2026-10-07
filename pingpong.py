import random
import tkinter as tk

WIDTH, HEIGHT = 800, 500
FPS = 60
PADDLE_W, PADDLE_H = 12, 90
PADDLE_SPEED = 7
MARGIN = 20
BALL_SIZE = 14
BALL_SPEED = 6


class Game:
    def __init__(self, root):
        self.root = root
        root.title("Ping Pong")
        root.resizable(False, False)
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black", highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_line(WIDTH // 2, 0, WIDTH // 2, HEIGHT, fill="gray", dash=(8, 8))

        # Raquetes: esquerda (W/S) e direita (setas)
        top = (HEIGHT - PADDLE_H) // 2
        self.left = self.canvas.create_rectangle(
            MARGIN, top, MARGIN + PADDLE_W, top + PADDLE_H, fill="white")
        self.right = self.canvas.create_rectangle(
            WIDTH - MARGIN - PADDLE_W, top, WIDTH - MARGIN, top + PADDLE_H, fill="white")

        self.ball = self.canvas.create_oval(0, 0, BALL_SIZE, BALL_SIZE, fill="white")
        self.reset_ball()

        self.keys = set()
        root.bind("<KeyPress>", lambda e: self.keys.add(e.keysym.lower()))
        root.bind("<KeyRelease>", lambda e: self.keys.discard(e.keysym.lower()))

    def reset_ball(self):
        cx, cy = (WIDTH - BALL_SIZE) // 2, (HEIGHT - BALL_SIZE) // 2
        self.canvas.coords(self.ball, cx, cy, cx + BALL_SIZE, cy + BALL_SIZE)
        self.vx = random.choice((-1, 1)) * BALL_SPEED
        self.vy = random.choice((-1, 1)) * random.randint(2, 4)

    def move_ball(self):
        self.canvas.move(self.ball, self.vx, self.vy)
        _, y1, _, y2 = self.canvas.coords(self.ball)
        if y1 <= 0 or y2 >= HEIGHT:
            self.vy = -self.vy

    def move_paddle(self, paddle, dy):
        _, y1, _, y2 = self.canvas.coords(paddle)
        dy = max(-y1, min(dy, HEIGHT - y2))
        self.canvas.move(paddle, 0, dy)

    def update(self):
        self.move_paddle(self.left, PADDLE_SPEED * (("s" in self.keys) - ("w" in self.keys)))
        self.move_paddle(self.right, PADDLE_SPEED * (("down" in self.keys) - ("up" in self.keys)))

    def loop(self):
        self.update()
        self.root.after(1000 // FPS, self.loop)


if __name__ == "__main__":
    root = tk.Tk()
    Game(root).loop()
    root.mainloop()
