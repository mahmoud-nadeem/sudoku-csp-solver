
import time
import random
import copy
from typing import Tuple, Set, Optional, Dict


class SudokuCSP:
    
    def __init__(self):
        self.board = [[0]*9 for _ in range(9)]
        self.initial_board = [[0]*9 for _ in range(9)]
        self.domains = {} #tracking the domains of the cells
        self.ac_steps = [] #tracking the steps of the AC-3 algorithm
        self.solve_time = 0
        self.backtrack_calls = 0
        self.ac_iterations = 0
        self.singleton_assignments = 0
    
    # ========== VALIDATION ==========
    
    def validate_input_board(self) -> Tuple[bool, str]:
        """Validate using backtracking"""
        for row in range(9):
            for col in range(9):
                if self.board[row][col] != 0:
                    num = self.board[row][col]
                    self.board[row][col] = 0
                    if not self.is_valid(row, col, num):
                        self.board[row][col] = num
                        return False, f"Invalid: {num} at ({row+1}, {col+1})"
                    self.board[row][col] = num
        
        backup = [r[:] for r in self.board] #make a copy of the board
        self.init_domains() 
        solvable = self.backtrack() #check if the puzzle is solvable
        self.board = backup
        return (True, "Valid and solvable") if solvable else (False, "Unsolvable")
    
    # ========== DOMAINS ==========
    
    def init_domains(self):
        """Initialize domains with initial constraint propagation."""
        self.domains = {}
        for r in range(9):
            for c in range(9):
                if self.board[r][c] != 0:
                    self.domains[(r, c)] = [self.board[r][c]]
                else:
                    self.domains[(r, c)] = [i for i in range(1, 10) if self.is_valid(r, c, i)] #initialize the domains of the cells
        
        self.ac_steps.append({ #track the steps of the AC-3 algorithm [deep copy of the domains]
            'type': 'initialization',
            'message': 'Initialized domains',
            'domains': copy.deepcopy(self.domains)
        })
        return self.domains
    
    def get_neighbors(self, row: int, col: int) -> Set[Tuple[int, int]]: #preventing duplicates in the neighbors
        """Get 20 neighbors (row + column + box)."""
        neighbors = set()
        for c in range(9): 
            if c != col:
                neighbors.add((row, c))
        for r in range(9):
            if r != row:
                neighbors.add((r, col))
        box_r, box_c = (row // 3) * 3, (col // 3) * 3
        for r in range(box_r, box_r + 3):
            for c in range(box_c, box_c + 3):
                if (r, c) != (row, col):
                    neighbors.add((r, c))
        return neighbors
    
    def is_valid(self, row: int, col: int, num: int) -> bool:
        """Check if placement is valid."""
        for c in range(9): #check the column
            if self.board[row][c] == num:
                return False
        for r in range(9): #check the row
            if self.board[r][col] == num:
                return False
        box_r, box_c = (row // 3) * 3, (col // 3) * 3 #check the box
        for r in range(box_r, box_r + 3):
            for c in range(box_c, box_c + 3):
                if self.board[r][c] == num:
                    return False
        return True
    
    # ========== AC-3 ==========
    
    def revise(self, xi: Tuple[int, int], xj: Tuple[int, int]) -> bool:
        """Revise domain of Xi based on Xj."""
        revised = False
        to_remove = []
        for val_i in self.domains[xi][:]:
            if not any(val_i != val_j for val_j in self.domains[xj]):
                to_remove.append(val_i)
                revised = True
        for val in to_remove:
            self.domains[xi].remove(val)
        return revised
    
    def ac3(self) -> bool:
        """AC-3 algorithm."""
        queue = []
        for r in range(9):
            for c in range(9):
                cell = (r, c)
                for neighbor in self.get_neighbors(r, c):
                    queue.append((cell, neighbor))
        
        self.ac_steps.append({
            'type': 'queue_init',
            'message': f'AC-3 started with {len(queue)} arcs',
            'queue_size': len(queue)
        })
        
        iteration = 0
        while queue:
            iteration += 1
            xi, xj = queue.pop(0)
            if self.revise(xi, xj):
                if len(self.domains[xi]) <= 2:
                    self.ac_steps.append({
                        'type': 'revision',
                        'message': f'Revised {xi}, domain: {self.domains[xi]}',
                        'arc': (xi, xj),
                        'iteration': iteration
                    })
                if len(self.domains[xi]) == 0:
                    return False
                for xk in self.get_neighbors(xi[0], xi[1]):
                    if xk != xj:
                        queue.append((xk, xi))
        
        self.ac_steps.append({
            'type': 'ac3_complete',
            'message': f'AC-3 completed ({iteration} iterations)',
            'iterations': iteration
        })
        return True
    
    def propagate(self, row: int, col: int, value: int):
        """Propagate constraints."""
        for n in self.get_neighbors(row, col):
            if self.board[n[0]][n[1]] == 0 and value in self.domains[n]:
                self.domains[n].remove(value)
    
    def apply_singletons(self) -> bool:
        """Apply singleton domains."""
        changed = True
        total = 0
        while changed:
            changed = False
            for r in range(9):
                for c in range(9):
                    if self.board[r][c] == 0 and len(self.domains[(r, c)]) == 1:
                        val = self.domains[(r, c)][0]
                        self.board[r][c] = val
                        changed = True
                        total += 1
                        self.singleton_assignments += 1
                        self.ac_steps.append({
                            'type': 'assignment',
                            'message': f'Assigned {val} to {(r, c)}',
                            'cell': (r, c),
                            'value': val
                        })
                        self.propagate(r, c, val)
        return total > 0
    
    # ========== BACKTRACKING ==========
    
    def select_cell(self) -> Optional[Tuple[int, int]]:
        """MRV heuristic."""
        best = None
        min_size = 10
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    size = len(self.domains[(r, c)])
                    if size < min_size:
                        min_size = size
                        best = (r, c)
        return best
    
    def backtrack(self) -> bool:
        """Backtracking with MRV."""
        self.backtrack_calls += 1
        cell = self.select_cell()
        if cell is None:
            return True
        
        r, c = cell
        for num in self.domains[(r, c)][:]:
            if self.is_valid(r, c, num):
                saved = copy.deepcopy(self.domains)
                self.board[r][c] = num
                self.domains[(r, c)] = [num]
                self.propagate(r, c, num)
                if self.backtrack():
                    return True
                self.board[r][c] = 0
                self.domains = saved
        return False
    
    # ========== SOLVE ==========
    
    def solve(self) -> Tuple[bool, float]:
        """Main solve: AC-3 + Backtracking."""
        try:
            start = time.time()
            self.backtrack_calls = 0
            self.ac_steps = []
            self.ac_iterations = 0
            self.singleton_assignments = 0
            
            self.init_domains()
            
            max_iter = 100
            while self.ac_iterations < max_iter:
                self.ac_iterations += 1
                if not self.ac3():
                    return False, time.time() - start
                if self.apply_singletons():
                    if all(self.board[i][j] != 0 for i in range(9) for j in range(9)):
                        self.solve_time = time.time() - start
                        return True, self.solve_time
                else:
                    break
            
            success = self.backtrack()
            self.solve_time = time.time() - start
            return success, self.solve_time
        except:
            return False, 0.0
    
    # ========== GENERATION ==========
    
    def count_solutions(self, limit=2) -> int:
        """Count solutions (optimized for speed)."""
        count = [0]
        # Use a copy of the board to avoid modifying original
        board_copy = [row[:] for row in self.board]
        
        def bt():
            if count[0] >= limit:
                return
            # Find first empty cell using MRV-like approach
            best_cell = None
            min_options = 10
            for r in range(9):
                for c in range(9):
                    if board_copy[r][c] == 0:
                        # Count valid options
                        options = sum(1 for num in range(1, 10) 
                                    if self._is_valid_for_count(board_copy, r, c, num))
                        if options < min_options:
                            min_options = options
                            best_cell = (r, c)
                        if min_options == 1:
                            break
                if min_options == 1:
                    break
            
            if best_cell is None:
                # All cells filled - found a solution
                count[0] += 1
                return
            
            r, c = best_cell
            # Try each possible value
            for num in range(1, 10):
                if self._is_valid_for_count(board_copy, r, c, num):
                    board_copy[r][c] = num
                    bt()
                    board_copy[r][c] = 0
                    if count[0] >= limit:
                        return
        
        bt()
        return count[0]
    
    def _is_valid_for_count(self, board, row: int, col: int, num: int) -> bool:
        """Check if placement is valid (for count_solutions)."""
        for c in range(9):
            if board[row][c] == num:
                return False
        for r in range(9):
            if board[r][col] == num:
                return False
        box_r, box_c = (row // 3) * 3, (col // 3) * 3
        for r in range(box_r, box_r + 3):
            for c in range(box_c, box_c + 3):
                if board[r][c] == num:
                    return False
        return True
    
    def generate_puzzle(self, difficulty: str = 'easy') -> None:
        """Generate puzzle."""
        try:
            self.board = [[0]*9 for _ in range(9)]
            self.init_domains()
            
            # Fill diagonal boxes
            for box in range(3):
                nums = list(range(1, 10))
                random.shuffle(nums)
                idx = 0
                for i in range(3):
                    for j in range(3):
                        r, c = box*3 + i, box*3 + j
                        self.board[r][c] = nums[idx]
                        self.domains[(r, c)] = [nums[idx]]
                        idx += 1
            
            # Solve the complete puzzle
            if not self.backtrack():
                # If backtracking fails, try again
                self.board = [[0]*9 for _ in range(9)]
                self.init_domains()
                for box in range(3):
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    idx = 0
                    for i in range(3):
                        for j in range(3):
                            r, c = box*3 + i, box*3 + j
                            self.board[r][c] = nums[idx]
                            self.domains[(r, c)] = [nums[idx]]
                            idx += 1
                self.backtrack()
            
            # Remove cells based on difficulty
            remove = {'easy': 35, 'intermediate': 45, 'hard': 50}[difficulty]  # Reduced hard to 50
            cells = [(i, j) for i in range(9) for j in range(9)]
            random.shuffle(cells)
            
            removed = 0
            max_attempts = 1500 if difficulty == 'hard' else len(cells)  # Limit for hard puzzles
            
            for idx, (r, c) in enumerate(cells):
                if removed >= remove:
                    break
                if idx >= max_attempts:
                    break
                    
                backup = self.board[r][c]
                
                if difficulty == 'hard':
                    # For hard puzzles, verify uniqueness
                    self.board[r][c] = 0
                    solutions = self.count_solutions(2)
                    
                    if solutions == 1:
                        removed += 1
                    else:
                        # Restore the cell if it creates multiple solutions
                        self.board[r][c] = backup
                else:
                    # For easy/intermediate, just remove
                    self.board[r][c] = 0
                    removed += 1
            
            self.initial_board = [row[:] for row in self.board]
        except Exception as e:
            # If generation fails, create a simple puzzle
            self.board = [[0]*9 for _ in range(9)]
            self.initial_board = [[0]*9 for _ in range(9)]
            # Try one more time with simpler approach
            try:
                self.board = [[0]*9 for _ in range(9)]
                self.init_domains()
                for box in range(3):
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    idx = 0
                    for i in range(3):
                        for j in range(3):
                            r, c = box*3 + i, box*3 + j
                            self.board[r][c] = nums[idx]
                            self.domains[(r, c)] = [nums[idx]]
                            idx += 1
                self.backtrack()
                # Remove fewer cells if hard puzzle fails
                if difficulty == 'hard':
                    remove = 50  # Reduce to 50 instead of 55
                cells = [(i, j) for i in range(9) for j in range(9)]
                random.shuffle(cells)
                removed = 0
                for r, c in cells[:remove]:
                    self.board[r][c] = 0
                self.initial_board = [row[:] for row in self.board]
            except:
                self.board = [[0]*9 for _ in range(9)]
                self.initial_board = [[0]*9 for _ in range(9)]
    
    def reset(self) -> None:
        """Reset to initial state."""
        self.board = [row[:] for row in self.initial_board]
        self.ac_steps = []
        self.backtrack_calls = 0
        self.ac_iterations = 0
        self.singleton_assignments = 0
  
    
    def check_user_input(self, row: int, col: int, num: int) -> Tuple[bool, str]:
        """Check user input validity."""
        if not (1 <= num <= 9):
            return False, "Number must be between 1 and 9"
        for c in range(9):
            if c != col and self.board[row][c] == num:
                return False, f"Number {num} already exists in row {row+1}"
        for r in range(9):
            if r != row and self.board[r][col] == num:
                return False, f"Number {num} already exists in column {col+1}"
        box_r, box_c = (row // 3) * 3, (col // 3) * 3
        for r in range(box_r, box_r + 3):
            for c in range(box_c, box_c + 3):
                if (r, c) != (row, col) and self.board[r][c] == num:
                    return False, f"Number {num} already exists in 3x3 box"
        return True, "Valid input"
