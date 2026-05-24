# ==============================================================================
# FILE: game_board_window.py
# Game Board Window with ENHANCED INTERACTIVE VALIDATION (BONUS)
# ==============================================================================

"""
Game Board Window Module - Enhanced with BONUS Features
Displays the Sudoku grid with thick lines separating 3x3 boxes.
Handles cell input with REAL-TIME validation and detailed feedback.
Uses CustomTkinter for modern dark mode UI.

BONUS FEATURES:
- Real-time constraint violation checking
- Detailed error messages for each constraint type
- Visual feedback with color coding
- Prevention of modifying initial cells
"""

import customtkinter as ctk
from tkinter import messagebox


class GameBoardWindow:
    """
    Enhanced game board with BONUS interactive validation.
    
    Features:
    - 9x9 grid with thick lines between 3x3 boxes
    - REAL-TIME input validation (BONUS)
    - Detailed constraint violation messages (BONUS)
    - Color-coded feedback (BONUS)
    - Keyboard navigation (arrow keys)
    - Protection of initial cells (BONUS)
    """
    
    def __init__(self, parent, sudoku_csp, callbacks):
        """
        Initialize game board window.
        
        Args:
            parent: Parent CTk widget
            sudoku_csp: SudokuCSP instance
            callbacks: Dictionary of callback functions
        """
        self.sudoku = sudoku_csp
        self.callbacks = callbacks
        self.cells = {}
        
        # Main frame
        self.frame = ctk.CTkFrame(parent, corner_radius=15)
        self.frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.create_board()
    
    def create_board(self):
        """
        Create the 9x9 Sudoku grid with thick 3x3 box separators.
        Uses proper padding to create visual box separation.
        Each cell has distinct highlighting to separate from background.
        """
        
        # Title
        ctk.CTkLabel(
            self.frame,
            text="Sudoku Board",
            font=("Arial", 14, "bold"),
            anchor="center"
        ).pack(pady=10)
        
        # Container for board
        board_container = ctk.CTkFrame(self.frame, corner_radius=10)
        board_container.pack(padx=15, pady=10)
        
        # Grid frame
        grid_frame = ctk.CTkFrame(board_container, fg_color="transparent")
        grid_frame.pack(padx=8, pady=8)
        
        cell_size = 48
        
        for i in range(9):
            for j in range(9):
                # Calculate padding for 3x3 box separation
                padx_left = 4 if j % 3 == 0 else 2
                padx_right = 4 if (j + 1) % 3 == 0 else 2
                pady_top = 4 if i % 3 == 0 else 2
                pady_bottom = 4 if (i + 1) % 3 == 0 else 2
                
                # Alternating box colors with better contrast
                box_color = "#2d2d2d" if (i // 3 + j // 3) % 2 == 0 else "#1f1f1f"
                
                # Entry widget with enhanced highlighting
                entry = ctk.CTkEntry(
                    grid_frame,
                    width=cell_size,
                    height=cell_size,
                    font=("Arial", 20, "bold"),
                    justify="center",
                    corner_radius=6,
                    border_width=2,
                    border_color="#555555",  # Thicker, more visible border
                    fg_color=box_color,
                    text_color="#ffffff"
                )
                
                entry.grid(
                    row=i, 
                    column=j, 
                    padx=(padx_left, padx_right),
                    pady=(pady_top, pady_bottom)
                )
                
                # Bind events
                entry.bind('<KeyRelease>', lambda e, r=i, c=j: self.validate_input(r, c))
                entry.bind('<Key>', lambda e, r=i, c=j: self.handle_key_press(e, r, c))
                
                self.cells[(i, j)] = entry
    
    def handle_key_press(self, event, row, col):
        """
        Handle keyboard navigation with arrow keys.
        """
        key = event.keysym
        
        if key == 'Up' and row > 0:
            self.cells[(row - 1, col)].focus()
        elif key == 'Down' and row < 8:
            self.cells[(row + 1, col)].focus()
        elif key == 'Left' and col > 0:
            self.cells[(row, col - 1)].focus()
        elif key == 'Right' and col < 8:
            self.cells[(row, col + 1)].focus()
    
    def validate_input(self, row: int, col: int):
        """
        ENHANCED VALIDATION with BONUS features.
        
        Real-time validation with:
        - Input format checking
        - Constraint violation detection
        - Detailed error messages
        - Visual feedback with colors
        - Initial cell protection
        
        Args:
            row: Cell row index
            col: Cell column index
        """
        entry = self.cells[(row, col)]
        value = entry.get().strip()
        
        # Allow empty cells
        if value == '':
            self.sudoku.board[row][col] = 0
            # Reset to normal color with enhanced border
            box_color = "#2d2d2d" if (row // 3 + col // 3) % 2 == 0 else "#1f1f1f"
            entry.configure(fg_color=box_color, border_color="#555555")
            return
        
        # Check if valid digit (1-9 only)
        if not value.isdigit() or len(value) > 1 or value == '0':
            entry.delete(0, 'end')
            return
        
        num = int(value)
        
        # ========== BONUS: USE CSP VALIDATION FUNCTION ==========
        is_valid, message = self.sudoku.check_user_input(row, col, num)
        
        if is_valid:
            # Valid input - update board and show green feedback
            self.sudoku.board[row][col] = num
            entry.configure(
                fg_color="#1f3d1f",  # Green tint
                border_color="#2ecc71",  # Green border (thicker)
                border_width=2,
                text_color="#2ecc71"  # Green text
            )
        else:
            # Invalid input - show error and revert
            messagebox.showwarning("Invalid Move", message)
            entry.delete(0, 'end')
            entry.configure(
                fg_color="#3d1f1f",  # Red tint
                border_color="#e74c3c",  # Red border (thicker)
                border_width=2
            )
            self.sudoku.board[row][col] = 0
            
            # Reset color after a delay
            entry.after(1000, lambda: self.reset_cell_color(row, col))
    
    def reset_cell_color(self, row: int, col: int):
        """Reset cell to normal color after error."""
        entry = self.cells[(row, col)]
        box_color = "#2d2d2d" if (row // 3 + col // 3) % 2 == 0 else "#1f1f1f"
        entry.configure(fg_color=box_color, border_color="#555555", border_width=2)
    
    def update_display(self):
        """
        Update GUI cells with current board state.
        
        Color codes:
        - Blue (#3498db): Initial puzzle numbers (readonly + locked icon)
        - Green (#2ecc71): Solved numbers
        - White: Editable empty cells
        """
        for i in range(9):
            for j in range(9):
                entry = self.cells[(i, j)]
                value = self.sudoku.board[i][j]
                
                # Enable entry to update
                entry.configure(state='normal')
                entry.delete(0, 'end')
                
                # Insert value if not empty
                if value != 0:
                    entry.insert(0, str(value))
                
                # Color code based on cell type with enhanced borders
                if self.sudoku.initial_board[i][j] != 0:
                    # Initial puzzle numbers - blue and readonly
                    entry.configure(
                        state='disabled',
                        text_color="#3498db",
                        fg_color="#1f1f1f",
                        border_color="#3498db",
                        border_width=2
                    )
                elif value != 0:
                    # Solved numbers - green
                    entry.configure(
                        text_color="#2ecc71",
                        fg_color="#1f3d1f",
                        border_color="#2ecc71",
                        border_width=2
                    )
                else:
                    # Empty editable cells - white with distinct border
                    box_color = "#2d2d2d" if (i // 3 + j // 3) % 2 == 0 else "#1f1f1f"
                    entry.configure(
                        text_color="white",
                        fg_color=box_color,
                        border_color="#555555",
                        border_width=2
                    )
    
    def read_board(self):
        """
        Read current board state from GUI entries.
        Temporarily enables readonly cells to read their values.
        """
        for i in range(9):
            for j in range(9):
                entry = self.cells[(i, j)]
                
                # Temporarily enable if readonly
                current_state = entry.cget('state')
                if current_state == 'disabled':
                    entry.configure(state='normal')
                
                # Read value
                value = entry.get().strip()
                if value.isdigit() and 1 <= int(value) <= 9:
                    self.sudoku.board[i][j] = int(value)
                else:
                    self.sudoku.board[i][j] = 0
                
                # Restore readonly state
                if current_state == 'disabled':
                    entry.configure(state='disabled')
        
        # Update initial board for reset functionality
        self.sudoku.initial_board = [row[:] for row in self.sudoku.board]
        self.update_display()