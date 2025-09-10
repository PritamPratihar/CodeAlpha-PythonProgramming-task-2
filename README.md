# CodeAlpha-PythonProgramming-task-2
this is my intership task  no 2.


# 📈 Stock Portfolio Tracker

A simple **Tkinter GUI** app to track stock holdings, fetch live prices (using `yfinance`), show profit/loss, plot graphs, and export portfolio data.

---

## Features

* Add stocks with **symbol**, **quantity**, and **buy price**.
* Fetch **live current price** from Yahoo Finance (`yfinance`) with a static backup price map if fetching fails.
* Calculate **Invested**, **Current Value**, and **PnL (Profit / Loss)** per stock and for the full portfolio.
* Show **Portfolio Allocation** (pie chart) and **PnL per stock** (bar chart) using `matplotlib`.
* Search holdings by **6-digit ID** and **delete** selected entries.
* Export portfolio to **CSV** or **TXT**.

---

## Requirements

* Python 3.8+
* Packages:

  * `yfinance`
  * `matplotlib`

Note: `tkinter` is part of the standard library but some Linux distributions require a separate package (e.g. `sudo apt install python3-tk`).

Install dependencies with pip:

```bash
pip install yfinance matplotlib
```

---

## Run the App

1. Save the provided Python script as `portfolio_tracker.py` (or any name you like).
2. Run:

```bash
python portfolio_tracker.py
```

The GUI window will open. Fill the input fields and use the buttons to add, graph, search, delete, or download your holdings.

---

## Important Notes & Tips

* The app tries to fetch the latest close price for the given ticker symbol. If Yahoo Finance fails or returns no data, the app uses a built-in `prices` backup map. You can also enter a **Current Price** manually in the input field.
* The app generates a unique 6-digit **stock ID** for each holding; use this ID for searching and deleting.
* Exported CSV can be opened in Excel or LibreOffice.

---

## Make it Git-ready (quick steps)

1. Initialize a local repo:

```bash
git init
git add portfolio_tracker.py README.md
git commit -m "Add stock portfolio tracker GUI"
```

2. Create a new GitHub repository on github.com and follow the instructions shown after creation to push your local repo (or use `gh` CLI).

Add a `.gitignore` file and exclude files like `*.csv` or environment folders.

---

## Troubleshooting

* **No GUI / tkinter error**: install `python3-tk` (Linux) or ensure Python installer included the TK option on Windows.
* **yfinance errors**: check internet connection or use the Current Price field manually.
* **Matplotlib figure not showing / embedding issue**: ensure `matplotlib` is installed and working; run a small plotting script to confirm.

---

## Want extra help?

If you want I can:

* Create a ready-to-push GitHub repo structure with a `.gitignore` and license.
* Convert the script into a single-file executable (`pyinstaller`) or add persistent storage (CSV auto-save or SQLite).

Tell me which option you prefer.
