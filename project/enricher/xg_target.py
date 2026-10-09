import pandas as pd
import numpy as np

from .base import Enricher

GOAL_HORIZON_S = 10

class XGTargetEnricher(Enricher):
  def before(self, target: pd.DataFrame):
    target['xg_y'] = 0

  def per_match(self, target: pd.DataFrame, match_id: str, match_df: pd.DataFrame) -> None:
    next_goal_at: float = None

    # Перебрать с конца
    for idx, row in match_df[::-1].iterrows():

      # Скип отрицательных значений
      if row['clock_match'] < 0:
        continue

      # Если гол, то зафиксировать
      if row['event_type'] == "goal" and row['clock_match'] >= 0:
        next_goal_at = row['clock_match']
        target.loc[idx, 'xg_y'] = 1
      # Иначе проставляем дистанцию по времени до гола
      elif next_goal_at != None and (next_goal_at - row['clock_match'] <= GOAL_HORIZON_S):
        target.loc[idx, 'xg_y'] = 1

 
  def after(self, target: pd.DataFrame):
    pass

    