import pandas as pd
from forge import run_forge
from shield import load_data, train_model, save_model

BASE_DATA   = "data/network_data.csv"
FORGE_DATA  = "data/forge_attacks.csv"
MERGED_DATA = "data/merged_training.csv"

def self_learning_cycle(iterations=3):

    print("\n⟷ SELF-LEARNING LOOP STARTING")
    print("================================")

    current_data = BASE_DATA   # ✅ use local variable (NO global issues)

    for i in range(iterations):
        print(f"\n🔁 Cycle {i+1}/{iterations}")

        # Step 1: Generate attacks
        print("  [FORGE] Simulating attacks...")
        run_forge()

        # Step 2: Merge datasets
        base_df  = pd.read_csv(current_data)
        forge_df = pd.read_csv(FORGE_DATA)

        merged = pd.concat([base_df, forge_df], ignore_index=True)
        merged.to_csv(MERGED_DATA, index=False)

        print(f"  [MERGE] Combined dataset: {len(merged)} rows")

        # Step 3: Train model
        print("  [SHIELD] Retraining AI...")
        X, y, _ = load_data(MERGED_DATA)
        model = train_model(X, y)
        save_model(model)

        print("  [SHIELD] Model updated ✅")

        # Update dataset for next cycle
        current_data = MERGED_DATA

    print("\n🏆 Self-learning complete! SHIELD is now smarter.")


if __name__ == "__main__":
    self_learning_cycle(iterations=3)
