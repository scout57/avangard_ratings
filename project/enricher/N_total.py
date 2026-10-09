import pandas as pd
import numpy as np

from typing import Dict, Literal, List, get_args

from .base import Enricher

from constants import T_ROLE, LINEUP_MAP, SHIFTS_MAP, get_args


class NTotalEnricher(Enricher):
  def before(self, target: pd.DataFrame):
    for role in get_args(T_ROLE):
      target['N_' + role] = 1 - target['p_dur_'+ role +'_s'] / target['m_dur_s']
    
    
  def per_match(self, target: pd.DataFrame, match_id: str, match_df: pd.DataFrame) -> None:
    pass
    

  def after(self, target: pd.DataFrame):
    pass

    