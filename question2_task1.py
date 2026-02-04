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
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid integers")
        return

    root = HydroNode(root_val)
    root.left = HydroNode(left_val)
    root.right = HydroNode(right_val)

    calculator = MaxPowerCalculator()
    result = calculator.calculate_max_power(root)

    result_label.config(text=f"Maximum Net Power: {result}")

window = tk.Tk()
window.title("Hydro Power Calculator")
window.geometry("420x380")
window.configure(bg="#f4f6f8")
window.resizable(False, False)

tk.Label(
    window,
    text="Maximum Net Power Calculator",
    font=("Helvetica", 18, "bold"),
    bg="#f4f6f8",
    fg="#2c3e50"
).pack(pady=15)

card = tk.Frame(window, bg="white")
card.pack(padx=20, pady=10, fill="x")

def input_row(text, row):
    tk.Label(
        card,
        text=text,
        bg="white",
        fg="#555",
        font=("Helvetica", 11)
    ).grid(row=row, column=0, padx=15, pady=10, sticky="w")

input_row("Root Node Power", 0)
input_row("Left Child Power", 1)
input_row("Right Child Power", 2)

root_entry = tk.Entry(card, width=15, font=("Helvetica", 11), relief="groove")
left_entry = tk.Entry(card, width=15, font=("Helvetica", 11), relief="groove")
right_entry = tk.Entry(card, width=15, font=("Helvetica", 11), relief="groove")

root_entry.grid(row=0, column=1, padx=15)
left_entry.grid(row=1, column=1, padx=15)
right_entry.grid(row=2, column=1, padx=15)

# Default values
root_entry.insert(0, "1")
left_entry.insert(0, "2")
right_entry.insert(0, "3")

tk.Button(
    window,
    text="Calculate",
    font=("Helvetica", 12, "bold"),
    bg="#3498db",
    fg="white",
    activebackground="#2980b9",
    relief="flat",
    padx=20,
    pady=8,
    command=calculate
).pack(pady=20)

result_card = tk.Frame(window, bg="white", height=90)
result_card.pack(padx=20, pady=10, fill="x")
result_card.pack_propagate(False)

result_label = tk.Label(
    result_card,
    text="Maximum Net Power will appear here",
    font=("Helvetica", 16, "bold"),
    bg="white",
    fg="#27ae60",
    wraplength=360,
    justify="center"
)
result_label.pack(expand=True)

window.mainloop()
