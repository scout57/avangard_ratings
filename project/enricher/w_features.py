import pandas as pd
import numpy as np
import os

from typing import Dict, Literal, List, get_args

from .base import Enricher

from constants import T_ROLE


import logging
logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s | %(levelname)-7s | %(message)s",
	datefmt="%H:%M:%S",
)
log = logging.getLogger("player_value")

class WFeaturesEnricher(Enricher):
  coef: Dict[T_ROLE, Dict[str, float]] = {}
  
  def __init__(self):
    self.coef = {}
    
    if not os.path.exists("out/weights_F.csv") or not os.path.exists("out/weights_D.csv"):
      msg = 'Сначала расчитайте out/weights_*.csv'
      log.error(msg)
      raise ValueError(msg)  
    
    df = pd.read_csv("out/weights_F.csv")
    self.coef['forward'] = dict(zip(df["event_type"], df["weight"].astype(float)))
    
    df = pd.read_csv("out/weights_D.csv")
    self.coef['defender'] = dict(zip(df["event_type"], df["weight"].astype(float)))
  
  def before(self, target: pd.DataFrame):
    # target['actor_w'] = 0.0
    # target['other_w'] = 0.0
    pass

  def per_match(self, target: pd.DataFrame, match_id: str, match_df: pd.DataFrame) -> None:

    # # LOGIC
    # for idx, row in match_df.iterrows():
    #     event_type = row['event_type']
        
    #     if pd.isna(event_type):
    #         continue
        
        
    #     if not pd.isna(row['actor_role']) and row['actor_role'] in self.coef:
    #         if row['event_type'] in self.coef[row['actor_role']]:
    #             target.loc[idx, "actor_w"] = self.coef[row['actor_role']][row['event_type']]
            
    #     if not pd.isna(row['other_role']) and row['other_role'] in self.coef:
    #         if row['event_type'] in self.coef[row['other_role']]:
    #             target.loc[idx, "other_w"] = self.coef[row['other_role']][row['event_type']]
    pass
        
    
  def after(self, target: pd.DataFrame):
    diff = [c for c in ('actor_w', 'other_w') if c in target.columns]
    if diff:
        target.drop(columns=diff, inplace=True)


    flat = pd.DataFrame(
        [(k1, k2, v) for k1, sub in self.coef.items() for k2, v in sub.items()],
        columns=["actor_role", "event_type", "actor_w"],
    )
    
    merged = target.merge(flat, on=["actor_role", "event_type"], how="left")
    target['actor_w'] = pd.to_numeric( merged['actor_w'], errors='coerce')
    
    flat = flat.rename(columns={'actor_role': 'other_role', 'actor_w': 'other_w'})
    merged = target.merge(flat, on=["other_role", "event_type"], how="left")
    target['other_w'] = pd.to_numeric( merged['other_w'], errors='coerce')
    
    
    pass


    