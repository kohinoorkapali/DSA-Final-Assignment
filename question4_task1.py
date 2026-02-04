import tkinter as tk
from tkinter import ttk, messagebox

def process_data():

    for item in tree_demand.get_children(): tree_demand.delete(item)
    for item in tree_source.get_children(): tree_source.delete(item)

    try:
        # Parse Demands: Hour, A, B, C
        demand_lines = hourly_demand_text.get("1.0", tk.END).strip().splitlines()
        for line in demand_lines:
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 4:
                h, a, b, c = map(int, parts)
                tree_demand.insert("", "end", values=(f"Hour {h}", a, b, c, a+b+c))

        # Parse Sources: ID, Type, Max, Time, Cost
        source_lines = sources_text.get("1.0", tk.END).strip().splitlines()
        for line in source_lines:
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 5:
                tree_source.insert("", "end", values=(parts[0], parts[1], parts[2], parts[3], parts[4]))

        status_label.config(text="✔ Data Model Loaded Successfully", fg="#27ae60")
    except Exception as e:
        messagebox.showerror("Format Error", "Use: Hour, A, B, C\nAnd: ID, Type, Max, Start-End, Cost")

def run_optimization():
    """Tasks 2-5: Greedy Allocation & Human-Readable Output"""
    for item in tree_results.get_children(): tree_results.delete(item)

    try:
        source_list = []
        for child in tree_source.get_children():
            v = tree_source.item(child)["values"]
            start, end = map(int, str(v[3]).split("-"))
            source_list.append({"id": v[0], "type": v[1], "cap": float(v[2]), "start": start, "end": end, "cost": float(v[4])})

        for child in tree_demand.get_children():
            d_vals = tree_demand.item(child)["values"]
            hour = int(str(d_vals[0]).split()[1])
            districts = {"A": float(d_vals[1]), "B": float(d_vals[2]), "C": float(d_vals[3])}
            
            # Filter and Sort by Cost (Task 3: Greedy)
            active_sources = sorted([s for s in source_list if s['start'] <= hour <= s['end']], key=lambda x: x['cost'])
            
            source_caps = {s['id']: s['cap'] for s in active_sources}
            allocation = {d: 0 for d in districts}
            breakdown = {d: [] for d in districts}

            for s in active_sources:
                for d in districts:
                    needed = districts[d] - allocation[d]
                    if needed > 0 and source_caps[s['id']] > 0:
                        grab = min(needed, source_caps[s['id']])
                        allocation[d] += grab
                        source_caps[s['id']] -= grab
                        if grab > 0:
                            # TRANSLATION LOGIC: Make S1/S2/S3 readable for the user
                            name = s['type'] 
                            breakdown[d].append(f"{name}: {int(grab)}kWh")

            for d in districts:
                target, actual = districts[d], allocation[d]
                pct = (actual / target * 100) if target > 0 else 0
                within = "Yes" if 90 <= pct <= 110 else "No"
                tree_results.insert("", "end", values=(f"{hour:02d}:00", d, target, actual, f"{pct:.1f}%", within, ", ".join(breakdown[d])))
        
        status_label.config(text="✔ Optimization Complete", fg="#2980b9")
    except Exception as e:
        messagebox.showerror("Error", f"Processing failed: {e}")

# ---------------- UI Setup ---------------- #
root = tk.Tk()
root.title("Smart Grid Optimization (Nepal)")
root.geometry("900x900")
root.configure(bg="#f4f7f6")

style = ttk.Style()
style.theme_use("clam")

header = tk.Frame(root, bg="#34495e", pady=15)
header.pack(fill="x")
tk.Label(header, text="Nepal Smart Grid Load Distribution", font=("Segoe UI", 16, "bold"), bg="#34495e", fg="white").pack()

main_frame = tk.Frame(root, bg="#f4f7f6", padx=20)
main_frame.pack(fill="both", expand=True)

# Demand Input
tk.Label(main_frame, text="INPUT HOURLY DEMAND (Hour, A, B, C)", font=("Segoe UI", 9, "bold"), bg="#f4f7f6").pack(anchor="w", pady=(10,0))
hourly_demand_text = tk.Text(main_frame, height=4, font=("Consolas", 10))
hourly_demand_text.pack(fill="x", pady=5)
hourly_demand_text.insert(tk.END, "6, 20, 15, 25\n17, 30, 35, 40\n22, 15, 10, 20")

# Source Input
tk.Label(main_frame, text="ENERGY SOURCES (ID, Type, MaxCap, Start-End, Cost)", font=("Segoe UI", 9, "bold"), bg="#f4f7f6").pack(anchor="w")
sources_text = tk.Text(main_frame, height=4, font=("Consolas", 10))
sources_text.pack(fill="x", pady=5)
sources_text.insert(tk.END, "S1, Solar, 50, 6-18, 1.0\nS2, Hydro, 40, 0-24, 1.5\nS3, Diesel, 60, 17-23, 3.0")

# Buttons
btn_frame = tk.Frame(main_frame, bg="#f4f7f6")
btn_frame.pack(fill="x", pady=10)
tk.Button(btn_frame, text="LOAD DATA MODEL", command=process_data, bg="#3498db", fg="white", font=("Segoe UI", 10, "bold"), width=20).pack(side="left", padx=5)
tk.Button(btn_frame, text="RUN OPTIMIZATION", command=run_optimization, bg="#27ae60", fg="white", font=("Segoe UI", 10, "bold"), width=20).pack(side="left", padx=5)

# Tables
tree_demand = ttk.Treeview(main_frame, columns=("h", "a", "b", "c", "t"), show="headings", height=3)
for col, txt in zip(("h", "a", "b", "c", "t"), ["Time", "Sec A", "Sec B", "Sec C", "Total"]):
    tree_demand.heading(col, text=txt); tree_demand.column(col, width=80, anchor="center")
tree_demand.pack(fill="x", pady=5)

tree_source = ttk.Treeview(main_frame, columns=("i", "t", "m", "h", "c"), show="headings", height=3)
for col, txt in zip(("i", "t", "m", "h", "c"), ["ID", "Type", "Max", "Hours", "Cost"]):
    tree_source.heading(col, text=txt); tree_source.column(col, width=80, anchor="center")
tree_source.pack(fill="x", pady=5)

# Results (Task 5 Output)
tk.Label(main_frame, text="TASK 5: OPTIMIZED RESULTS TABLE", font=("Segoe UI", 10, "bold"), fg="#2c3e50").pack(anchor="w", pady=(10,0))
tree_results = ttk.Treeview(main_frame, columns=("hr", "dst", "dem", "act", "pct", "win", "brk"), show="headings", height=8)
for col, txt in zip(("hr", "dst", "dem", "act", "pct", "win", "brk"), ["Hour", "District", "Demand", "Actual", "% Fill", "OK?", "Source Breakdown"]):
    tree_results.heading(col, text=txt); tree_results.column(col, width=90 if col != "brk" else 250, anchor="center")
tree_results.pack(fill="x", pady=10)

status_label = tk.Label(root, text="Ready", font=("Segoe UI", 9), bg="#f4f7f6")
status_label.pack(side="bottom", pady=5)

root.mainloop()