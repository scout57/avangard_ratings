import pandas as pd
import numpy as np

from typing import Dict, Literal, List, get_args

from .base import Enricher

from constants import T_ROLE


class VTotalEnricher(Enricher):
  def before(self, target: pd.DataFrame):
    for role in get_args(T_ROLE):
      
      V_impact_key = "V_" + role + "_impact"
      V_priv_key = "V_" + role + "_priv"
      V_pub_key = "V_" + role + "_pub"
      A_key = "A_" + role
      N_key = "N_" + role

      target[V_impact_key] = target[A_key] * target[N_key]
      target[V_priv_key] = target.groupby("player_id")[V_impact_key].cumsum()
      target[V_pub_key] = target[V_priv_key] / target["R"]
    
  def per_match(self, target: pd.DataFrame, match_id: str, match_df: pd.DataFrame) -> None:
    pass
    

  def after(self, target: pd.DataFrame):
    pass

    