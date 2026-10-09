import pandas as pd
import numpy as np

from .base import Enricher


class ManpowerEnricher(Enricher):
  ACTOR_KEY = 'actor_team_size'
  OTHER_KEY = 'actor_team_size'
  
  def before(self, target: pd.DataFrame):
    target[self.ACTOR_KEY] = pd.NA
    target[self.OTHER_KEY] = pd.NA

  def per_match(self, target: pd.DataFrame, match_id: str, match_df: pd.DataFrame) -> None:
    pass

  def after(self, target: pd.DataFrame):
    target[self.ACTOR_KEY] = np.where(target['actor_team_id'] == target['home_team_id'], target["n_home"], target["n_away"])
    target[self.OTHER_KEY] = np.where(target['other_team_id'] == target['home_team_id'], target["n_home"], target["n_away"])
    
    target[self.ACTOR_KEY] = target[self.ACTOR_KEY].astype('Int64')
    target[self.OTHER_KEY] = target[self.OTHER_KEY].astype('Int64')
    target['manpower_diff'] = target[self.ACTOR_KEY] - target[self.OTHER_KEY]
    