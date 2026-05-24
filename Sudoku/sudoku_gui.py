# ==============================================================================
# FILE: sudoku_gui.py
# Main GUI Coordinator with VALIDATION & EXPORT Features
# ==============================================================================

"""
Sudoku GUI Coordinator Module - Enhanced Version
Main GUI class that manages all windows and coordinates between components.

Enhanced Features:
- Input validation before solving (Assignment requirement)
- Statistics export to CSV for report
- Improved error handling
"""

import customtkinter as ctk
from tkinter import messagebox
from sudoku_csp import SudokuCSP
from configuration_window import ConfigurationWindow
from game_board_window import GameBoardWindow
from statistics_panel import StatisticsPanel
from visualization_window import VisualizationWindow


class SudokuGUI:
    """
    Enhanced Main GUI coordinator with validation and export features.
    
    Manages all components:
    - Configuration window (left panel)
    - Game board window (center panel) with BONUS validation
    - Statistics panel (right panel)
    - Visualization window (separate popup)
    - Export functionality for reports
    """
    
    def __init__(self, root):
        """
        Initialize the main GUI.
        
        Args:
            root: Root CTk window
        """
        self.root = root
        self.root.title("Sudoku CSP Solver - AI Project (Enhanced)")
        self.root.geometry("1400x800")
        
        # Create CSP solver instance
        self.sudoku = SudokuCSP()
        
        # ========== Title Bar ==========
        title_frame = ctk.CTkFrame(self.root, corner_radius=0, height=50)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            title_frame,
            text="Sudoku CSP Solver with Arc Consistency  ",
            font=("Arial", 20, "bold"),
            anchor="center"
        ).pack(pady=12)
        
        # ========== Main Container (NO SCROLLING) ==========
        main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        main_container.pack(fill='both', expand=True, padx=8, pady=8)
        
        # ========== Left Panel: Configuration ==========
        left_panel = ctk.CTkFrame(main_container, width=320)
        left_panel.pack(side='left', fill='y', padx=4, pady=4)
        left_panel.pack_propagate(False)
        
        # ========== Center Panel: Game Board ==========
        center_panel = ctk.CTkFrame(main_container, width=560)
        center_panel.pack(side='left', fill='both', expand=True, padx=4, pady=4)
        
        # ========== Right Panel: Statistics ==========
        right_panel = ctk.CTkFrame(main_container, width=320)
        right_panel.pack(side='right', fill='y', padx=4, pady=4)
        right_panel.pack_propagate(False)
        
        # ========== Create Callbacks Dictionary ==========
        self.callbacks = {
            'generate': self.generate_puzzle,
            'solve': self.solve_puzzle,
            'reset': self.reset_board,
            'clear': self.clear_board
        }
        
        # ========== Initialize Components ==========
        self.config_window = ConfigurationWindow(left_panel, self.sudoku, self.callbacks)
        self.board_window = GameBoardWindow(center_panel, self.sudoku, self.callbacks)
        self.stats_panel = StatisticsPanel(right_panel)
        
        # ========== Enhanced Control Buttons in Right Panel ==========
        button_container = ctk.CTkFrame(right_panel, corner_radius=10)
        button_container.pack(pady=10, padx=12, fill='x')
        
        # Visualization Button (opens visualization window)
        ctk.CTkButton(
            button_container,
            text="Show Visualization",
            command=self.open_visualization,
            font=("Arial", 11, "bold"),
            height=35,
            corner_radius=8,
            fg_color="#9b59b6",
            hover_color="#8e44ad"
        ).pack(pady=4, fill='x', padx=12)
        
        # Export Statistics Button
        ctk.CTkButton(
            button_container,
            text="Export Statistics",
            command=self.export_statistics,
            font=("Arial", 11, "bold"),
            height=35,
            corner_radius=8,
            fg_color="#e67e22",
            hover_color="#d35400"
        ).pack(pady=4, fill='x', padx=12)
        
        # Visualization window reference
        self.viz_window = None
        self.visualization = None
    
    def open_visualization(self):
        """
        Open or focus visualization window.
        Displays AC-3 algorithm steps in the visualization window.
        """
        try:
            if self.viz_window is None or not self.viz_window.winfo_exists():
                self.viz_window = ctk.CTkToplevel(self.root)
                self.viz_window.title("Arc Consistency Visualization")
                self.viz_window.geometry("900x750")
                self.visualization = VisualizationWindow(self.viz_window, self.sudoku)
                
                # If puzzle has been solved, display the AC-3 steps
                if self.sudoku.ac_steps:
                    self.visualization.display_steps(
                        self.sudoku.ac_steps,
                        self.sudoku.backtrack_calls,
                        self.sudoku.solve_time,
                        self.sudoku.domains
                    )
            else:
                self.viz_window.focus()
                # Update visualization if puzzle has been solved
                if self.sudoku.ac_steps and self.visualization is not None:
                    self.visualization.display_steps(
                        self.sudoku.ac_steps,
                        self.sudoku.backtrack_calls,
                        self.sudoku.solve_time,
                        self.sudoku.domains
                    )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to open visualization window:\n{str(e)}"
            )
    
    def export_statistics(self):
        """
        Export statistics to CSV for report comparison.
        """
        if self.sudoku.solve_time == 0:
            messagebox.showwarning(
                "No Data",
                "Please solve a puzzle first before exporting statistics!"
            )
            return
        
        try:
            if hasattr(self.sudoku, 'export_statistics_csv'):
                success, message = self.sudoku.export_statistics_csv()
                
                if success:
                    messagebox.showinfo("Export Success", message)
                else:
                    messagebox.showerror("Export Failed", message)
            else:
                messagebox.showinfo(
                    "Feature Not Available",
                    "Statistics export feature is not available in the current version."
                )
        except Exception as e:
            messagebox.showerror(
                "Export Failed",
                f"Error exporting statistics:\n{str(e)}"
            )
    
    def generate_puzzle(self):
        """
        Generate a new random puzzle based on selected difficulty.
        """
        self.clear_board()
        difficulty = self.config_window.get_difficulty()
        
        # Generate puzzle
        self.sudoku.generate_puzzle(difficulty)
        
        # Update display
        self.board_window.update_display()
        
        messagebox.showinfo("Success", f"Generated {difficulty} puzzle!")
    
    def solve_puzzle(self):
        """
        Solve the current puzzle with INPUT VALIDATION.
        Enhanced with validation before solving (Assignment requirement).
        """
        # Read current board state
        self.board_window.read_board()
        
        # Check if board is empty
        if all(self.sudoku.board[i][j] == 0 for i in range(9) for j in range(9)):
            messagebox.showwarning(
                "Empty Board",
                "Please generate or input a puzzle first!"
            )
            return
        
        # ========== VALIDATE INPUT FIRST (ASSIGNMENT REQUIREMENT) ==========
        is_valid, validation_message = self.sudoku.validate_input_board()
        
        if not is_valid:
            messagebox.showerror(
                "Invalid Board",
                f"Cannot solve puzzle:\n\n{validation_message}\n\nPlease fix the input and try again."
            )
            return
        
        # Show validation success
        messagebox.showinfo(
            "Validation Passed",
            f"{validation_message}\n\nProceeding to solve..."
        )
        
        # ========== SOLVE USING CSP ==========
        success, solve_time = self.sudoku.solve()
        
        if not success:
            messagebox.showerror(
                "Unsolvable",
                "This puzzle has no solution!\n\nThis should not happen after validation."
            )
            return
        
        # Update board display
        self.board_window.update_display()
        
        # Update statistics panel
        difficulty = self.config_window.get_difficulty()
        self.stats_panel.update_stats(
            solve_time,
            difficulty,
            self.sudoku.backtrack_calls,
            len(self.sudoku.ac_steps),
            self.sudoku.ac_iterations,
            self.sudoku.singleton_assignments
        )
        
        # Update visualization window if open
        if (self.viz_window is not None and self.viz_window.winfo_exists() 
            and self.visualization is not None):
            self.visualization.display_steps(
                self.sudoku.ac_steps,
                self.sudoku.backtrack_calls,
                solve_time,
                self.sudoku.domains
            )
        
        # Show success message with details
        method = "AC-3 only" if self.sudoku.backtrack_calls == 0 else "AC-3 + Backtracking"
        messagebox.showinfo(
            "Success",
            f"Puzzle solved in {solve_time:.4f} seconds!\n\n"
            f"Method: {method}\n"
            f"AC-3 solved: {self.sudoku.singleton_assignments}/81 cells\n"
            f"Backtracking calls: {self.sudoku.backtrack_calls}"
        )
    
    def reset_board(self):
        """
        Reset board to initial puzzle state (before solving).
        """
        if all(self.sudoku.initial_board[i][j] == 0 for i in range(9) for j in range(9)):
            messagebox.showinfo(
                "Already Empty",
                "Board is already empty. Generate or input a puzzle first."
            )
            return
        
        self.sudoku.reset()
        self.board_window.update_display()
        self.stats_panel.reset()
        
        messagebox.showinfo("Reset", "Board reset to initial puzzle state!")
    
    def clear_board(self):
        """
        Clear entire board to empty state.
        """
        self.sudoku.board = [[0 for _ in range(9)] for _ in range(9)]
        self.sudoku.initial_board = [[0 for _ in range(9)] for _ in range(9)]
        self.sudoku.ac_steps = []
        self.sudoku.backtrack_calls = 0
        self.sudoku.ac_iterations = 0
        self.sudoku.singleton_assignments = 0
        
        self.board_window.update_display()
        self.stats_panel.reset()