# setup_demo.py
import auth_app
import data_handler
import visualize
import health_score
import ml_predict

NUM_USERS = 50
FAMILY_COUNT = 5

print("🔹 Step 1: Initializing Database...")
auth_app.init_db()
print("✅ Database Initialized")

print(f"🔹 Step 2: Generating {NUM_USERS} Users across {FAMILY_COUNT} Families...")
auth_app.auto_generate_users(n=NUM_USERS, family_count=FAMILY_COUNT)
print("✅ Users Generated")

print("🔹 Step 3: Generating Expenses for all users...")
data_handler.auto_generate_expenses(family_count=FAMILY_COUNT)
print("✅ Expenses Generated")

print("🔹 Step 4: Generating Charts, Health Scores, and ML Predictions...")
for f in range(1, FAMILY_COUNT + 1):
    family_id = f"fam" + str(f)
    visualize.bar_chart_family(family_id)
    health_score.compute_health_score(family_id)
    ml_predict.predict_next_month(family_id)
print("✅ Charts, Health Scores, and ML Predictions Generated")

print("\n🎉 Setup Complete! You can now run `python app.py` to launch the dashboard.")
