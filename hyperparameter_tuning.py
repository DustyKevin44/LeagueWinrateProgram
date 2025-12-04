import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, make_scorer
from data_loader import DataLoader
from feature_engineer import DefaultFeatureEngineer
import time

def hyperparameter_tuning():
    """
    Test different combinations of n_estimators and max_depth
    to find the optimal Random Forest configuration.
    """
    
    # Load and prepare data
    print("Loading data...")
    loader = DataLoader("data")
    match_stats, team_stats, match_tbl, summoner_match = loader.load_match_stats()
    
    print("Engineering features...")
    engineer = DefaultFeatureEngineer()
    X, y = engineer.fit_transform(match_stats, team_stats, summoner_match, match_tbl)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}\n")
    
    # Define parameter grid
    param_grid = {
        'n_estimators': [50, 100, 200, 300],
        'max_depth': [5, 10, 15, 20, None],
        'min_samples_split': [20],
        'min_samples_leaf': [10],
        'class_weight': ['balanced'],
        'random_state': [42],
        'n_jobs': [-1]
    }
    
    print("Parameter grid:")
    print(f"  n_estimators: {param_grid['n_estimators']}")
    print(f"  max_depth: {param_grid['max_depth']}")
    print(f"\nTotal combinations: {len(param_grid['n_estimators']) * len(param_grid['max_depth'])}")
    print("=" * 80)
    
    # Create base model
    rf = RandomForestClassifier()
    
    # Perform grid search with cross-validation
    print("\nPerforming Grid Search with 5-fold Cross-Validation...")
    print("This may take several minutes...\n")
    
    grid_search = GridSearchCV(
        estimator=rf,
        param_grid=param_grid,
        cv=5,  # 5-fold cross-validation
        scoring='accuracy',
        verbose=2,
        n_jobs=-1,
        return_train_score=True
    )
    
    start_time = time.time()
    grid_search.fit(X_train, y_train)
    elapsed_time = time.time() - start_time
    
    print(f"\nGrid search completed in {elapsed_time:.2f} seconds")
    print("=" * 80)
    
    # Get results
    results_df = pd.DataFrame(grid_search.cv_results_)
    
    # Sort by test score
    results_df = results_df.sort_values('rank_test_score')
    
    # Display top 10 configurations
    print("\n" + "=" * 80)
    print("TOP 10 CONFIGURATIONS")
    print("=" * 80)
    
    for idx, row in results_df.head(10).iterrows():
        print(f"\nRank {int(row['rank_test_score'])}:")
        print(f"  n_estimators: {row['param_n_estimators']}")
        print(f"  max_depth: {row['param_max_depth']}")
        print(f"  Mean CV Accuracy: {row['mean_test_score']:.4f} (+/- {row['std_test_score']:.4f})")
        print(f"  Mean Train Accuracy: {row['mean_train_score']:.4f}")
        print(f"  Mean Fit Time: {row['mean_fit_time']:.2f}s")
    
    # Best parameters
    print("\n" + "=" * 80)
    print("BEST CONFIGURATION")
    print("=" * 80)
    print(f"Best parameters: {grid_search.best_params_}")
    print(f"Best CV accuracy: {grid_search.best_score_:.4f}")
    
    # Evaluate on test set
    print("\n" + "=" * 80)
    print("TEST SET EVALUATION")
    print("=" * 80)
    
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Test Accuracy: {test_accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Feature importances
    feature_names = X.columns if hasattr(X, 'columns') else [f'feature_{i}' for i in range(X.shape[1])]
    importances = pd.DataFrame({
        'feature': feature_names,
        'importance': best_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nFeature Importances (Best Model):")
    for _, row in importances.iterrows():
        print(f"  {row['feature']:20s}: {row['importance']:.4f}")
    
    # Comparison with current model
    print("\n" + "=" * 80)
    print("COMPARISON WITH CURRENT MODEL")
    print("=" * 80)
    print("Current model parameters:")
    print("  n_estimators: 100")
    print("  max_depth: 10")
    
    # Train current model for comparison
    current_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=20,
        min_samples_leaf=10,
        random_state=42,
        class_weight='balanced',
        n_jobs=-1
    )
    current_model.fit(X_train, y_train)
    y_pred_current = current_model.predict(X_test)
    current_accuracy = accuracy_score(y_test, y_pred_current)
    
    print(f"\nCurrent model test accuracy: {current_accuracy:.4f}")
    print(f"Best model test accuracy: {test_accuracy:.4f}")
    print(f"Improvement: {(test_accuracy - current_accuracy)*100:.2f}%")
    
    # Save detailed results
    results_file = "data/hyperparameter_tuning_results.csv"
    results_df[['param_n_estimators', 'param_max_depth', 'mean_test_score', 
                'std_test_score', 'mean_train_score', 'mean_fit_time']].to_csv(
        results_file, index=False
    )
    print(f"\nDetailed results saved to: {results_file}")
    
    # Recommendations
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    
    best_n_est = grid_search.best_params_['n_estimators']
    best_depth = grid_search.best_params_['max_depth']
    
    print(f"\nUpdate model.py line 35-36 to:")
    print(f"  n_estimators={best_n_est},")
    print(f"  max_depth={best_depth},")
    
    if test_accuracy > current_accuracy:
        print(f"\n[+] This will improve accuracy by {(test_accuracy - current_accuracy)*100:.2f}%")
    else:
        print(f"\n[-] Current configuration is already optimal or very close.")
    
    return grid_search.best_params_, test_accuracy

if __name__ == "__main__":
    best_params, accuracy = hyperparameter_tuning()
