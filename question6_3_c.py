import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque

# Graph with capacities
capacity = {
    'KTM': {'JA': 10, 'JB': 15},
    'JA': {'KTM': 0, 'PH': 8, 'BS': 5},
    'JB': {'KTM': 0, 'JA': 4, 'BS': 12},
    'PH': {'JA': 8, 'BS': 6},
    'BS': {'JA': 5, 'JB': 12, 'PH': 6}
}

# --- Logic Section ---
def bfs(residual, source, sink, parent):
    visited = set()
    queue = deque([source])
    visited.add(source)
    while queue:
        u = queue.popleft()
        for v in residual.get(u, {}):
            if v not in visited and residual[u][v] > 0:
                visited.add(v)
                parent[v] = u
                if v == sink:
                    return True
                queue.append(v)
    return False

def edmonds_karp(capacity, source, sink):
    residual = {u: dict(v) for u, v in capacity.items()}
    parent = {}
    max_flow = 0
    while bfs(residual, source, sink, parent):
        path_flow = float('inf')
        s = sink
        while s != source:
            path_flow = min(path_flow, residual[parent[s]][s])
            s = parent[s]
        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= path_flow
            residual[v][u] = residual.get(v, {}).get(u, 0) + path_flow
            v = u
        max_flow += path_flow
        parent = {}
    return max_flow

def calculate_max_flow():
    source = source_var.get()
    sink = sink_var.get()
    if source not in capacity or sink not in capacity:
        messagebox.showerror("Selection Error", "Please select valid locations.")
        return
    if source == sink:
        messagebox.showwarning("Logic Error", "Source and Destination cannot be the same.")
        return
    
    flow_val = edmonds_karp(capacity, source, sink)
    
    # Update the UI result display
    res_title_label.config(text=f"OPTIMIZED THROUGHPUT: {source} → {sink}")
    res_value_label.config(text=f"{flow_val} Trucks / Hour")

# --- UI Setup ---
root = tk.Tk()
root.title("RescueRoute | Throughput Optimizer")
root.geometry("600x450")
root.configure(bg="#1e2124")

# Styling
style = ttk.Style()
style.theme_use('clam')

# Custom Combobox Styling 
style.configure("TCombobox", fieldbackground="#2f3136", background="#42454a", foreground="black", arrowcolor="white")
root.option_add("*TCombobox*Listbox.background", "#2f3136")
root.option_add("*TCombobox*Listbox.foreground", "white")
root.option_add("*TCombobox*Listbox.selectBackground", "#7289da")

# Button Styles
style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), background="#7289da", foreground="white")
style.map("Action.TButton", background=[('active', '#5b6eae')])

# Main Layout
main_frame = tk.Frame(root, bg="#1e2124", padx=40, pady=30)
main_frame.pack(fill=tk.BOTH, expand=True)

# Title & Description
tk.Label(main_frame, text="THROUGHPUT OPTIMIZER", font=("Segoe UI", 18, "bold"), bg="#1e2124", fg="#7289da").pack()
tk.Label(main_frame, text="Calculate maximum logistics capacity between nodes", font=("Segoe UI", 9), bg="#1e2124", fg="#b9bbbe").pack(pady=(0, 25))

# Input Card
input_card = tk.Frame(main_frame, bg="#2f3136", padx=20, pady=20, highlightbackground="#42454a", highlightthickness=1)
input_card.pack(fill=tk.X)

# Grid Layout for Inputs
input_card.columnconfigure(1, weight=1)

tk.Label(input_card, text="SOURCE BASE", font=("Segoe UI", 8, "bold"), bg="#2f3136", fg="#96989d").grid(row=0, column=0, sticky="w", pady=5)
source_var = tk.StringVar(value="KTM")
source_cb = ttk.Combobox(input_card, textvariable=source_var, values=list(capacity.keys()), state="readonly")
source_cb.grid(row=1, column=0, sticky="ew", padx=(0, 10))

tk.Label(input_card, text="DESTINATION", font=("Segoe UI", 8, "bold"), bg="#2f3136", fg="#96989d").grid(row=0, column=1, sticky="w", pady=5)
sink_var = tk.StringVar(value="BS")
sink_cb = ttk.Combobox(input_card, textvariable=sink_var, values=list(capacity.keys()), state="readonly")
sink_cb.grid(row=1, column=1, sticky="ew")

calc_btn = ttk.Button(main_frame, text="RUN ANALYSIS", style="Action.TButton", command=calculate_max_flow)
calc_btn.pack(pady=25, fill=tk.X)

# Results Display Card
result_card = tk.Frame(main_frame, bg="#36393f", padx=20, pady=20)
result_card.pack(fill=tk.BOTH, expand=True)

res_title_label = tk.Label(result_card, text="RESULTS WILL APPEAR HERE", font=("Segoe UI", 9, "bold"), bg="#36393f", fg="#b9bbbe")
res_title_label.pack()

res_value_label = tk.Label(result_card, text="0 Units", font=("Segoe UI", 16, "bold"), bg="#36393f", fg="#43b581")
res_value_label.pack(pady=5)

root.mainloop()