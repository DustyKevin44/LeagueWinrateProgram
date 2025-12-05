pyth# analyze_rank_importances_all.py

import os
import pandas as pd
from data_loader import DataLoader
from feature_engineer import DefaultFeatureEngineer
from model import RandomForestWinModel, MODEL_PATH

RANK_MAP = {
    'iron': 1,
    'bronze': 2,
    'silver': 3,
    'gold': 4,
    'platinum': 5,
    'emerald': 6,
    'diamond': 7,
    'master': 8,
    'grandmaster': 9,
    'challenger': 10
}

def analyze_ranks(include_unranked=True):
    all_feature_importances = {}
    all_datasets = {}

    ranks_to_process = list(RANK_MAP.keys())
    if include_unranked:
        ranks_to_process.append("unranked")

    for rank in ranks_to_process:
        print(f"\n=== Processing Rank: {rank.upper()} ===")
        try:
            loader = DataLoader("data")

            if rank == "unranked":
                # all ranks combined
                match_stats, team_stats, match_tbl, summoner_match = loader.load_match_stats(rank_ids=None)
                rank_label = "All"
            else:
                rank_id = RANK_MAP[rank]
                min_rank = max(1, rank_id - 1)
                max_rank = min(10, rank_id + 1)
                rank_ids = list(range(min_rank, max_rank + 1))
                match_stats, team_stats, match_tbl, summoner_match = loader.load_match_stats(rank_ids=rank_ids)
                rank_label = rank.capitalize()

            # Save dataset info
            all_datasets[rank_label] = {
                'match_count': len(match_stats),
                'team_count': len(team_stats),
                'dataframe': match_stats  # store for later rank counts
            }

            if len(match_stats) < 50:
                print("Not enough data for this rank, skipping feature importance.")
                continue

            # Feature engineering
            engineer = DefaultFeatureEngineer()
            X, y = engineer.fit_transform(match_stats, team_stats, summoner_match, match_tbl)

            # Train model for feature importance
            model = RandomForestWinModel(MODEL_PATH)
            model.train(X, y)

            feature_names = X.columns if hasattr(X, 'columns') else [f'feature_{i}' for i in range(X.shape[1])]
            importances = dict(zip(feature_names, model.model.feature_importances_))
            all_feature_importances[rank_label] = importances

        except Exception as e:
            print(f"Error processing {rank}: {e}")

    return all_feature_importances, all_datasets

def main():
    feature_importances, datasets = analyze_ranks(include_unranked=True)

    # Convert to DataFrame: features as rows, ranks as columns
    fi_df = pd.DataFrame(feature_importances).fillna(0)
    # Sort rows by 'All' importance descending
    fi_df = fi_df.sort_values(by='All', ascending=False)

    # Save CSVs
    fi_df.to_csv("feature_importances_per_rank_sorted.csv")
    fi_df.to_csv("feature_importances_per_rank.csv")
    print("Feature importances saved to CSV.")

    # Dataset summary
    ds_summary = {}
    for rank_label, data_info in datasets.items():
        df = data_info['dataframe']
        if rank_label != "All":
            ds_summary[rank_label] = len(df)
    # Add all ranks
    ds_summary['All'] = len(datasets['All']['dataframe'])

    # Pretty print feature importances
    print("\n=== Feature Importances Table ===")
    fi_df_sorted = fi_df.sort_values(by='All', ascending=False)
    print(fi_df_sorted.round(4).to_string())

    # Pretty print dataset sizes
    print("\n=== Dataset Sizes by Rank ===")
    for rank, count in ds_summary.items():
        print(f"{rank:12s}: {count}")

if __name__ == "__main__":
    main()
