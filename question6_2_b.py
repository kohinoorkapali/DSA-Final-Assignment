import tkinter as tk
from tkinter import ttk, messagebox
import heapq
import math

# Graph with safety probabilities
graph = {
    "KTM": [("JA", 0.9), ("JB", 0.8)],
    "JA": [("KTM", 0.9), ("PH", 0.95), ("BS", 0.7)],
    "JB": [("KTM", 0.8), ("JA", 0.6), ("BS", 0.9)],
    "PH": [("JA", 0.95), ("BS", 0.85)],
    "BS": [("JA", 0.7), ("JB", 0.9), ("PH", 0.85)]
}

def safest_path(graph, source):
    dist = {node: float('inf') for node in graph}
    dist[source] = 0
    parent = {}
    pq = [(0, source)]

    while pq:
        curr_dist, u = heapq.heappop(pq)
        for v, prob in graph[u]:
            weight = -math.log(prob)
            if dist[v] > curr_dist + weight:
                dist[v] = curr_dist + weight
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))
    safety = {node: math.exp(-dist[node]) for node in dist}
    return safety, parent

def show_safest_path():
    source = source_var.get()
    safety, parent = safest_path(graph, source)
    
    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"  SAFEST PATHS FROM: {source}\n", "header_tag")
    output_text.insert(tk.END, "━" * 50 + "\n\n")
    
    for node in sorted(graph.keys()):
        path = []
        current = node
        while current != source:
            path.append(current)
            current = parent.get(current, source)
            if current == source:
                path.append(source)
                break
        path.reverse()
        path_str = " ➔ ".join(path)
        output_text.insert(tk.END, f"📍 To {node}:\n", "node_tag")
        output_text.insert(tk.END, f"   Path:   {path_str}\n")
        output_text.insert(tk.END, f"   Safety: {safety[node]*100:.2f}%\n\n", "prob_tag")
    output_text.config(state=tk.DISABLED)

def reset_output():
    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.config(state=tk.DISABLED)

# --- UI Setup ---
root = tk.Tk()
root.title("RescueRoute | Emergency Logistics")
root.geometry("750x600")
root.configure(bg="#1e2124")

style = ttk.Style()
style.theme_use('clam')

# Fix for Combobox visibility
style.configure("TCombobox", 
                fieldbackground="#2f3136", 
                background="#42454a", 
                foreground="black", 
                arrowcolor="white")

# This specifically targets the dropdown list colors
root.option_add("*TCombobox*Listbox.background", "#2f3136")
root.option_add("*TCombobox*Listbox.foreground", "black")
root.option_add("*TCombobox*Listbox.selectBackground", "#1b45e0")
root.option_add("*TCombobox*Listbox.selectForeground", "white")

style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
style.configure("Action.TButton", background="#7289da", foreground="white")
style.map("Action.TButton", background=[('active', '#5b6eae')])

main_frame = tk.Frame(root, bg="#1e2124", padx=30, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)

title_lbl = tk.Label(main_frame, text="RESCUE ROUTE", font=("Segoe UI", 24, "bold"), bg="#1e2124", fg="#7289da")
title_lbl.pack()

# Control Panel
control_panel = tk.Frame(main_frame, bg="#2f3136", padx=15, pady=15, highlightbackground="#42454a", highlightthickness=1)
control_panel.pack(fill=tk.X, pady=10)

tk.Label(control_panel, text="SELECT STARTING BASE:", font=("Segoe UI", 9, "bold"), bg="#2f3136", fg="white").grid(row=0, column=0, padx=10)

source_var = tk.StringVar(value="KTM")
source_dropdown = ttk.Combobox(control_panel, textvariable=source_var, values=list(graph.keys()), state="readonly", width=15)
source_dropdown.grid(row=0, column=1, padx=10)

calc_btn = ttk.Button(control_panel, text="CALCULATE", style="Action.TButton", command=show_safest_path)
calc_btn.grid(row=0, column=2, padx=10)

reset_btn = ttk.Button(control_panel, text="RESET", command=reset_output)
reset_btn.grid(row=0, column=3, padx=10)

# Output Area
text_frame = tk.Frame(main_frame, bg="#1e2124")
text_frame.pack(fill=tk.BOTH, expand=True, pady=15)

output_text = tk.Text(text_frame, wrap=tk.WORD, state=tk.DISABLED, bg="#2f3136", fg="#dcddde", 
                     font=("Consolas", 11), padx=15, pady=15, borderwidth=0)
output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

output_text.tag_configure("header_tag", foreground="#ffffff", font=("Segoe UI", 12, "bold"))
output_text.tag_configure("node_tag", foreground="#7289da", font=("Segoe UI", 11, "bold"))
output_text.tag_configure("prob_tag", foreground="#43b581", font=("Consolas", 10, "italic"))

scrollbar = ttk.Scrollbar(text_frame, command=output_text.yview)
output_text.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

root.mainloop()