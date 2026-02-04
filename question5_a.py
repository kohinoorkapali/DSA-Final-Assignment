import tkinter as tk
from tkinter import messagebox, ttk
import itertools
import time

#  DATASET
spots = [
    {"name": "Pashupatinath", "lat": 27.7104, "lon": 85.3488, "fee": 100, "tags": ["culture", "religious"]},
    {"name": "Swayambhunath", "lat": 27.7149, "lon": 85.2906, "fee": 200, "tags": ["culture", "heritage"]},
    {"name": "Garden of Dreams", "lat": 27.7125, "lon": 85.3170, "fee": 150, "tags": ["nature", "relaxation"]},
    {"name": "Chandragiri Hills", "lat": 27.6616, "lon": 85.2458, "fee": 700, "tags": ["nature", "adventure"]},
    {"name": "Durbar Square", "lat": 27.7048, "lon": 85.3076, "fee": 100, "tags": ["culture", "heritage"]}
]


unique_tags = sorted(list(set(tag for s in spots for tag in s['tags'])))

class TouristOptimizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tourist Spot Optimizer Pro")
        self.root.geometry("1100x750")
        self.root.configure(bg="#f5f7fa")

        # --- HEADER ---
        header = tk.Label(root, text="🗺️ Tourist Path Optimizer", font=("Helvetica", 20, "bold"), 
                         bg="#3498db", fg="white", pady=20)
        header.pack(fill=tk.X)

        # INPUT SECTION (Dropdowns and Entries)
        input_frame = tk.Frame(root, bg="white", padx=20, pady=15, highlightthickness=1, highlightbackground="#dcdde1")
        input_frame.pack(padx=20, pady=15, fill=tk.X)

        tk.Label(input_frame, text="Time (hrs):", bg="white").grid(row=0, column=0, sticky="w")
        self.time_entry = ttk.Entry(input_frame, width=8)
        self.time_entry.insert(0, "10")
        self.time_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Budget (Rs):", bg="white").grid(row=0, column=2, sticky="w")
        self.budget_entry = ttk.Entry(input_frame, width=12)
        self.budget_entry.insert(0, "1000")
        self.budget_entry.grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Interest 1:", bg="white").grid(row=0, column=4, sticky="w")
        self.tag_cb1 = ttk.Combobox(input_frame, values=unique_tags, width=12, state="readonly")
        self.tag_cb1.set("culture")
        self.tag_cb1.grid(row=0, column=5, padx=5)

        tk.Label(input_frame, text="Interest 2:", bg="white").grid(row=0, column=6, sticky="w")
        self.tag_cb2 = ttk.Combobox(input_frame, values=unique_tags, width=12, state="readonly")
        self.tag_cb2.set("nature")
        self.tag_cb2.grid(row=0, column=7, padx=5)

        self.plan_btn = tk.Button(input_frame, text="COMPARE ALGORITHMS", command=self.calculate, 
                                 bg="#2ecc71", fg="white", font=("Helvetica", 10, "bold"), 
                                 relief="flat", padx=15, pady=5)
        self.plan_btn.grid(row=0, column=8, padx=10)

        # MAIN CONTENT 
        content_frame = tk.Frame(root, bg="#f5f7fa")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.res_box = tk.Text(content_frame, font=("Consolas", 10), bg="white", padx=10, pady=10, width=50)
        self.res_box.place(relx=0, rely=0, relwidth=0.48, relheight=1)

        self.canvas = tk.Canvas(content_frame, bg="white", highlightthickness=0)
        self.canvas.place(relx=0.52, rely=0, relwidth=0.48, relheight=1)

    def get_dist(self, p1, p2):
        return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5 * 100


    def heuristic_solve(self, max_t, max_b, user_tags):
        path, curr_pos, t_used, b_used = [], (27.7000, 85.3000), 0, 0
        available = spots.copy()
        while available:
            best_s, best_score = None, -1
            for s in available:
                dist = self.get_dist(curr_pos, (s['lat'], s['lon']))
                if (t_used + dist + 2 <= max_t) and (b_used + s['fee'] <= max_b):
                    m = len(set(user_tags) & set(s['tags']))
                    score = (m + 1) / (dist + 0.5)
                    if score > best_score:
                        best_score, best_s = score, s
            if best_s:
                dist = self.get_dist(curr_pos, (best_s['lat'], best_s['lon']))
                t_used += (dist + 2); b_used += best_s['fee']
                path.append(best_s); curr_pos = (best_s['lat'], best_s['lon'])
                available.remove(best_s)
            else: break
        return path, t_used, b_used


    def brute_force_solve(self, max_t, max_b, user_tags):
        best_p, max_m = [], -1

        for r in range(1, len(spots) + 1):
            for p in itertools.permutations(spots, r):
                t, b, m, pos = 0, 0, 0, (27.7000, 85.3000)
                valid = True
                for s in p:
                    dist = self.get_dist(pos, (s['lat'], s['lon']))
                    if (t + dist + 2 <= max_t) and (b + s['fee'] <= max_b):
                        t += (dist + 2); b += s['fee']
                        m += len(set(user_tags) & set(s['tags']))
                        pos = (s['lat'], s['lon'])
                    else:
                        valid = False; break
                if valid and m > max_m:
                    max_m, best_p = m, p
        return best_p

    def calculate(self):
        try:
            mt, mb = float(self.time_entry.get()), float(self.budget_entry.get())
            tags = [self.tag_cb1.get(), self.tag_cb2.get()]
            
            # Performance timing
            start_h = time.perf_counter()
            h_path, h_t, h_b = self.heuristic_solve(mt, mb, tags)
            h_time = time.perf_counter() - start_h

            start_bf = time.perf_counter()
            bf_path = self.brute_force_solve(mt, mb, tags)
            bf_time = time.perf_counter() - start_bf

            self.update_results(h_path, h_t, h_b, h_time, bf_path, bf_time)
            self.draw_map(h_path)
        except ValueError:
            messagebox.showerror("Error", "Invalid numeric inputs.")

    def update_results(self, h_p, h_t, h_b, h_dur, bf_p, bf_dur):
        self.res_box.delete(1.0, tk.END)
        self.res_box.insert(tk.END, "--- 1. HEURISTIC (GREEDY) ---\n", "blue")
        self.res_box.insert(tk.END, f"Spots: {len(h_p)} | Time: {h_t:.2f}h | Cost: {h_b}\n")
        self.res_box.insert(tk.END, f"Execution Time: {h_dur*1000:.4f} ms\n\n")

        self.res_box.insert(tk.END, "--- 2. BRUTE FORCE (OPTIMAL) ---\n", "green")
        self.res_box.insert(tk.END, f"Spots: {len(bf_p)}\n")
        self.res_box.insert(tk.END, f"Execution Time: {bf_dur*1000:.4f} ms\n\n")

        self.res_box.insert(tk.END, "--- 3. DISCUSSION (TASK 5) ---\n", "bold")
        acc = (len(h_p)/len(bf_p)*100) if bf_p else 100
        self.res_box.insert(tk.END, f"Accuracy: {acc:.1f}%\n")
        self.res_box.insert(tk.END, "Heuristic is O(N^2), whereas Brute Force is O(N!). ")
        self.res_box.insert(tk.END, "For 5 spots, Brute Force is fast, but for 50 spots, it would take years.")
        
        self.res_box.tag_configure("blue", foreground="#3498db", font=("Consolas", 10, "bold"))
        self.res_box.tag_configure("green", foreground="#27ae60", font=("Consolas", 10, "bold"))
        self.res_box.tag_configure("bold", font=("Consolas", 10, "bold"))

    def draw_map(self, path):
        self.canvas.delete("all")
        lx, ly = 50, 150
        self.canvas.create_oval(lx-7, ly-7, lx+7, ly+7, fill="#3498db")
        self.canvas.create_text(lx, ly+20, text="START", font=("Arial", 8, "bold"))

        for i, s in enumerate(path):
            nx, ny = lx + 130, 150 + (60 if i % 2 == 0 else -60)
            self.canvas.create_line(lx, ly, nx, ny, arrow=tk.LAST, fill="#bdc3c7", width=2)
            self.canvas.create_rectangle(nx-7, ny-7, nx+7, ny+7, fill="#e74c3c", outline="white")
            self.canvas.create_text(nx, ny-20, text=s['name'], font=("Arial", 8, "bold"))
            lx, ly = nx, ny

if __name__ == "__main__":
    root = tk.Tk()
    app = TouristOptimizerApp(root)
    root.mainloop()