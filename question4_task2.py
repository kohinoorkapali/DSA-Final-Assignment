import tkinter as tk
from tkinter import ttk, messagebox

# ---------------- Logic for Task 2 ---------------- #
def allocate_energy():
    # Clear previous table entries
    for item in tree_alloc.get_children():
        tree_alloc.delete(item)
    
    try:
        # --- Parse Demand ---
        demand_lines = hourly_demand_text.get("1.0", tk.END).strip().splitlines()
        demand_data = []
        for line in demand_lines:
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 4:
                h, a, b, c = map(int, parts)
                demand_data.append({"hour": h, "A": a, "B": b, "C": c})
        
        # --- Parse Sources ---
        source_lines = sources_text.get("1.0", tk.END).strip().splitlines()
        sources = []
        for line in source_lines:
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 5:
                start, end = map(int, parts[3].split("-"))
                sources.append({
                    "id": parts[0],
                    "type": parts[1],
                    "max_capacity": int(parts[2]),
                    "start": start,
                    "end": end,
                    "cost": float(parts[4])
                })
        
        # --- Allocation per Hour ---
        for d in demand_data:
            hour = d["hour"]
            allocation = {"A": 0, "B": 0, "C": 0}
            remaining = d.copy()
            remaining.pop("hour")
            
            # Get available sources for this hour, sorted by cheapest cost
            available_sources = [s for s in sources if s["start"] <= hour <= s["end"]]
            available_sources.sort(key=lambda x: x["cost"])
            
            # Allocate energy greedily
            for s in available_sources:
                cap = s["max_capacity"]
                for district in ["A", "B", "C"]:
                    if remaining[district] > 0 and cap > 0:
                        take = min(remaining[district], cap)
                        allocation[district] += take
                        remaining[district] -= take
                        cap -= take
            
            # Insert into table
            tree_alloc.insert("", "end", values=(
                f"Hour {hour}", allocation["A"], allocation["B"], allocation["C"]
            ))
        
        status_label.config(text="✔ Hourly Allocation Completed", fg="#27ae60")
    
    except Exception as e:
        messagebox.showerror("Error", f"Check input format.\n{e}")
        status_label.config(text="✘ Error in Allocation", fg="#e74c3c")

# ---------------- Tkinter UI ---------------- #
root = tk.Tk()
root.title("Task 2 | Hourly Energy Allocation")
root.geometry("750x650")
root.configure(bg="#f4f7f6")

# --- Header ---
header = tk.Frame(root, bg="#34495e", pady=15)
header.pack(fill="x")
tk.Label(header, text="Hourly Energy Allocation (Task 2)", font=("Segoe UI", 16, "bold"),
         bg="#34495e", fg="white").pack()

# --- Input Frame ---
main_frame = tk.Frame(root, bg="#f4f7f6", padx=20, pady=10)
main_frame.pack(fill="both", expand=True)

# Demand Input
tk.Label(main_frame, text="HOURLY DEMAND (Hour,A,B,C)", font=("Segoe UI", 9, "bold"),
         bg="#f4f7f6", fg="#7f8c8d").pack(anchor="w")
demand_frame = tk.Frame(main_frame, bg="white", highlightthickness=1, highlightbackground="#dcdde1")
demand_frame.pack(fill="x", pady=(5,10))
hourly_demand_text = tk.Text(demand_frame, height=5, font=("Consolas",11), padx=10, pady=5)
hourly_demand_text.pack(fill="x")
hourly_demand_text.insert(tk.END, "6, 20, 15, 25\n7, 18, 20, 22\n8, 25, 15, 20")

# Source Input
tk.Label(main_frame, text="ENERGY SOURCES (ID,Type,MaxCap,Start-End,Cost)", font=("Segoe UI",9,"bold"),
         bg="#f4f7f6", fg="#7f8c8d").pack(anchor="w")
source_frame = tk.Frame(main_frame, bg="white", highlightthickness=1, highlightbackground="#dcdde1")
source_frame.pack(fill="x", pady=(5,10))
sources_text = tk.Text(source_frame, height=5, font=("Consolas",11), padx=10, pady=5)
sources_text.pack(fill="x")
sources_text.insert(tk.END, "S1, Solar, 50, 6-18, 1.0\nS2, Hydro, 40, 0-23, 1.5\nS3, Diesel, 60, 17-23, 3.0")

# --- Action Button ---
btn_allocate = tk.Button(main_frame, text="ALLOCATE ENERGY", font=("Segoe UI",11,"bold"),
                         bg="#3498db", fg="white", relief="flat", cursor="hand2",
                         padx=20, pady=10, command=allocate_energy)
btn_allocate.pack(fill="x", pady=10)

# --- Allocation Table ---
tk.Label(main_frame, text="HOURLY ENERGY ALLOCATION", font=("Segoe UI",9,"bold"),
         bg="#f4f7f6", fg="#7f8c8d").pack(anchor="w", pady=(10,0))

columns = ("hour", "A", "B", "C")
tree_alloc = ttk.Treeview(main_frame, columns=columns, show="headings", height=8)
for col, text in zip(columns, ["Hour", "Sector A", "Sector B", "Sector C"]):
    tree_alloc.heading(col, text=text)
    tree_alloc.column(col, width=150, anchor="center")
tree_alloc.pack(fill="x", pady=5)

# --- Status Label ---
status_label = tk.Label(root, text="Ready", font=("Segoe UI",9), bg="#f4f7f6", fg="#95a5a6")
status_label.pack(pady=10)

root.mainloop()
