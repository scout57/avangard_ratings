import pandas as pd

from .base import Enricher


from typing import Dict, Literal, List, get_args


from constants import T_ROLE, LINEUP_MAP, SHIFTS_MAP




class RoleDurationEnricher(Enricher):
  
  def before(self, target: pd.DataFrame):
    
    def key(role: str) -> str:
      return 'p_dur_' + role + '_s'
    
    for role in get_args(T_ROLE):
      target[key(role)] = 0.0 # default value

  def per_match(self, target: pd.DataFrame, match_id: str, match_df: pd.DataFrame) -> None:

    def key(role: str) -> str:
      return 'p_dur_' + role + '_s'

    # DEFAULTS
    toi: Dict[T_ROLE, Dict[str, float]] = {}
    shifts_opens_at: Dict[T_ROLE, Dict[str, float]] = {}

    for role in get_args(T_ROLE):
      toi[role] = {}
      shifts_opens_at[role] = {}

    # LOGIC
    for row in match_df.itertuples(index=False):

      # Отдельно выходы на лед
      if row.event_type in LINEUP_MAP:
        role = LINEUP_MAP[row.event_type]
      
        # Если заполнен actor_id и еще не открыта смена, то зафиксировать
        if row.actor_id and not row.actor_id in shifts_opens_at[role]:
          shifts_opens_at[role][row.actor_id] = row.clock_match


      # Отдельно смены
      if row.event_type in SHIFTS_MAP:
        role = SHIFTS_MAP[row.event_type]

        # Если заполнен actor_id и еще не открыта смена, то зафиксировать
        if row.actor_id and not row.actor_id in shifts_opens_at[role]:
          shifts_opens_at[role][row.actor_id] = row.clock_match

        
        # Если заполнен other_id, то накопить TOI
        if row.other_id:

          # Если открыта смена
          if row.other_id in shifts_opens_at[role]:
            dur = row.clock_match - shifts_opens_at[role][row.other_id]

            if not row.other_id in toi[role]:
              toi[role][row.other_id] = dur
            else:
              toi[role][row.other_id] = toi[role][row.other_id] + dur
            
            del shifts_opens_at[role][row.other_id]


    # AFTER MATCH
    # авто-закрытие тех, кто до конца сидел
    dur_match = match_df.iloc[-1]['clock_match']
    for role in get_args(T_ROLE):
      
      for player_id in shifts_opens_at[role]:
        dur = dur_match - shifts_opens_at[role][player_id]

        if not player_id in toi[role]:
          toi[role][player_id] = dur
        else:
          toi[role][player_id] = toi[role][player_id] + dur

    # UPDATE DATASET
    for role in get_args(T_ROLE):
      for player_id in toi[role]:
        target.loc[(target["match_id"] == match_id) & (target["player_id"] == player_id), key(role)] = toi[role][player_id]

  def after(self, target: pd.DataFrame):
    pass