import pandas as pd
import numpy as np

from typing import Dict, Literal, List, get_args

from .base import Enricher


class RTotalEnricher(Enricher):
  def before(self, target: pd.DataFrame):
    target["match_seq"] = target["match_id"].rank(method="dense").astype(int)
    target["player_seq"] = target.groupby("player_id")["match_seq"].transform("min")
    target["R"] = target["match_seq"] - target["player_seq"] + 1
    
  def per_match(self, target: pd.DataFrame, match_id: str, match_df: pd.DataFrame) -> None:
    pass
    
  def after(self, target: pd.DataFrame):
    pass


    