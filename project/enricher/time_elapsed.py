import pandas as pd

from .base import Enricher


class TimeElapsedEnricher(Enricher):
  
  def before(self, target: pd.DataFrame):
    target['clock_match'] = (target["period"].astype(float) - 1) * 1200.0 + target["clock_s"].astype(float)


  def per_match(self, target: pd.DataFrame, match_id: str, match_df: pd.DataFrame) -> None:
    pass
  

  def after(self, target: pd.DataFrame):
    pass
  