# ==============================================================================
# FILE: visualization_window.py
# Arc Consistency Visualization
# ==============================================================================

"""
Visualization Window Module
Displays detailed trace of AC-3 algorithm execution.

Features:
- Detailed AC-3 steps trace
- Better formatting and organization
"""

import customtkinter as ctk


class VisualizationWindow:
    """
    Visualization window for AC-3 algorithm steps.
    
    Features:
    - Detailed AC-3 steps trace
    - Export-ready formatting
    """
    
    def __init__(self, parent, sudoku_csp=None):
        """
        Initialize visualization window.
        
        Args:
            parent: Parent CTk widget (typically a Toplevel window)
            sudoku_csp: SudokuCSP instance
        """
        self.sudoku = sudoku_csp
        
        # Main frame
        self.frame = ctk.CTkFrame(parent, corner_radius=15)
        self.frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Title
        ctk.CTkLabel(
            self.frame,
            text="Arc Consistency Visualization",
            font=("Arial", 16, "bold"),
            anchor="center"
        ).pack(pady=15)
        
        # Create tabbed view
        self.tabview = ctk.CTkTabview(self.frame)
        self.tabview.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Add tabs
        self.tabview.add("AC-3 Steps")
        
        # ========== Tab 1: AC-3 Steps ==========
        self.steps_text = ctk.CTkTextbox(
            self.tabview.tab("AC-3 Steps"),
            font=("Courier", 10),
            corner_radius=10,
            wrap='word'
        )
        self.steps_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def clear(self):
        """Clear all text from the steps tab."""
        self.steps_text.delete('1.0', 'end')
    
    def display_steps(self, ac_steps, backtrack_calls, solve_time, domains):
        """
        Display complete arc consistency algorithm trace.
        
        Args:
            ac_steps: List of AC-3 algorithm steps
            backtrack_calls: Number of backtracking calls
            solve_time: Total solving time
            domains: Final domain state for all cells
        """
        self.clear()
        
        # ========== TAB 1: AC-3 STEPS ==========
        self.steps_text.insert('end', "="*70 + "\n")
        self.steps_text.insert('end', "SUDOKU CSP SOLVER - ARC CONSISTENCY TRACE\n")
        self.steps_text.insert('end', "="*70 + "\n\n")
        
        phase1_shown = False
        phase2_shown = False
        phase3_shown = False
        
        for step in ac_steps:
            step_type = step['type']
            
            # Phase 1: Domain Initialization
            if step_type == 'initialization':
                if not phase1_shown:
                    self.steps_text.insert('end', "PHASE 1: DOMAIN INITIALIZATION\n")
                    self.steps_text.insert('end', "-"*70 + "\n")
                    phase1_shown = True
                
                self.steps_text.insert('end', f"\n{step['message']}\n")
                
                sample_cells = [(0, 0), (0, 1), (4, 4), (8, 8)]
                for cell in sample_cells:
                    if cell in step['domains']:
                        domain = step['domains'][cell]
                        self.steps_text.insert('end', f"  Cell {cell}: domain = {domain}\n")
            
            # Phase 2: Arc Consistency
            elif step_type == 'queue_init':
                if not phase2_shown:
                    self.steps_text.insert('end', f"\n\nPHASE 2: ARC CONSISTENCY (AC-3)\n")
                    self.steps_text.insert('end', "-"*70 + "\n")
                    phase2_shown = True
                self.steps_text.insert('end', f"\n{step['message']}\n")
            
            elif step_type == 'iteration_start':
                self.steps_text.insert('end', f"\n{step['message']}\n")
            
            elif step_type == 'revision':
                iteration = step.get('iteration', 0)
                arc = step['arc']
                if iteration % 50 == 0 or step.get('domain_size', 9) == 1:
                    self.steps_text.insert('end', f"\nIteration {iteration}:\n")
                    self.steps_text.insert('end', f"  Arc: {arc[0]} -> {arc[1]}\n")
                    self.steps_text.insert('end', f"  Domain size: {step.get('domain_size', 'N/A')}\n")
                    
                    if arc[0] in step.get('domains', {}):
                        domain = step['domains'][arc[0]]
                        self.steps_text.insert('end', f"  New domain: {domain}\n")
            
            elif step_type == 'ac3_complete':
                self.steps_text.insert('end', f"\n{step['message']}\n")
            
            elif step_type == 'assignment':
                self.steps_text.insert('end', f"  [ASSIGNED] {step['message']}\n")
            
            elif step_type == 'singleton_summary':
                self.steps_text.insert('end', f"\n{step['message']}\n")
            
            elif step_type == 'ac3_limit':
                self.steps_text.insert('end', f"\n{step['message']}\n")
                self.steps_text.insert('end', f"  Remaining cells require backtracking search\n")
            
            elif step_type == 'ac3_solved':
                self.steps_text.insert('end', "\n" + "="*70 + "\n")
                self.steps_text.insert('end', f"  {step['message']}\n")
                self.steps_text.insert('end', "="*70 + "\n")
            
            elif step_type == 'failure':
                self.steps_text.insert('end', f"\n[FAILED] {step['message']}\n")
            
            # Phase 3: Backtracking
            elif step_type == 'complete':
                if not phase3_shown:
                    self.steps_text.insert('end', f"\n\nPHASE 3: BACKTRACKING SEARCH\n")
                    self.steps_text.insert('end', "-"*70 + "\n")
                    phase3_shown = True
                self.steps_text.insert('end', f"\n{step['message']}\n")
        
        # Final Statistics
        self.steps_text.insert('end', f"\n\nFINAL STATISTICS\n")
        self.steps_text.insert('end', "-"*70 + "\n")
        
        singleton_count = sum(1 for domain in domains.values() if len(domain) == 1)
        
        self.steps_text.insert('end', f"Singleton domains (solved by AC-3): {singleton_count}/81\n")
        self.steps_text.insert('end', f"Cells requiring backtracking: {81 - singleton_count}/81\n")
        self.steps_text.insert('end', f"Backtracking calls: {backtrack_calls}\n")
        
        self.steps_text.insert('end', "\n" + "="*70 + "\n")
        self.steps_text.insert('end', f"[SUCCESS] PUZZLE SOLVED!\n")
        self.steps_text.insert('end', f"Total time: {solve_time:.4f} seconds\n")
        self.steps_text.insert('end', "="*70 + "\n")
        
        self.steps_text.see('1.0')