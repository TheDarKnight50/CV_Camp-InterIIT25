import pandas as pd
import os
import config

def get_final_metrics():
    """
    Reads the results.csv file from the validation run and prints the final mAP scores.
    """
    results_path = os.path.join(config.RUNS_DIR, config.DETECTOR_RUN_NAME, 'results.csv')

    if not os.path.exists(results_path):
        print(f"ERROR: results.csv not found at {results_path}")
        return

    # Read the csv file
    df = pd.read_csv(results_path)
    
    # The column names might have leading/trailing spaces, so we strip them
    df.columns = df.columns.str.strip()

    # Get the last row which contains the final metrics
    final_results = df.iloc[-1]

    # Extract the mAP scores
    map50 = final_results['metrics/mAP50(B)']
    map50_95 = final_results['metrics/mAP50-95(B)']

    print("\n--- ✅ Final Model Performance ---")
    print(f"auPRC (mAP@50):   {map50:.4f}")
    print(f"auPRC (mAP@50-95):{map50_95:.4f}")
    print("---------------------------------")


if __name__ == '__main__':
    get_final_metrics()