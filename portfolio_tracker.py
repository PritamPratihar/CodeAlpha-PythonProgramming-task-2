# # 📈 Stock Portfolio Tracker (with Profit/Loss, Live Price Fetch & Graphs)
# 📊 Stock Portfolio Tracker - GUI Version with Colors & Graphs

# 📈 Stock Portfolio Tracker (with Profit/Loss, Live Price Fetch, Graphs & Download)
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import csv

# ====================== STOCK DATA (Static Backup) ======================
# If yfinance fails, these backup prices will be used
prices = {
    "AAPL": 180.0,   # Apple Inc.
    "TSLA": 250.0,   # Tesla, Inc.
    "MSFT": 300.0,   # Microsoft Corporation
    "GOOG": 140.0,   # Alphabet Inc. (Google)
    "AMZN": 120.0,   # Amazon.com, Inc.
    "META": 280.0,   # Meta Platforms, Inc. (Facebook)
    "NFLX": 400.0,   # Netflix, Inc.
    "NVDA": 480.0    # NVIDIA Corporation
}

# Global portfolio list to store all holdings
holdings = []
graph_canvas = None   # to keep track of matplotlib canvas


# ====================== HELPER FUNCTIONS ======================

def get_live_price(symbol):
    """Fetch live stock price from Yahoo Finance. If not found, use backup prices."""
    try:
        data = yf.Ticker(symbol)
        live_price = data.history(period="1d")["Close"].iloc[0]
        return float(live_price)
    except:
        return prices.get(symbol, None)


def add_stock():
    """Add stock details entered by user into holdings list"""
    symbol = entry_symbol.get().upper()
    try:
        qty = float(entry_qty.get())
        buy_price = float(entry_buy.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Enter valid numbers for Quantity and Buy Price")
        return

    # Get current market price
    current_price = get_live_price(symbol)

    # If not available, check manual entry
    if current_price is None:
        if entry_current.get().strip():
            try:
                current_price = float(entry_current.get())
            except ValueError:
                messagebox.showerror("Invalid Input", "Enter valid number for Current Price")
                return
        else:
            messagebox.showwarning("No Price", f"No price found for {symbol}, enter Current Price manually")
            return

    # Financial calculations
    investment = qty * current_price
    total_invested = qty * buy_price
    pnl = (current_price - buy_price) * qty
    status = "Profit" if pnl > 0 else "Loss" if pnl < 0 else "No Change"

    # Generate unique 6-digit stock ID
    stock_id = random.randint(100000, 999999)

    # Append to holdings list
    holdings.append({
        "id": stock_id,
        "symbol": symbol,
        "quantity": qty,
        "buy_price": buy_price,
        "current_price": current_price,
        "investment": investment,
        "total_invested": total_invested,
        "pnl": pnl,
        "status": status
    })

    update_table()


def update_table():
    """Refresh stock table with updated portfolio data"""
    # Clear old rows
    for row in table.get_children():
        table.delete(row)

    # Add updated rows
    for h in holdings:
        color = "green" if h["pnl"] > 0 else "red" if h["pnl"] < 0 else "black"
        table.insert("", "end",
                     values=(h["id"], h["symbol"], h["quantity"],
                             f"{h['buy_price']:.2f}", f"{h['current_price']:.2f}",
                             f"{h['total_invested']:.2f}", f"{h['investment']:.2f}",
                             f"{h['pnl']:.2f}", h["status"]),
                     tags=(color,))

    # Update portfolio summary (total values)
    total_invested = sum(h["total_invested"] for h in holdings)
    total_value = sum(h["investment"] for h in holdings)
    total_pnl = sum(h["pnl"] for h in holdings)
    status = "Profit" if total_pnl > 0 else "Loss" if total_pnl < 0 else "No Change"

    lbl_summary.config(
        text=f"💰 Invested: {total_invested:.2f} | Value: {total_value:.2f} | "
             f"PnL: {total_pnl:.2f} ({status})",
        fg="green" if total_pnl > 0 else "red" if total_pnl < 0 else "black"
    )


def delete_stock():
    """Delete selected stock from table & holdings"""
    selected = table.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a stock to delete")
        return

    item = table.item(selected[0])
    stock_id = int(item["values"][0])

    # Remove from holdings
    for h in holdings:
        if h["id"] == stock_id:
            holdings.remove(h)
            break

    update_table()
    messagebox.showinfo("Deleted", f"Stock ID {stock_id} deleted successfully!")


def search_stock():
    """Search stock ONLY by ID and highlight in table"""
    query = entry_search.get().strip()
    if not query.isdigit():
        messagebox.showwarning("Invalid Input", "Search only by 6-digit Stock ID")
        return

    found = None
    for item in table.get_children():
        stock_id = str(table.item(item)["values"][0])
        if query == stock_id:
            found = item
            break

    if found:
        table.selection_set(found)
        table.see(found)
        messagebox.showinfo("Found", f"Stock found: {table.item(found)['values']}")
    else:
        messagebox.showerror("Not Found", f"No stock with ID: {query}")


def show_graphs():
    """Show portfolio allocation and Profit/Loss graphs"""
    global graph_canvas
    if not holdings:
        messagebox.showwarning("No Data", "No holdings to plot")
        return

    # Remove previous graph if exists
    if graph_canvas:
        graph_canvas.get_tk_widget().destroy()

    labels = [h["symbol"] for h in holdings]
    investments = [h["investment"] for h in holdings]
    pnl_values = [h["pnl"] for h in holdings]

    fig, ax = plt.subplots(1, 2, figsize=(10, 5))

    # Pie chart (portfolio allocation)
    ax[0].pie(investments, labels=labels, autopct="%.1f%%", startangle=140)
    ax[0].set_title("Portfolio Allocation")

    # Bar chart (PnL with green/red bars)
    colors = ["green" if x > 0 else "red" for x in pnl_values]
    bars = ax[1].bar(labels, pnl_values, color=colors)
    for bar, val in zip(bars, pnl_values):
        ax[1].text(bar.get_x() + bar.get_width() / 2,
                   bar.get_height() + (5 if val >= 0 else -15),
                   f"{val:.2f}", ha="center",
                   va="bottom" if val >= 0 else "top",
                   color="black", fontweight="bold")

    ax[1].set_title("Profit/Loss per Stock")
    ax[1].set_xlabel("Stocks")
    ax[1].set_ylabel("PnL")

    # Embed matplotlib graph in Tkinter
    graph_canvas = FigureCanvasTkAgg(fig, master=root)
    graph_canvas.draw()
    graph_canvas.get_tk_widget().pack(pady=15)


def download_data():
    """Download portfolio data as CSV or TXT file"""
    if not holdings:
        messagebox.showwarning("No Data", "No holdings to download")
        return

    filetypes = [("CSV File", "*.csv"), ("Text File", "*.txt")]
    file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=filetypes)

    if not file:
        return

    # Save as CSV
    if file.endswith(".csv"):
        with open(file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Symbol", "Qty", "Buy Price", "Current Price",
                             "Invested", "Value", "PnL", "Status"])
            for h in holdings:
                writer.writerow([h["id"], h["symbol"], h["quantity"],
                                 h["buy_price"], h["current_price"],
                                 h["total_invested"], h["investment"],
                                 h["pnl"], h["status"]])
    # Save as TXT
    else:
        with open(file, "w") as f:
            for h in holdings:
                f.write(f"ID: {h['id']} | Symbol: {h['symbol']} | Qty: {h['quantity']} | "
                        f"Buy: {h['buy_price']:.2f} | Current: {h['current_price']:.2f} | "
                        f"Invested: {h['total_invested']:.2f} | Value: {h['investment']:.2f} | "
                        f"PnL: {h['pnl']:.2f} | Status: {h['status']}\n")

    messagebox.showinfo("Download Complete", f"Portfolio saved as {file}")


