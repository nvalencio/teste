import random
import tkinter as tk

WIDTH, HEIGHT = 800, 500
FPS = 60
PADDLE_W, PADDLE_H = 12, 90
PADDLE_SPEED = 7
MARGIN = 20
BALL_SIZE = 14
BALL_SPEED = 6
WIN_SCORE = 7
MAX_BALL_SPEED = 16


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

        self.score = [0, 0]
        self.over = False
        self.score_text = self.canvas.create_text(
            WIDTH // 2, 40, text="0   0", fill="white", font=("Courier", 32, "bold"))
        self.message = self.canvas.create_text(
            WIDTH // 2, HEIGHT // 2, text="", fill="yellow", font=("Courier", 24, "bold"))

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
        x1, y1, x2, y2 = self.canvas.coords(self.ball)
        if y1 <= 0:
            self.vy = abs(self.vy)
        elif y2 >= HEIGHT:
            self.vy = -abs(self.vy)
        if x2 < 0:
            self.point(1)
            return
        if x1 > WIDTH:
            self.point(0)
            return
        self.bounce_off(self.left, going_left=True)
        self.bounce_off(self.right, going_left=False)

    def point(self, player):
        self.score[player] += 1
        self.canvas.itemconfig(self.score_text, text=f"{self.score[0]}   {self.score[1]}")
        if self.score[player] >= WIN_SCORE:
            self.over = True
            side = "ESQUERDO" if player == 0 else "DIREITO"
            self.canvas.itemconfig(
                self.message, text=f"Jogador {side} venceu!\nPressione R para reiniciar")
        else:
            self.reset_ball()

    def restart(self):
        self.score = [0, 0]
        self.over = False
        self.canvas.itemconfig(self.score_text, text="0   0")
        self.canvas.itemconfig(self.message, text="")
        self.reset_ball()

    def bounce_off(self, paddle, going_left):
        """Rebate a bola na raquete; o ângulo depende de onde ela bate."""
        if (self.vx < 0) != going_left:
            return
        bx1, by1, bx2, by2 = self.canvas.coords(self.ball)
        px1, py1, px2, py2 = self.canvas.coords(paddle)
        if bx2 >= px1 and bx1 <= px2 and by2 >= py1 and by1 <= py2:
            offset = ((by1 + by2) / 2 - (py1 + py2) / 2) / (PADDLE_H / 2)
            speed = min(abs(self.vx) * 1.05, MAX_BALL_SPEED)  # acelera a cada rebatida
            self.vx = speed if going_left else -speed
            self.vy = offset * BALL_SPEED

    def move_paddle(self, paddle, dy):
        _, y1, _, y2 = self.canvas.coords(paddle)
        dy = max(-y1, min(dy, HEIGHT - y2))
        self.canvas.move(paddle, 0, dy)

    def update(self):
        self.move_paddle(self.left, PADDLE_SPEED * (("s" in self.keys) - ("w" in self.keys)))
        self.move_paddle(self.right, PADDLE_SPEED * (("down" in self.keys) - ("up" in self.keys)))
        if self.over:
            if "r" in self.keys:
                self.restart()
            return
        self.move_ball()

    def loop(self):
        self.update()
        self.root.after(1000 // FPS, self.loop)


if __name__ == "__main__":
    root = tk.Tk()
    Game(root).loop()
    root.mainloop()
