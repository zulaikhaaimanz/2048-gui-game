import tkinter as tk
import random

class Game2048Twist:
    def __init__(self, master):
        self.master = master
        self.master.title("2048 Game with a Twist (Opposites Cancel!)")
        self.grid = [[0] * 4 for _ in range(4)]
        self.cells = [[None] * 4 for _ in range(4)]
        self.frame = tk.Frame(master)
        self.frame.pack()
        self.create_grid()
        self.master.bind("<Key>", self.key_handler)
        self.add_random_tile()
        self.add_random_tile()
        self.update_grid()

    def create_grid(self):
        for i in range(4):
            for j in range(4):
                cell = tk.Label(self.frame, text="", width=6, height=3,
                                font=("Helvetica", 24), bg="lightgray", relief="raised")
                cell.grid(row=i, column=j, padx=5, pady=5)
                self.cells[i][j] = cell

    def update_grid(self):
        for i in range(4):
            for j in range(4):
                value = self.grid[i][j]
                self.cells[i][j]['text'] = str(value) if value != 0 else ""
                self.cells[i][j]['bg'] = self.get_color(value)

    def get_color(self, value):
        if value == 0:
            return "lightgray"
        elif value > 0:
            return "lightblue"
        else:
            return "lightcoral"

    def add_random_tile(self):
        empty = [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
        if empty:
            i, j = random.choice(empty)
            # Add positive or negative tile with equal chance
            self.grid[i][j] = random.choice([2, -2])

    def compress_and_merge(self, row):
        new_row = [val for val in row if val != 0]
        i = 0
        while i < len(new_row) - 1:
            a, b = new_row[i], new_row[i + 1]
            if a == b:
                new_row[i] *= 2
                new_row.pop(i + 1)
                new_row.append(0)
            elif a == -b:
                new_row[i] = 0
                new_row.pop(i + 1)
                new_row.append(0)
            i += 1
        return [val for val in new_row if val != 0] + [0] * (4 - len([val for val in new_row if val != 0]))

    def move(self, direction):
        moved = False
        for i in range(4):
            original = []
            if direction in ("Left", "Right"):
                row = self.grid[i][:]
                if direction == "Right":
                    row.reverse()
                new_row = self.compress_and_merge(row)
                if direction == "Right":
                    new_row.reverse()
                if self.grid[i] != new_row:
                    self.grid[i] = new_row
                    moved = True
            else:
                col = [self.grid[j][i] for j in range(4)]
                if direction == "Down":
                    col.reverse()
                new_col = self.compress_and_merge(col)
                if direction == "Down":
                    new_col.reverse()
                for j in range(4):
                    if self.grid[j][i] != new_col[j]:
                        self.grid[j][i] = new_col[j]
                        moved = True
        return moved

    def key_handler(self, event):
        direction_keys = {
            "Up": "Up",
            "Down": "Down",
            "Left": "Left",
            "Right": "Right"
        }
        if event.keysym in direction_keys:
            moved = self.move(direction_keys[event.keysym])
            if moved:
                self.add_random_tile()
                self.update_grid()
                if not self.can_move():
                    self.game_over()

    def can_move(self):
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    return True
                for di, dj in [(0,1),(1,0)]:
                    ni, nj = i+di, j+dj
                    if 0 <= ni < 4 and 0 <= nj < 4:
                        if self.grid[i][j] == self.grid[ni][nj] or self.grid[i][j] == -self.grid[ni][nj]:
                            return True
        return False

    def game_over(self):
        over_label = tk.Label(self.master, text="Game Over!", font=("Helvetica", 32), fg="red")
        over_label.pack()

# Run the Game
if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048Twist(root)
    root.mainloop()