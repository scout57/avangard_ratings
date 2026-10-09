from typing import Dict, Tuple

import numpy as np
import pandas as pd

from .base import Enricher

PLAYER_EVENT_TYPES: Tuple[str, ...] = (
  'faceoff',
  'duel',
  'pass_complete',
  'dump_in_failed',
  'turnover',
  'steal',
  'pass_failed',
  'entry_success',
  'shot_blocked',
  'exit_success',
  'body_hit',
  'clear_out_success',
  'dump_in_success',
  'shot_on_target',
  'scoring_chance',
  'icing',
  'infraction',
  'shot_missed',
  'clear_out_failed',
  'exit_controlled',
  'penalty_return',
  'offside',
  'goal',
  'assist_primary',
  'goal_error',
  'intermission',
  'assist_secondary',
  'deke_failed',
  'deke_success',
  'dump_misc',
  'ot_start',
  'fight_end',
  'feed_break',
  'so_attempt',
  'stick_check',
  'receive_failed',
  'rebound',
  'board_pass_failed',
  'intercept',
  'duel_contested',
  'carry',
  'receive',
  'board_pass_complete',
  'clearance',
  'key_pass_failed',
  'intercept_failed',
  'key_pass_complete',
  'board_battle_won',
  'board_battle_lost',
  'rush_1v2',
  'rush_2v2',
  'rush_1v0',
  'rush_1v1',
  'rush_3v2',
  'rush_2v1',
  'rush_2v3',
  'rush_3v3',
  'rush_1v3',
  'rush_3v1',
)
PLAYER_EVENT_TYPE_SET = frozenset(PLAYER_EVENT_TYPES)
STAT_COLUMNS: Tuple[str, ...] = tuple(
  f'{role}_{action}'
  for action in PLAYER_EVENT_TYPES
  for role in ('actor', 'other')
)


class PlayerMatchEventStatsEnricher(Enricher):
  """Итоговые счётчики событий для player_id в одном матче."""

  def before(self, target: pd.DataFrame) -> None:
    for column in STAT_COLUMNS:
      target[column] = np.uint16(0)

  def per_match(self, target: pd.DataFrame, match_id: str, match_df: pd.DataFrame) -> None:
    counts_by_player: Dict[str, Dict[str, int]] = {}

    def add(player_id: str, column: str) -> None:
      if pd.isna(player_id) or player_id == '':
        return
      player_counts = counts_by_player.setdefault(player_id, {})
      count = player_counts.get(column, 0)
      player_counts[column] = count + 1

    for row in match_df.itertuples(index=False):
      action = row.event_type
      if action not in PLAYER_EVENT_TYPE_SET:
        continue

      actor_id = row.actor_id
      other_id = row.other_id
      add(actor_id, f'actor_{action}')
      add(other_id, f'other_{action}')

    match_rows = target.loc[target['match_id'].eq(match_id), 'player_id']
    for idx, player_id in match_rows.items():
      player_counts = counts_by_player.get(player_id)
      if player_counts:
        target.loc[idx, list(player_counts)] = list(player_counts.values())

  def after(self, target: pd.DataFrame):
    pass