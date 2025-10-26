import pandas as pd
from datetime import datetime
import os

DATA_FILE = "family_expenses_10000.csv"

# --- create file if not present OR empty ---
if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
    df = pd.DataFrame(columns=["Date", "Member", "Category", "Amount", "Family_ID"])
    df.to_csv(DATA_FILE, index=False)

# --- add new expense ---
def add_expense(member, category, amount, family_id):
    """Append a new expense entry to CSV."""
    df = pd.DataFrame([{
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Member": member,
        "Category": category,
        "Amount": float(amount),
        "Family_ID": family_id
    }])
    df.to_csv(DATA_FILE, mode='a', header=False, index=False)
    print(f"✅ Expense added: {member} | {category} | ₹{amount}")

# --- read all expenses ---
def read_expenses(family_id=None):
    df = pd.read_csv(DATA_FILE)
    if family_id:
        df = df[df["Family_ID"] == family_id]
    return df

# --- quick test run ---
if __name__ == "__main__":
    add_expense("Father", "Food", 450, "fam1")
    print("\n🔹 Family Expenses:")
    print(read_expenses("fam1").head())

# --- auto-generate expenses ---
def auto_generate_expenses(family_count=5, users_per_family=10):
    import random
    categories = ["Food", "Travel", "Bills", "Entertainment", "Shopping"]
    
    # Ensure CSV has proper columns
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        df = pd.DataFrame(columns=["Date", "Member", "Category", "Amount", "Family_ID"])
        df.to_csv(DATA_FILE, index=False)
    
    for f in range(1, family_count + 1):
        family_id = f"fam{f}"
        for u in range(1, users_per_family + 1):
            member = f"user{u}_fam{f}"
            for _ in range(random.randint(3,6)):
                category = random.choice(categories)
                amount = random.randint(50, 2000)
                add_expense(member, category, amount, family_id)
