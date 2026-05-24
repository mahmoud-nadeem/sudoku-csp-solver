# 🧩 Sudoku CSP Solver

A **Sudoku solver** built with Constraint Satisfaction Problem (CSP) techniques, featuring **Arc Consistency (AC-3)** and **Backtracking Search with MRV heuristic** — wrapped in a modern dark-mode GUI.

> 📌 **Course:** Artificial Intelligence — Assignment 3  
> 🏫 **Institution:** Alexandria National University  
> 👤 **Author:** Mahmoud Hazem Ali Nadeem

---

## 📸 Features

- ✅ Solves any valid 9×9 Sudoku puzzle
- ✅ **AC-3 Algorithm** for arc consistency and constraint propagation
- ✅ **Backtracking Search** with MRV (Minimum Remaining Values) heuristic
- ✅ **Real-time input validation** — detects constraint violations as you type
- ✅ **Statistics panel** — solve time, AC-3 iterations, backtracking calls
- ✅ **AC-3 step visualization** — view each arc revision in a tree trace
- ✅ **Puzzle generator** — Easy / Intermediate / Hard levels
- ✅ **Export** — save AC tree to `.txt` and statistics to `.csv`
- ✅ Modern dark-mode GUI built with CustomTkinter

---

## 🗂️ Project Structure

```
Sudoku/
├── main.py                  # Entry point — launches the app
├── sudoku_csp.py            # Core CSP solver (AC-3 + backtracking + MRV)
├── sudoku_gui.py            # Main GUI coordinator
├── configuration_window.py  # Left panel — difficulty & controls
├── game_board_window.py     # Center panel — interactive 9×9 board
├── statistics_panel.py      # Right panel — performance metrics
├── visualization_window.py  # Popup — AC-3 step-by-step trace
└── REPORT.md                # Full assignment report
```

---

## ⚙️ Requirements

| Requirement | Version |
|-------------|---------|
| Python | 3.10+ (tested on 3.13) |
| customtkinter | latest |
| tkinter | bundled with Python |

> All other modules used (`time`, `random`, `copy`, `typing`) are part of the Python standard library — **no extra installation needed**.

---

## 📦 Installation

**1. Clone the repository**

```bash
git clone https://github.com/your-username/sudoku-csp-solver.git
cd sudoku-csp-solver
```

**2. Install the required package**

```bash
pip install customtkinter
```

**3. Run the app**

```bash
python main.py
```

---

## 🚀 How to Use

1. Launch the app with `python main.py`
2. Choose a mode from the **Configuration Panel** (left):
   - 🎲 **Generate Puzzle** — pick Easy, Intermediate, or Hard
   - ✏️ **Manual Input** — type your own puzzle directly on the board
3. Click **Solve** to run the CSP solver
4. View the solution on the board:
   - 🔵 Blue cells = initial (given) values
   - 🟢 Green cells = solved by the algorithm
5. Check the **Statistics Panel** (right) for performance details
6. Click **View AC-3 Steps** to open the visualization window

---

## 🧠 Algorithms

### AC-3 (Arc Consistency Algorithm)

Enforces arc consistency by iteratively removing values from domains that violate constraints.

```
AC-3():
  queue ← all arcs (Xi, Xj) where Xi and Xj are neighbors
  while queue is not empty:
    (Xi, Xj) ← pop from queue
    if REVISE(Xi, Xj):
      if domain[Xi] is empty → return False  // inconsistent
      for each neighbor Xk of Xi (Xk ≠ Xj):
        add (Xk, Xi) to queue
  return True
```

- **Time Complexity:** O(n²d³) — n=81 cells, d=9 domain size
- **Total initial arcs:** 1,620 (81 cells × 20 neighbors each)

### Backtracking with MRV Heuristic

When AC-3 alone can't solve the puzzle, backtracking takes over — always picking the **most constrained cell first**.

```
BACKTRACK():
  if all cells assigned → return True
  cell ← SELECT_UNASSIGNED_VARIABLE()  // MRV: smallest domain
  for each value in domain[cell]:
    if is_valid(cell, value):
      assign value → propagate constraints
      if BACKTRACK() → return True
      unassign value → restore domains
  return False
```

---

## 📊 Performance Results

| Difficulty | Filled Cells | Solve Time | AC-3 Iterations | Solved by AC-3 | Backtracking Calls |
|------------|:------------:|:----------:|:---------------:|:--------------:|:------------------:|
| Easy | 26 | 0.023s | 3 | 75 / 81 (92.6%) | 12 |
| Intermediate | 17 | 0.089s | 5 | 42 / 81 (51.9%) | 156 |
| Hard | 17–20 | 0.343s | 2–3 | ~10 / 81 (<20%) | 1,247 |

**Key takeaway:** AC-3 is most effective on dense (easy) puzzles. As the puzzle gets harder, backtracking takes over — but the MRV heuristic keeps it fast even on the hardest puzzles (< 0.5s).

---

## 📐 CSP Problem Formulation

| Component | Definition |
|-----------|------------|
| **Variables** | Each of the 81 cells — represented as `(row, col)` |
| **Domains** | `[1–9]` for empty cells; singleton `[n]` for pre-filled cells |
| **Constraints** | No duplicate values in any row, column, or 3×3 box |
| **Objective** | Assign values to all 81 cells satisfying all constraints |

---

## 📁 Export Options

From the app you can export:

- 📄 **AC-3 Step Trace** → `.txt` file with full arc revision history
- 📊 **Solve Statistics** → `.csv` file with all performance metrics

---

## 📄 License

This project was developed as a university assignment. Feel free to use it for learning purposes.
