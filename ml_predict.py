#ml_predict.py
# ml_predict.py
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

DATA_FILE = "family_expenses_10000.csv"
OUTPUT_FILE = "predicted_expenses.csv"

def predict_next_month(family_id=None):
    df = pd.read_csv(DATA_FILE)
    if family_id:
        df = df[df["Family_ID"]==family_id]
    if df.empty:
        return
    predictions = {}
    for member, grp in df.groupby("Member"):
        grp = grp.sort_values("Date")
        X = np.arange(len(grp)).reshape(-1,1)
        y = grp["Amount"].values
        if len(X) < 2:
            pred = y[-1] if len(y)>0 else 0
        else:
            model = LinearRegression().fit(X, y)
            pred = model.predict([[len(X)]])[0]
        predictions[member] = pred
    pd.DataFrame(list(predictions.items()), columns=["Member","Predicted_Expense"]).to_csv(OUTPUT_FILE, index=False)


