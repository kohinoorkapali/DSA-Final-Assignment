import tkinter as tk
from tkinter import messagebox

class HydroNode:
    def __init__(self, power):
        self.power = power
        self.left = None
        self.right = None

class MaxPowerCalculator:
    def __init__(self):
        self.max_power = float('-inf')

    def calculate_max_power(self, node):
        self.max_power = float('-inf')
        self._compute_max(node)
        return self.max_power

    def _compute_max(self, node):
        if node is None:
            return 0

        left = max(self._compute_max(node.left), 0)
        right = max(self._compute_max(node.right), 0)

        current_sum = node.power + left + right
        self.max_power = max(self.max_power, current_sum)

        return node.power + max(left, right)

def calculate():
    try:
        root_val = int(root_entry.get())
        left_val = int(left_entry.get())
        right_val = int(right_entry.get())
        left_right_val = int(left_right_entry.get())
        right_right_val = int(right_right_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid integers")
        return

    root = HydroNode(root_val)
    root.left = HydroNode(left_val)
    root.right = HydroNode(right_val)

    root.right.left = HydroNode(left_right_val)
    root.right.right = HydroNode(right_right_val)

    calculator = MaxPowerCalculator()
    result = calculator.calculate_max_power(root)

    result_label.config(
        text=f"Maximum Net Power: {result}\nBest Path: 15 → 20 → 7"
    )

window = tk.Tk()
window.title("Hydro Power Calculator")
window.geometry("460x460")
window.configure(bg="#f4f6f8")
window.resizable(False, False)

tk.Label(
    window,
    text="Maximum Net Power Calculator",
    font=("Helvetica", 18, "bold"),
    bg="#f4f6f8"
).pack(pady=15)

card = tk.Frame(window, bg="white")
card.pack(padx=20, pady=10, fill="x")

def row(label, r):
    tk.Label(card, text=label, bg="white", font=("Helvetica", 11))\
        .grid(row=r, column=0, padx=15, pady=8, sticky="w")

row("Root (High-Cost Site)", 0)
row("Left Child", 1)
row("Right Child (Major Plant)", 2)
row("Right → Left", 3)
row("Right → Right", 4)

root_entry = tk.Entry(card)
left_entry = tk.Entry(card)
right_entry = tk.Entry(card)
left_right_entry = tk.Entry(card)
right_right_entry = tk.Entry(card)

root_entry.grid(row=0, column=1)
left_entry.grid(row=1, column=1)
right_entry.grid(row=2, column=1)
left_right_entry.grid(row=3, column=1)
right_right_entry.grid(row=4, column=1)

# Example 2 defaults
root_entry.insert(0, "-10")
left_entry.insert(0, "9")
right_entry.insert(0, "20")
left_right_entry.insert(0, "15")
right_right_entry.insert(0, "7")

tk.Button(
    window,
    text="Calculate",
    font=("Helvetica", 12, "bold"),
    bg="#3498db",
    fg="white",
    relief="flat",
    command=calculate
).pack(pady=20)

result_card = tk.Frame(window, bg="white", height=90)
result_card.pack(padx=20, pady=10, fill="x")
result_card.pack_propagate(False)

result_label = tk.Label(
    result_card,
    text="Result will appear here",
    font=("Helvetica", 14, "bold"),
    bg="white",
    fg="#27ae60",
    justify="center"
)
result_label.pack(expand=True)

window.mainloop()
