import tkinter as tk
from tkinter import ttk, messagebox

def max_profit(max_trades, daily_prices):
    if not daily_prices or max_trades == 0:
        return 0
    n = len(daily_prices)

    if max_trades >= n // 2:
        profit = 0
        for i in range(1, n):
            if daily_prices[i] > daily_prices[i - 1]:
                profit += daily_prices[i] - daily_prices[i - 1]
        return profit

    buy = [-float('inf')] * (max_trades + 1)
    sell = [0] * (max_trades + 1)

    for price in daily_prices:
        for t in range(1, max_trades + 1):
            buy[t] = max(buy[t], sell[t - 1] - price)
            sell[t] = max(sell[t], buy[t] + price)
    return sell[max_trades]

def calculate_profit():
    try:
        k = int(trades_entry.get())
        prices_str = prices_entry.get()
        prices = [int(p.replace(",", "").strip()) for p in prices_str.split(",") if p.strip()]
        if not prices:
            raise ValueError("Empty prices")
        profit = max_profit(k, prices)
        result_label.config(text=f"NPR {profit:,}", fg="#2ecc71")
        status_label.config(text="Calculation successful.", fg="#7f8c8d")
    except ValueError:
        messagebox.showerror(
            "Input Error",
            "Please enter valid numbers.\nFormat: 2000,4000,1000"
        )
        status_label.config(text="Error: Invalid input.", fg="#e74c3c")

root = tk.Tk()
root.title("AgriTrade Optimizer")
root.geometry("520x500")
root.configure(bg="#ffffff")

style = ttk.Style()
style.theme_use('clam') 
style.configure("TEntry", padding=5)

header_frame = tk.Frame(root, bg="#2c3e50", height=80)
header_frame.pack(fill="x")

tk.Label(
    header_frame, text="AgriTrade Pro", 
    font=("Segoe UI", 20, "bold"), bg="#2c3e50", fg="white"
).pack(pady=(15, 0))

tk.Label(
    header_frame, text="Max Transaction Optimization", 
    font=("Segoe UI", 9), bg="#2c3e50", fg="#bdc3c7"
).pack(pady=(0, 15))

main_container = tk.Frame(root, bg="white", padx=30, pady=20)
main_container.pack(fill="both", expand=True)

tk.Label(main_container, text="MAXIMUM TRADES (K)", font=("Segoe UI", 9, "bold"), bg="white", fg="#7f8c8d").pack(anchor="w")
trades_entry = ttk.Entry(main_container, font=("Segoe UI", 11))
trades_entry.pack(fill="x", pady=(5, 15))
trades_entry.insert(0, "2")

tk.Label(main_container, text="PRICE SEQUENCE (Comma Separated)", font=("Segoe UI", 9, "bold"), bg="white", fg="#7f8c8d").pack(anchor="w")
prices_entry = ttk.Entry(main_container, font=("Segoe UI", 11))
prices_entry.pack(fill="x", pady=(5, 20))
prices_entry.insert(0, "2000,4000,1000")

def on_enter(e):
    calc_btn['background'] = '#2980b9'
def on_leave(e):
    calc_btn['background'] = '#3498db'

calc_btn = tk.Button(
    main_container, text="CALCULATE PROFIT", font=("Segoe UI", 11, "bold"),
    bg="#3498db", fg="white", relief="flat", cursor="hand2",
    activebackground="#2980b9", activeforeground="white",
    command=calculate_profit, pady=10
)
calc_btn.pack(fill="x")
calc_btn.bind("<Enter>", on_enter)
calc_btn.bind("<Leave>", on_leave)

result_container = tk.Frame(main_container, bg="#f9f9f9", pady=20, highlightthickness=1, highlightbackground="#ecf0f1", height=150)
result_container.pack(fill="x", pady=20)
result_container.pack_propagate(False)

tk.Label(result_container, text="TOTAL ESTIMATED PROFIT", font=("Segoe UI", 9), bg="#f9f9f9", fg="#95a5a6").pack(pady=(0,5))
result_label = tk.Label(result_container, text="NPR 0", font=("Segoe UI", 28, "bold"), bg="#f9f9f9", fg="#2c3e50", wraplength=480, justify="center")
result_label.pack(expand=True)

status_label = tk.Label(root, text="Ready to calculate", font=("Segoe UI", 8), bg="#ffffff", fg="#bdc3c7")
status_label.pack(side="bottom", pady=5)

root.mainloop()
