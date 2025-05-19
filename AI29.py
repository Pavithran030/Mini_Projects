import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import random
import time
from PIL import Image, ImageTk

class SudokuSolver:
    def __init__(self):
        # Initialize the main window
        self.window = ctk.CTk()
        self.window.title("Sudoku Solver")
        self.window.geometry("700x750")
        self.window.resizable(False, False)
        ctk.set_appearance_mode("dark")
        
        # Create main container frame
        self.main_container = ctk.CTkFrame(self.window)
        self.main_container.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.main_container,
            text="AI Sudoku Solver",
            font=("Helvetica", 24, "bold")
        )
        self.title_label.pack(pady=10)
        
        # Create the grid cells
        self.cells = {}
        self.create_board()
        
        # Create buttons and additional controls
        self.create_controls()
        
        # Initialize AI parameters
        self.solving_speed = 0.1
        self.show_steps = True
        
    def create_board(self):
        # Create container for board and controls
        board_section = ctk.CTkFrame(
            self.main_container,
            fg_color="transparent"
        )
        board_section.pack(pady=10)
        
        # Create a frame for the Sudoku grid with border
        board_container = ctk.CTkFrame(
            board_section,
            fg_color="#2B2B2B",
            border_width=2,
            border_color="#3E3E3E",
            corner_radius=15
        )
        board_container.grid(row=0, column=0, padx=(0, 20))
        
        # Create right side control panel
        control_panel = ctk.CTkFrame(
            board_section,
            fg_color="#2B2B2B",
            corner_radius=10
        )
        control_panel.grid(row=0, column=1, sticky="n")
        
        # AI Speed label and slider (vertical)
        speed_label = ctk.CTkLabel(
            control_panel,
            text="AI Speed",
            font=('Helvetica', 14)
        )
        speed_label.pack(pady=(10, 5))
        
        self.speed_slider = ctk.CTkSlider(
            control_panel,
            from_=0.01,
            to=1.0,
            command=self.update_speed,
            orientation="vertical",
            height=200,
            width=20
        )
        self.speed_slider.set(0.1)
        self.speed_slider.pack(pady=10)
        
        # Show steps checkbox below the slider
        self.show_steps_var = tk.BooleanVar(value=True)
        show_steps_cb = ctk.CTkCheckBox(
            control_panel,
            text="Show AI Steps",
            variable=self.show_steps_var,
            font=('Helvetica', 14),
            checkbox_width=24,
            checkbox_height=24
        )
        show_steps_cb.pack(pady=(10, 20))
        
        # Create 3x3 box frames
        for box_row in range(3):
            for box_col in range(3):
                box_frame = ctk.CTkFrame(
                    board_container,
                    fg_color=("#1E1E1E" if (box_row + box_col) % 2 == 0 else "#2B2B2B")
                )
                box_frame.grid(row=box_row, column=box_col, padx=2, pady=2)
                
                # Create cells within each box
                for i in range(3):
                    for j in range(3):
                        cell_row = box_row * 3 + i
                        cell_col = box_col * 3 + j
                        cell = ctk.CTkEntry(
                            box_frame,
                            width=45,
                            height=45,
                            justify='center',
                            font=('Arial', 20),
                            fg_color="transparent",
                            border_color="#666666",
                            border_width=1
                        )
                        cell.grid(row=i, column=j, padx=1, pady=1)
                        self.cells[(cell_row, cell_col)] = cell
        
        # Add generate button below the grid
        generate_button = ctk.CTkButton(
            board_section,
            text="New Puzzle",
            command=self.generate_puzzle,
            width=150,
            height=40,
            font=('Helvetica', 16, "bold"),
            fg_color="#FFA500",
            hover_color="#FF8C00",
            corner_radius=10
        )
        generate_button.grid(row=1, column=0, columnspan=2, pady=(10, 0))

    def create_controls(self):
        # Button frame
        button_frame = ctk.CTkFrame(self.main_container)
        button_frame.pack(pady=10)
        
        # First row of buttons
        solve_button = ctk.CTkButton(
            button_frame,
            text="Solve with AI",
            command=self.solve_button_clicked,
            width=150,
            height=40,
            font=('Helvetica', 16, "bold"),
            fg_color="#2FA4FF",
            hover_color="#1B8AD4",
            corner_radius=10
        )
        solve_button.grid(row=0, column=0, padx=8, pady=3)
        
        hint_button = ctk.CTkButton(
            button_frame,
            text="Get Hint",
            command=self.get_hint,
            width=150,
            height=40,
            font=('Helvetica', 16, "bold"),
            fg_color="#28C76F",
            hover_color="#1EA55D",
            corner_radius=10
        )
        hint_button.grid(row=0, column=1, padx=8, pady=3)
        
        clear_button = ctk.CTkButton(
            button_frame,
            text="Clear",
            command=self.clear_board,
            width=150,
            height=40,
            font=('Helvetica', 16, "bold"),
            fg_color="#FF5C5C",
            hover_color="#D14545",
            corner_radius=10
        )
        clear_button.grid(row=0, column=2, padx=8, pady=3)
        
        check_button = ctk.CTkButton(
            button_frame,
            text="Check Progress",
            command=self.check_progress,
            width=150,
            height=40,
            font=('Helvetica', 16, "bold"),
            fg_color="#9B59B6",
            hover_color="#8E44AD",
            corner_radius=10
        )
        check_button.grid(row=0, column=3, padx=8, pady=3)
        
        # Progress label
        self.progress_label = ctk.CTkLabel(
            button_frame,
            text="Progress: 0%",
            font=('Helvetica', 14)
        )
        self.progress_label.grid(row=0, column=4, columnspan=2, pady=3)
        
    def check_progress(self):
        """Check the current progress and show percentage of correctness"""
        current_board = self.get_board()
        if current_board is None:
            return
            
        # Create a solved board for comparison
        solved_board = [row[:] for row in current_board]
        if not self.solve_sudoku(solved_board):
            messagebox.showerror("Error", "Current configuration has no valid solution!")
            return
            
        # Count correct cells and calculate percentage
        total_filled = 0
        correct_cells = 0
        
        for i in range(9):
            for j in range(9):
                if current_board[i][j] != 0:
                    total_filled += 1
                    if current_board[i][j] == solved_board[i][j]:
                        correct_cells += 1
                        self.cells[(i, j)].configure(text_color="#28C76F")  # Correct cells in green
                    else:
                        self.cells[(i, j)].configure(text_color="#FF5C5C")  # Wrong cells in red
                        
        if total_filled == 0:
            percentage = 0
        else:
            percentage = (correct_cells / total_filled) * 100
            
        # Update progress label
        self.progress_label.configure(
            text=f"Progress: {percentage:.1f}% ({correct_cells}/{total_filled} correct)"
        )
        
        # Show appropriate message
        if percentage == 100 and total_filled == 81:
            messagebox.showinfo("Congratulations!", "Puzzle solved correctly!")
        elif percentage == 100:
            messagebox.showinfo("Great!", "All filled numbers are correct!")
        elif total_filled == 0:
            messagebox.showinfo("Empty Board", "Please fill some numbers first!")

    def get_hint(self):
        """Provide a hint by filling in one correct number"""
        board = self.get_board()
        if board is None:
            return
            
        # Find an empty cell
        empty = self.find_empty(board)
        if not empty:
            messagebox.showinfo("Hint", "The puzzle is already complete!")
            return
            
        # Try to solve the puzzle to get the correct number
        temp_board = [row[:] for row in board]
        if self.solve_sudoku(temp_board):
            row, col = empty
            hint_value = temp_board[row][col]
            self.cells[(row, col)].delete(0, tk.END)
            self.cells[(row, col)].insert(0, str(hint_value))
            self.cells[(row, col)].configure(text_color="#28C76F")  # Green color for hints
        else:
            messagebox.showerror("Error", "This puzzle has no solution!")

    def update_speed(self, value):
        self.solving_speed = value
        
    def generate_puzzle(self):
        # Generate a random valid Sudoku puzzle
        board = [[0 for _ in range(9)] for _ in range(9)]
        self.solve_sudoku(board)  # Generate a complete solution
        
        # Remove numbers randomly to create puzzle
        cells_to_remove = random.randint(40, 50)  # Keep 30-40 numbers
        for _ in range(cells_to_remove):
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            while board[row][col] == 0:
                row = random.randint(0, 8)
                col = random.randint(0, 8)
            board[row][col] = 0
            
        # Display the generated puzzle
        self.display_solution(board)
        
    def solve_button_clicked(self):
        board = self.get_board()
        if board is None:
            return
            
        if self.show_steps_var.get():
            self.window.after(0, lambda: self.solve_with_visualization(board))
        else:
            if self.solve_sudoku(board):
                self.display_solution(board)
            else:
                messagebox.showerror("Error", "No solution exists!")
                
    def solve_with_visualization(self, board):
        empty = self.find_empty(board)
        if not empty:
            return True
            
        row, col = empty
        for num in range(1, 10):
            if self.is_valid(board, row, col, num):
                board[row][col] = num
                self.cells[(row, col)].delete(0, tk.END)
                self.cells[(row, col)].insert(0, str(num))
                self.window.update()
                time.sleep(self.solving_speed)
                
                if self.solve_with_visualization(board):
                    return True
                    
                board[row][col] = 0
                self.cells[(row, col)].delete(0, tk.END)
                self.window.update()
                time.sleep(self.solving_speed)
                
        return False
        
    def get_board(self):
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                value = self.cells[(i, j)].get()
                if value == '':
                    row.append(0)
                else:
                    try:
                        num = int(value)
                        if num < 1 or num > 9:
                            messagebox.showerror("Error", "Please enter numbers between 1 and 9 only!")
                            return None
                        row.append(num)
                    except ValueError:
                        messagebox.showerror("Error", "Please enter valid numbers!")
                        return None
            board.append(row)
        return board
        
    def display_solution(self, board):
        for i in range(9):
            for j in range(9):
                self.cells[(i, j)].delete(0, tk.END)
                self.cells[(i, j)].insert(0, str(board[i][j]) if board[i][j] != 0 else '')
                
    def clear_board(self):
        for cell in self.cells.values():
            cell.delete(0, tk.END)
            
    def is_valid(self, board, row, col, num):
        # Check row
        for x in range(9):
            if board[row][x] == num:
                return False
        
        # Check column
        for x in range(9):
            if board[x][col] == num:
                return False
        
        # Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == num:
                    return False
        return True
        
    def solve_sudoku(self, board):
        empty = self.find_empty(board)
        if not empty:
            return True
            
        row, col = empty
        for num in range(1, 10):
            if self.is_valid(board, row, col, num):
                board[row][col] = num
                if self.solve_sudoku(board):
                    return True
                board[row][col] = 0
        return False
        
    def find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = SudokuSolver()
    app.run()
