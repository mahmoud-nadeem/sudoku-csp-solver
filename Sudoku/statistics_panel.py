# ==============================================================================
# FILE: statistics_panel.py
# Statistics Panel with CustomTkinter - ENHANCED
# ==============================================================================

"""
Statistics Panel Module - Enhanced Version
Displays solve statistics including time, difficulty, and algorithm metrics.
Uses CustomTkinter for modern UI.

Enhancements:
- Added AC-3 iterations tracking
- Added singleton assignments tracking
- Better formatting and organization
"""

import customtkinter as ctk


class StatisticsPanel:
    """
    Modern statistics panel using CustomTkinter.
    Displays:
    - Solve time
    - Difficulty level
    - Arc Consistency metrics (iterations, singleton assignments)
    - Backtracking metrics (calls)
    - Total AC steps
    """
    
    def __init__(self, parent):
        """
        Initialize statistics panel.
        
        Args:
            parent: Parent CTk widget
        """
        # Main frame - fills parent
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.frame.pack(fill='both', expand=True, padx=15, pady=12)
        
        # Title
        ctk.CTkLabel(
            self.frame,
            text="Statistics",
            font=("Arial", 16, "bold"),
            anchor="center"
        ).pack(pady=(0, 12))
        
        # Statistics label
        self.stats_label = ctk.CTkLabel(
            self.frame,
            text="No puzzle solved yet",
            font=("Arial", 10),
            justify='left',
            anchor="w"
        )
        self.stats_label.pack(padx=8, pady=8, fill='both', expand=True)
    
    def update_stats(self, solve_time, difficulty, backtrack_calls, ac_steps, 
                     ac_iterations=0, singleton_assignments=0):
        """
        Update statistics display with solve results.
        
        Args:
            solve_time: Time taken to solve (seconds)
            difficulty: Puzzle difficulty level
            backtrack_calls: Number of backtracking calls made
            ac_steps: Total number of AC steps performed
            ac_iterations: Number of AC-3 loop iterations
            singleton_assignments: Number of cells solved by singleton domains
        """
        # Calculate percentages
        ac_percentage = (singleton_assignments / 81) * 100 if singleton_assignments > 0 else 0
        backtrack_percentage = ((81 - singleton_assignments) / 81) * 100 if singleton_assignments < 81 else 0
        
        # Determine solving method
        if backtrack_calls == 0:
            method = "AC-3 Only ✓"
        else:
            method = "AC-3 + Backtracking"
        
        # Format statistics text
        stats_text = (
            f"╔═══════════════════════════╗\n"
            f"  Solve Time: {solve_time:.4f}s\n"
            f"  Difficulty: {difficulty.capitalize()}\n"
            f"  Method: {method}\n"
            f"╚═══════════════════════════╝\n\n"
            
            f"┌─ Arc Consistency (AC-3) ──┐\n"
            f"│ Iterations: {ac_iterations}\n"
            f"│ Cells Solved: {singleton_assignments}/81\n"
            f"│   ({ac_percentage:.1f}%)\n"
            f"│ Total Steps: {ac_steps}\n"
            f"└────────────────────────────┘\n\n"
            
            f"┌─ Backtracking ─────────────┐\n"
            f"│ Calls: {backtrack_calls}\n"
            f"│ Cells Needed: {81-singleton_assignments}/81\n"
            f"│   ({backtrack_percentage:.1f}%)\n"
            f"└────────────────────────────┘\n\n"
            
            f"┌─ Performance ──────────────┐\n"
            f"│ AC-3 Efficiency:\n"
            f"│   {ac_percentage:.1f}%\n"
        )
        
        # Add performance rating
        if ac_percentage >= 90:
            stats_text += f"│ Rating:\n│   ★★★★★ Excellent\n"
        elif ac_percentage >= 70:
            stats_text += f"│ Rating:\n│   ★★★★☆ Very Good\n"
        elif ac_percentage >= 50:
            stats_text += f"│ Rating:\n│   ★★★☆☆ Good\n"
        elif ac_percentage >= 30:
            stats_text += f"│ Rating:\n│   ★★☆☆☆ Fair\n"
        else:
            stats_text += f"│ Rating:\n│   ★☆☆☆☆ Complex\n"
        
        stats_text += f"└────────────────────────────┘"
        
        self.stats_label.configure(text=stats_text, font=("Courier", 9))
    
    def reset(self):
        """Reset statistics display to default state."""
        self.stats_label.configure(
            text="No puzzle solved yet",
            font=("Arial", 11)
        )