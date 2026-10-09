import pandas as pd

from .base import Enricher


class GameWinEnricher(Enricher):
  def before(self, target: pd.DataFrame):
    target['is_win'] = 0.0

  def per_match(self, target: pd.DataFrame, match_id: str, match_df: pd.DataFrame) -> None:
    score_home = 0
    score_away = 0
    
    home_team_id = None
    away_team_id = None
    
    
    for row in match_df.itertuples(index=False):
      if pd.isna(row.event_type):
        continue
      
      if row.event_type != 'goal':
        continue
      
      if row.actor_team_id == row.home_team_id:
        score_home = score_home + 1
      else:
        score_away = score_away + 1
        
      if home_team_id is None and not pd.isna(row.home_team_id):
        home_team_id = row.home_team_id
        
      if away_team_id is None and not pd.isna(row.away_team_id):
        away_team_id = row.away_team_id

    target.loc[(target["match_id"] == match_id) & (target["actor_team_id"] == home_team_id), 'is_win'] = 1 if score_home >= score_away else 0
    target.loc[(target["match_id"] == match_id) & (target["actor_team_id"] == away_team_id), 'is_win'] = 1 if score_away >= score_home else 0
    
    
  def after(self, target: pd.DataFrame):
    pass