import tkinter as tk
from tkinter import ttk, messagebox
import threading
import requests
import time

# CONFIGURATION 

API_KEY = "5a912e47afdd479eb39154741260302" 
CITIES = ["Kathmandu", "Pokhara", "Biratnagar", "Nepalgunj, NP", "Dhangadhi"]

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-threaded Weather Collector")
        self.root.geometry("1100x650")
        self.root.configure(bg="#f8f9fa")
        
        self.gui_lock = threading.Lock()
        # --- HEADER ---
        header = tk.Label(root, text="🌤️ Parallel Weather Dashboard", font=("Helvetica", 20, "bold"), 
                         bg="#34495e", fg="white", pady=20)
        header.pack(fill=tk.X)

        # --- CONTROLS ---
        self.fetch_btn = tk.Button(root, text="🚀 START DATA COLLECTION", command=self.start_fetching, 
                                  bg="#27ae60", fg="white", font=("Helvetica", 11, "bold"), 
                                  padx=25, pady=12, relief="flat", cursor="hand2")
        self.fetch_btn.pack(pady=20)

        # --- DASHBOARD LAYOUT ---
        main_frame = tk.Frame(root, bg="#f8f9fa")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)

        table_frame = tk.LabelFrame(main_frame, text=" Weather Results (Threaded) ", bg="white", padx=10, pady=10)
        table_frame.place(relx=0, rely=0, relwidth=0.52, relheight=0.9)

        columns = ("City", "Temp", "Humidity", "Pressure")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=90, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True)

        chart_frame = tk.LabelFrame(main_frame, text=" Latency: Sequential vs Parallel (ms) ", bg="white", padx=10, pady=10)
        chart_frame.place(relx=0.55, rely=0, relwidth=0.45, relheight=0.9)

        self.canvas = tk.Canvas(chart_frame, bg="white", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def fetch_city_worker(self, city):
        """Task 3: Thread-specific function for API calls"""
        try:
            url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
            response = requests.get(url, timeout=7).json()
            
            # Data extraction
            temp = f"{response['current']['temp_c']}°C"
            hum = f"{response['current']['humidity']}%"
            pres = f"{response['current']['pressure_mb']} hPa"

            with self.gui_lock:
                self.tree.insert("", tk.END, values=(city, temp, hum, pres))
        except Exception:
            with self.gui_lock:
                self.tree.insert("", tk.END, values=(city, "Error", "---", "---"))

    def start_fetching(self):
        # Reset UI
        for item in self.tree.get_children(): self.tree.delete(item)
        self.canvas.delete("all")
        self.fetch_btn.config(state=tk.DISABLED, text="⌛ COLLECTING...")
        threading.Thread(target=self.run_benchmark, daemon=True).start()

    def run_benchmark(self):


        start_seq = time.perf_counter()
        for city in CITIES:
            try: requests.get(f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}", timeout=7)
            except: pass
        seq_ms = (time.perf_counter() - start_seq) * 1000

       
        start_par = time.perf_counter()
        threads = [threading.Thread(target=self.fetch_city_worker, args=(city,)) for city in CITIES]
        for t in threads: t.start()
        for t in threads: t.join()
        par_ms = (time.perf_counter() - start_par) * 1000

        # Update GUI
        self.root.after(0, lambda: self.draw_detailed_chart(seq_ms, par_ms))
        self.root.after(0, lambda: self.fetch_btn.config(state=tk.NORMAL, text="🚀 START DATA COLLECTION"))

    def draw_detailed_chart(self, seq, par):
        self.canvas.delete("all")
        c_width = self.canvas.winfo_width()
        c_height = self.canvas.winfo_height()
        
        # Scaling
        max_val = max(seq, par)
        base_y = c_height - 60
        scale = (c_height - 120) / max_val if max_val > 0 else 1

        # Coordinates
        bar_w = 80
        x1, x2 = (c_width * 0.25), (c_width * 0.65)
        
        # Draw Sequential Bar
        h_seq = seq * scale
        self.canvas.create_rectangle(x1, base_y - h_seq, x1 + bar_w, base_y, fill="#e74c3c", outline="#c0392b", width=2)
        self.canvas.create_text(x1 + bar_w/2, base_y + 25, text="Sequential", font=("Arial", 10, "bold"))
        self.canvas.create_text(x1 + bar_w/2, base_y - h_seq - 15, text=f"{int(seq)} ms", font=("Arial", 9, "bold"), fill="#c0392b")

        # Draw Parallel Bar
        h_par = par * scale
        self.canvas.create_rectangle(x2, base_y - h_par, x2 + bar_w, base_y, fill="#2ecc71", outline="#27ae60", width=2)
        self.canvas.create_text(x2 + bar_w/2, base_y + 25, text="Parallel", font=("Arial", 10, "bold"))
        self.canvas.create_text(x2 + bar_w/2, base_y - h_par - 15, text=f"{int(par)} ms", font=("Arial", 9, "bold"), fill="#27ae60")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()