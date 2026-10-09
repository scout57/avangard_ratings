import pandas as pd
import numpy as np

from typing import Dict, Literal, List, get_args

from .base import Enricher

from constants import T_ROLE, LINEUP_MAP, SHIFTS_MAP, get_args


class ATotalEnricher(Enricher):
  def before(self, target: pd.DataFrame):
    for role in get_args(T_ROLE):
      target['A_' + role] = 0.0

  def per_match(self, target: pd.DataFrame, match_id: str, match_df: pd.DataFrame) -> None:

    A: Dict[T_ROLE,Dict[str, float]] = {}
    
    def A_append(role: T_ROLE, player: str, value: float):
      if not role in A:
        A[role] = {}

      if player in A[role]:
        A[role][player] = A[role][player] + value
      else:
        A[role][player] = value

    # LOGIC
    for idx, row in match_df.iterrows():
      event_type = row['event_type']
      
      if pd.isna(event_type):
          continue
      
      if not pd.isna(row['actor_id']) and not pd.isna(row['actor_role']) and not pd.isna(row['actor_A']):
        A_append(row['actor_role'], row['actor_id'], row['actor_A'])

      if not pd.isna(row['other_id']) and not pd.isna(row['other_role']) and not pd.isna(row['other_A']):
        A_append(row['other_role'], row['other_id'], row['other_A'])
      
    # AFTER CALC
    for role in A:
      for player in A[role]:
        target.loc[(target['player_id'] == player) & (target['match_id'] == match_id), 'A_' + role] = A[role][player]
  
  def after(self, target: pd.DataFrame):
    pass
    


    