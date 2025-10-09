# visualize.py
import pandas as pd
import matplotlib.pyplot as plt
import os

DATA_FILE = "family_expenses_10000.csv"
CHART_FOLDER = "charts"

if not os.path.exists(CHART_FOLDER):
    os.makedirs(CHART_FOLDER)

# --- Bar chart per family ---
def bar_chart_family(family_id):
    df = pd.read_csv(DATA_FILE)
    df = df[df["Family_ID"]==family_id]
    summary = df.groupby("Member")["Amount"].sum()
    if not summary.empty:
        summary.plot(kind="bar", title=f"Family {family_id} Spending")
        plt.ylabel("Amount (₹)")
        plt.savefig(f"{CHART_FOLDER}/bar_{family_id}.png")
        plt.close()

# --- Pie chart per member ---
def pie_chart_member(member, family_id):
    df = pd.read_csv(DATA_FILE)
    df = df[(df["Family_ID"]==family_id) & (df["Member"]==member)]
    summary = df.groupby("Category")["Amount"].sum()
    if not summary.empty:
        summary.plot(kind="pie", title=f"{member} Spending by Category", autopct='%1.1f%%')
        plt.ylabel("")
        plt.savefig(f"{CHART_FOLDER}/pie_{member}_{family_id}.png")
        plt.close()
