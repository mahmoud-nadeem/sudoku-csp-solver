# ==============================================================================
# FILE: configuration_window.py
# Configuration Window - FIXED LAYOUT
# ==============================================================================

"""
Configuration Window Module - Fixed Version
Handles game mode selection, difficulty settings, and control buttons.
Uses CustomTkinter with improved spacing and layout.
"""

import customtkinter as ctk


class ConfigurationWindow:
    """
    Modern configuration window with consistent spacing.
    Provides controls for:
    - Game mode selection (Generate vs Manual Input)
    - Difficulty level selection
    - Control buttons (Generate, Solve, Reset, Clear)
    """
    
    def __init__(self, parent, sudoku_csp, callbacks):
        """
        Initialize configuration window.
        
        Args:
            parent: Parent CTk widget
            sudoku_csp: SudokuCSP instance
            callbacks: Dictionary of callback functions
        """
        self.sudoku = sudoku_csp
        self.callbacks = callbacks
        
        # Main frame - fills parent
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.frame.pack(fill='both', expand=True, padx=15, pady=12)
        
        # GUI variables
        self.mode = ctk.StringVar(value='generate')
        self.difficulty = ctk.StringVar(value='easy')
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create all configuration widgets with consistent spacing."""
        
        # ========== Title ==========
        ctk.CTkLabel(
            self.frame,
            text="Configuration",
            font=("Arial", 16, "bold"),
            anchor="center"
        ).pack(pady=(0, 12))
        
        # ========== Mode Selection Section ==========
        mode_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        mode_frame.pack(fill='x', pady=10)
        
        ctk.CTkLabel(
            mode_frame,
            text="Game Mode",
            font=("Arial", 13, "bold"),
            anchor="center"
        ).pack(pady=(12, 8))
        
        # Radio button for Generate mode
        ctk.CTkRadioButton(
            mode_frame,
            text="Generate Puzzle",
            variable=self.mode,
            value='generate',
            font=("Arial", 11),
            command=self.on_mode_change
        ).pack(anchor='w', padx=25, pady=6)
        
        # Radio button for Manual Input mode
        ctk.CTkRadioButton(
            mode_frame,
            text="Manual Input",
            variable=self.mode,
            value='input',
            font=("Arial", 11),
            command=self.on_mode_change
        ).pack(anchor='w', padx=25, pady=(6, 12))
        
        # ========== Difficulty Selection Section ==========
        diff_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        diff_frame.pack(fill='x', pady=10)
        
        ctk.CTkLabel(
            diff_frame,
            text="Difficulty Level",
            font=("Arial", 13, "bold"),
            anchor="center"
        ).pack(pady=(12, 8))
        
        # Dropdown menu for difficulty selection
        self.difficulty_menu = ctk.CTkOptionMenu(
            diff_frame,
            variable=self.difficulty,
            values=['easy', 'intermediate', 'hard'],
            font=("Arial", 11),
            width=180,
            height=36
        )
        self.difficulty_menu.pack(pady=(0, 12))
        
        # ========== Control Buttons Section ==========
        button_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        button_frame.pack(fill='x', pady=10)
        
        ctk.CTkLabel(
            button_frame,
            text="Controls",
            font=("Arial", 13, "bold"),
            anchor="center"
        ).pack(pady=(12, 10))
        
        # Generate button
        self.generate_btn = ctk.CTkButton(
            button_frame,
            text="Generate",
            command=self.callbacks.get('generate'),
            font=("Arial", 12, "bold"),
            height=40,
            corner_radius=8
        )
        self.generate_btn.pack(fill='x', padx=18, pady=6)
        
        # Solve button - Green color
        ctk.CTkButton(
            button_frame,
            text="Solve",
            command=self.callbacks.get('solve'),
            font=("Arial", 12, "bold"),
            height=40,
            corner_radius=8,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        ).pack(fill='x', padx=18, pady=6)
        
        # Reset button - Orange color
        ctk.CTkButton(
            button_frame,
            text="Reset",
            command=self.callbacks.get('reset'),
            font=("Arial", 12, "bold"),
            height=40,
            corner_radius=8,
            fg_color="#e67e22",
            hover_color="#d35400"
        ).pack(fill='x', padx=18, pady=6)
        
        # Clear button - Red color
        ctk.CTkButton(
            button_frame,
            text="Clear",
            command=self.callbacks.get('clear'),
            font=("Arial", 12, "bold"),
            height=40,
            corner_radius=8,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        ).pack(fill='x', padx=18, pady=(6, 12))
    
    def on_mode_change(self):
        """
        Handle mode change between generate and input.
        Disables generate button and difficulty menu in manual input mode.
        """
        if self.mode.get() == 'generate':
            self.generate_btn.configure(state='normal')
            self.difficulty_menu.configure(state='normal')
        else:
            self.generate_btn.configure(state='disabled')
            self.difficulty_menu.configure(state='disabled')
    
    def get_mode(self):
        """Get current game mode."""
        return self.mode.get()
    
    def get_difficulty(self):
        """Get current difficulty level."""
        return self.difficulty.get()