# ====================== GUI LAYOUT ======================
root = tk.Tk()
root.title("📈 Stock Portfolio Tracker")
root.geometry("1150x720")
root.configure(bg="#f4f4f9")   # Light background color

# ---------- Input Frame ----------
frame_input = tk.Frame(root, bg="#e6f0fa", pady=10)
frame_input.pack(fill="x")

# Input fields
tk.Label(frame_input, text="Stock Symbol:", bg="#e6f0fa").grid(row=0, column=0, padx=5)
entry_symbol = tk.Entry(frame_input)
entry_symbol.grid(row=0, column=1, padx=5)

tk.Label(frame_input, text="Quantity:", bg="#e6f0fa").grid(row=0, column=2, padx=5)
entry_qty = tk.Entry(frame_input)
entry_qty.grid(row=0, column=3, padx=5)

tk.Label(frame_input, text="Buy Price:", bg="#e6f0fa").grid(row=0, column=4, padx=5)
entry_buy = tk.Entry(frame_input)
entry_buy.grid(row=0, column=5, padx=5)

tk.Label(frame_input, text="Current Price (optional):", bg="#e6f0fa").grid(row=0, column=6, padx=5)
entry_current = tk.Entry(frame_input)
entry_current.grid(row=0, column=7, padx=5)

# Buttons (modern colors)
btn_add = tk.Button(frame_input, text="➕ Add Stock", command=add_stock, bg="#4CAF50", fg="white")
btn_add.grid(row=0, column=8, padx=10)

btn_graph = tk.Button(frame_input, text="📊 Show Graphs", command=show_graphs, bg="#2196F3", fg="white")
btn_graph.grid(row=0, column=9, padx=10)

# Search
tk.Label(frame_input, text="🔍 Search (ID only):", bg="#e6f0fa").grid(row=0, column=10, padx=5)
entry_search = tk.Entry(frame_input)
entry_search.grid(row=0, column=11, padx=5)

btn_search = tk.Button(frame_input, text="Search", command=search_stock, bg="#9C27B0", fg="white")
btn_search.grid(row=0, column=12, padx=10)

btn_delete = tk.Button(frame_input, text="❌ Delete Stock", command=delete_stock, bg="#f44336", fg="white")
btn_delete.grid(row=0, column=13, padx=10)

# ---------- Table ----------
columns = ("ID", "Symbol", "Qty", "Buy Price", "Current Price", "Invested", "Value", "PnL", "Status")
table = ttk.Treeview(root, columns=columns, show="headings", height=12)

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=110)

table.tag_configure("green", foreground="green")
table.tag_configure("red", foreground="red")
table.pack(pady=10, fill="x")

# ---------- Summary & Download ----------
frame_summary = tk.Frame(root, bg="#f4f4f9")
frame_summary.pack(pady=10)

lbl_summary = tk.Label(frame_summary, text="💰 Invested: 0 | Value: 0 | PnL: 0",
                       font=("Arial", 12, "bold"), bg="#f4f4f9")
lbl_summary.pack(pady=5)

btn_download = tk.Button(frame_summary, text="⬇️ Download", command=download_data, bg="#FF9800", fg="white")
btn_download.pack(pady=5)

# Run application
root.mainloop()
  
