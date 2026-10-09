import pandas as pd
import numpy as np

from .base import Enricher

from constants import T_ROLE, LINEUP_MAP, SHIFTS_MAP

from typing import Dict, Literal, List, get_args






EVENT_TO_ROLE = {**LINEUP_MAP, **SHIFTS_MAP}   # SHIFTS перекрывает LINEUP, как в оригинале


class RoleEnricher(Enricher):
  
  def before(self, target: pd.DataFrame):
    # target['actor_id'] = target['actor_id'].astype(str)
    # target['other_id'] = target['other_id'].astype(str)
    
    target['actor_role'] = pd.NA
    target['other_role'] = pd.NA

  def per_match(self, target: pd.DataFrame, match_id: str, match_df: pd.DataFrame) -> None:
    # # DEFAULTS
    # roles: Dict[str, T_ROLE] = {}
    

    # # LOGIC
    # for idx, row in match_df.iterrows():

    #   # Отдельно выходы на лед
    #   if row['event_type'] in LINEUP_MAP:
    #     if not pd.isna(row['actor_id']):
    #       roles[row['actor_id']] = LINEUP_MAP[row['event_type']]
    #     if not pd.isna(row['other_id']):
    #       roles[row['other_id']] = LINEUP_MAP[row['event_type']]


    #   # Отдельно смены
    #   if row['event_type'] in SHIFTS_MAP:
    #     if not pd.isna(row['actor_id']):
    #       roles[row['actor_id']] = SHIFTS_MAP[row['event_type']]
    #     if not pd.isna(row['other_id']):
    #       roles[row['other_id']] = SHIFTS_MAP[row['event_type']]
        
      
    #   # Обновляем таргет
    #   if not pd.isna(row['actor_id']) and row['actor_id'] in roles:
    #     target.loc[idx, "actor_role"] = roles[row['actor_id']] 

    #   if not pd.isna(row['other_id']) and row['other_id'] in roles:
    #     target.loc[idx, "other_role"] = roles[row['other_id']]
    # Предварительно: единый маппинг event_type -> role

     # Гарантируем сортировку по seq (stateful-логика зависит от порядка).
    # Если выше по стеку match_df уже отсортирован — эта строка дешёвая no-op.
    roles: Dict = {}

    # --- Сырые массивы из match_df (без Series-оверхеда) ---
    event_types = match_df['event_type'].to_numpy()
    actor_ids   = match_df['actor_id'].to_numpy()
    other_ids   = match_df['other_id'].to_numpy()
    match_index = match_df.index

    # --- Буферы значений ровно для строк текущего матча ---
    n = len(match_df)
    actor_role_vals = np.empty(n, dtype=object)
    other_role_vals = np.empty(n, dtype=object)
    actor_mask = np.zeros(n, dtype=bool)
    other_mask = np.zeros(n, dtype=bool)

    # --- Основной цикл ---
    for i, (et, a, o) in enumerate(zip(event_types, actor_ids, other_ids)):

        role = EVENT_TO_ROLE.get(et)
        if role is not None:
            # NaN != NaN — быстрый чек для float/object
            if a == a:
                roles[a] = role
            if o == o:
                roles[o] = role

        if a == a and a in roles:
            actor_role_vals[i] = roles[a]
            actor_mask[i] = True

        if o == o and o in roles:
            other_role_vals[i] = roles[o]
            other_mask[i] = True

    # --- Одна запись на колонку: только строки текущего матча ---
    if actor_mask.any():
        target.loc[match_index[actor_mask], 'actor_role'] = actor_role_vals[actor_mask]

    if other_mask.any():
        target.loc[match_index[other_mask], 'other_role'] = other_role_vals[other_mask]
        

  def after(self, target: pd.DataFrame):
    pass