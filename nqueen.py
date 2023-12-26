import tkinter as tk

class NQueensGUI:
    def __init__(self, root, n):
        self.root = root
        self.n = n
        self.board = [[0] * n for _ in range(n)]
        self.current_solution = 0

        self.window_width = root.winfo_screenwidth()  # Set to screen width
        self.window_height = root.winfo_screenheight()  # Set to screen height

        # Left side (N-Queens problem visualization)
        self.left_frame = tk.Frame(root, width=self.window_width // 2, height=self.window_height)
        self.left_frame.pack(side=tk.LEFT, padx=5)

        self.square_size = min(self.window_width // (2 * n), self.window_height // n)
        self.canvas = tk.Canvas(self.left_frame, width=self.square_size * n, height=self.square_size * n)
        self.canvas.pack()

        self.speed_label = tk.Label(self.left_frame, text="Speed:")
        self.speed_label.pack()

        self.speed_var = tk.IntVar()
        self.speed_scale = tk.Scale(
            self.left_frame, variable=self.speed_var, from_=1, to=10, orient=tk.HORIZONTAL
        )
        self.speed_scale.pack()

        # Right side (Explanation and Notes)
        self.right_frame = tk.Frame(root, width=self.window_width // 2, height=self.window_height, bg="#334d40")
        self.right_frame.pack(side=tk.RIGHT, padx=5)

        self.explanation_label = tk.Label(self.right_frame, text="Explanation:", font=("Helvetica", 40), bg="#334d40", fg="red")
        self.explanation_label.pack()

        self.explanation_text = tk.Text(self.right_frame, height=5, width=40, font=("Helvetica", 42), bg="#334d40", fg="red", bd=2, relief="solid")
        self.explanation_text.pack()

        self.notes_label = tk.Label(self.right_frame, text="Notes:", font=("Helvetica", 44), bg="#334d40", fg="red")
        self.notes_label.pack()

        self.notes_text = tk.Text(self.right_frame, height=10, width=40, font=("Helvetica", 42), bg="#334d40", fg="red", bd=2, relief="solid")
        self.notes_text.pack()

        # Automatically start the solving process
        self.start_n_queens()

    def draw_board(self):
        self.canvas.delete("all")

        for i in range(self.n):
            for j in range(self.n):
                x0, y0 = j * self.square_size, i * self.square_size
                x1, y1 = x0 + self.square_size, y0 + self.square_size

                color = "white" if (i + j) % 2 == 0 else "black"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

                if self.board[i][j] == 1:
                    self.canvas.create_text(
                        x0 + self.square_size // 2,
                        y0 + self.square_size // 2,
                        text="\u265B",  # Unicode for a chess queen
                        font=("Helvetica", self.square_size // 2),
                        fill="red",
                    )

    def update_explanation(self, text):
        self.explanation_text.delete(1.0, tk.END)  # Clear previous text
        self.explanation_text.insert(tk.END, text)

    def update_notes(self, text):
        self.notes_text.delete(1.0, tk.END)  # Clear previous text
        self.notes_text.insert(tk.END, text)

    def is_safe(self, row, col):
        for i in range(row):
            if self.board[i][col] == 1:
                return False

            if col - (row - i) >= 0 and self.board[i][col - (row - i)] == 1:
                return False

            if col + (row - i) < self.n and self.board[i][col + (row - i)] == 1:
                return False

        return True

    def solve_n_queens_util(self, row):
        if row == self.n:
            self.current_solution += 1
            self.draw_board()
            self.root.update()
            self.root.after(self.speed_var.get() * 100)  # Delay based on speed
            explanation = f"Solution {self.current_solution}: Queens placed successfully."
            self.update_explanation(explanation)
            return

        for col in range(self.n):
            if self.is_safe(row, col):
                self.board[row][col] = 1
                self.draw_board()
                self.root.update()
                self.root.after(self.speed_var.get() * 100)  # Delay based on speed
                explanation = f"Placing queen in row {row + 1}, column {col + 1}."
                self.update_explanation(explanation)
                self.solve_n_queens_util(row + 1)
                self.board[row][col] = 0
                self.draw_board()
                self.root.update()
                self.root.after(self.speed_var.get() * 100)  # Delay based on speed

    def start_n_queens(self):
        self.current_solution = 0
        self.board = [[0] * self.n for _ in range(self.n)]
        self.draw_board()
        self.root.update()
        self.root.after(500)  # Initial delay
        self.solve_n_queens_util(0)

if __name__ == "__main__":
    n = 8  # Change this to the desired board size
    root = tk.Tk()
    root.title(f"{n}-Queens Problem")
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")  # Set to full screen
    gui = NQueensGUI(root, n)
    root.mainloop()
