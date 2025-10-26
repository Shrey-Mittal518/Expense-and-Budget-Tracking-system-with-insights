# health_score.py

import pandas as pd

DATA_FILE = "family_expenses_10000.csv"
OUTPUT_FILE = "health_scores.csv"

def compute_health_score(family_id=None):
    try:
        df = pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        return "No data available"
    
    if family_id:
        df = df[df["Family_ID"] == family_id]
    
    if df.empty:
        return "No expenses found"  # Changed from return to return a message
    
    scores = {}
    for member, grp in df.groupby("Member"):
        total = grp["Amount"].sum()
        score = max(0, 100 - total/100)  # simple scoring logic
        scores[member] = score
    
    pd.DataFrame(list(scores.items()), columns=["Member","Health_Score"]).to_csv(OUTPUT_FILE, index=False)
    
    # Return the average score or a summary
    avg_score = sum(scores.values()) / len(scores) if scores else 0
    return f"{avg_score:.1f}"  # Return formatted score instead of None
