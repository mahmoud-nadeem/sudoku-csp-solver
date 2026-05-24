# ==============================================================================
# FILE: main.py
# Main Entry Point
# ==============================================================================

"""
Sudoku CSP Solver - Main Entry Point
Assignment 3 - Artificial Intelligence Course
Alexandria National University

This program implements a complete Sudoku solver using:
1. Constraint Satisfaction Problem (CSP) formulation
2. Arc Consistency (AC-3 Algorithm)
3. Backtracking with constraint propagation
4. Modern GUI with CustomTkinter

Instructions:
1. Install required packages: pip install customtkinter
2. Run with: python main.py
3. Select mode (Generate or Manual Input)
4. Click Generate or input your own puzzle
5. Click Solve to see the solution
"""

import customtkinter as ctk
from sudoku_gui import SudokuGUI

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


def main():
    """
    Main function to run the application.
    Creates the CTk root window and starts the GUI event loop.
    """
    root = ctk.CTk()
    app = SudokuGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

