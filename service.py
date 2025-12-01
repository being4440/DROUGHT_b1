from typing import Dict
import pandas as pd
from d_core import (
    load_clean_df, DataPrep, FeatureEng,
    DroughtThresholds, UserDroughtPred, monthly_cols
)

def predict_drought_for_region(
    csv_path: str,
    region_nm: str,
    user_month_values: Dict[str, float]
) -> Dict:
    """
    user_month_values: e.g. {"JAN": 5.0, "FEB": 10.2, "MAR": 0.0, ...}
    Can be partial; missing months will be filled with mean.
    """
    # 1) Load + region data
    clean_df = load_clean_df(csv_path)
    prep = DataPrep(clean_df)
    region_df = prep.get_region_df(region_nm)

    if region_df.empty:
        raise ValueError(f"Region {region_nm} not found in data")

    # 2) Compute weights + historical weighted df
    weights = prep.compute_weights(region_df)
    fe = FeatureEng(region_df, weights)
    region_weighted_df = fe.prepare_features(region_df)

    # 3) Compute thresholds from history
    thresh = DroughtThresholds(region_weighted_df)
    thresholds_dict = thresh.compute_thresholds()

    # 4) Prepare user input as one-row DataFrame
    row = {}
    for m in monthly_cols:
        row[m] = user_month_values.get(m, None)
    user_df = pd.DataFrame([row])

    user_features = fe.prepare_features(user_df)
    user_weighted_val = float(user_features['weighted_annual'].iloc[0])

    # 5) Classify
    user_pred = UserDroughtPred(thresholds_dict, region_weighted_df)
    label = user_pred.classify(user_weighted_val)
    prob = user_pred.probability(user_weighted_val)

    return {
        "region": region_nm,
        "weighted_annual": user_weighted_val,
        "label": label,
        "Dryness percentile": prob,
        "thresholds": thresholds_dict,
    }