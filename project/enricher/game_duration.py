import pandas as pd

from .base import Enricher


class GameDurationEnricher(Enricher):
  def before(self, target: pd.DataFrame):
    target['m_dur_s'] = 0.0

  def per_match(self, target: pd.DataFrame, match_id: str, match_df: pd.DataFrame) -> None:
    dur = match_df.iloc[-1]['clock_match']
    
    target.loc[target["match_id"] == match_id, 'm_dur_s'] = dur
  
  def after(self, target: pd.DataFrame):
    pass