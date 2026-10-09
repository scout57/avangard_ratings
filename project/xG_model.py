
import logging
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, roc_auc_score
from sklearn.model_selection import GroupKFold
from xgboost import XGBClassifier


logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s | %(levelname)-7s | %(message)s",
	datefmt="%H:%M:%S",
)
log = logging.getLogger("player_value")

FEATURE_COLS = [
    "event_type_code",
    "zone_code",
    "manpower_diff",
    #"manpower_ratio",
    #"score_diff",
    "period",
    "clock_match",
    "x",
    "y",
    "x2",
    "y2",
    "dist_to_net",
    "angle_to_net",
    # "is_home",
]

class xGModel:

  model: XGBClassifier | None = None
  metrics: Dict[str, float] | None = None

  def __init__(self):
    self.n_splits = 5
    self.xgb_params: Dict = {
        "n_estimators": 400,
        "max_depth": 6,
        "learning_rate": 0.05,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "objective": "binary:logistic",
        "eval_metric": "auc",
        "tree_method": "hist",
        "n_jobs": -1,
        "random_state": 42,
    }

  def fit(self, features: pd.DataFrame, target: pd.Series):
    X = features[FEATURE_COLS].fillna(0.0)
    y = target.astype(int).values

    self.model = XGBClassifier(**self.xgb_params)
    self.model = self.model.fit(X, y)

    y_pred = self.predict(features)

    auc = roc_auc_score(y, y_pred) if len(np.unique(y)) > 1 else float("nan")
    mae = mean_absolute_error(y, y_pred)
    log.info("K_h: AUC=%.4f, MAE=%.4f", auc, mae)
    
    return self, self.predict(features)


  def predict(self, features: pd.DataFrame) -> pd.Series:
    if self.model == None:
        raise ValueError("Сначала обучите модель :)")

    X = features[FEATURE_COLS].fillna(0.0)
    y = self.model.predict_proba(X)[:,1]
    
    return pd.Series(y, index=features.index)
  
