import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from data_loader import DataLoader
from feature_engineer import DefaultFeatureEngineer

def analyze_feature_importance():
    print("Loading data...")
    loader = DataLoader("data")
    match_stats, team_stats, match_tbl, summoner_match = loader.load_match_stats()

    print("Engineering features...")
    engineer = DefaultFeatureEngineer()
    X_full, y = engineer.fit_transform(match_stats, team_stats, summoner_match, match_tbl)
    
    # Start with all features
    current_features = list(X_full.columns)
    results = []

    print(f"\nStarting analysis with {len(current_features)} features.")
    print("Iteratively removing the most important feature...\n")

    iteration = 0
    while len(current_features) >= 2:
        iteration += 1
        X = X_full[current_features]
        
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model (using parameters from model.py)
        model = RandomForestClassifier(
            n_estimators=50,
            max_depth=10,
            min_samples_split=20,
            min_samples_leaf=10,
            random_state=42,
            class_weight='balanced',
            n_jobs=-1
        )
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_val)
        acc = accuracy_score(y_val, y_pred)
        
        # Get feature importances
        importances = pd.DataFrame({
            'feature': current_features,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        # Identify top feature to remove
        top_feature = importances.iloc[0]['feature']
        top_importance = importances.iloc[0]['importance']
        
        print(f"Iter {iteration}: Features={len(current_features)}, Acc={acc:.4f}, Removed='{top_feature}' ({top_importance:.4f})")
        
        # Store result row
        # We want to show the top 5 features for this iteration in the table as requested roughly
        # The user said: "displayed in a table how each iterations wheights looked and the models accuracy"
        # We'll store the top 3 features + importance for concise display, plus accuracy.
        
        top_3 = importances.head(3)
        top_3_str = ", ".join([f"{row['feature']} ({row['importance']:.2f})" for _, row in top_3.iterrows()])
        
        results.append({
            'Iteration': iteration,
            'Num_Features': len(current_features),
            'Accuracy': acc,
            'Removed_Feature': top_feature,
            'Top_3_Importances': top_3_str
        })
        
        # Remove the top feature for next iteration
        current_features.remove(top_feature)

    # Display final table
    results_df = pd.DataFrame(results)
    
    print("\n" + "="*80)
    print("FEATURE ELIMINATION ANALYSIS SUMMARY")
    print("="*80)
    # Adjust column width for display
    pd.set_option('display.max_colwidth', 100)
    pd.set_option('display.width', 1000)
    print(results_df.to_string(index=False))

if __name__ == "__main__":
    analyze_feature_importance()
