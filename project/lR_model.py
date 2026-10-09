
import os
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression


EVENT_TYPES = (
    "assist_primary", "assist_secondary", "board_battle_lost",
    "board_battle_won", "board_pass_complete", "board_pass_failed",
    "body_hit", "carry", "clear_out_failed", "clear_out_success",
    "clearance", "deke_failed", "deke_success", "duel", "duel_contested",
    "dump_in_failed", "dump_in_success", "dump_misc", "entry_success",
    "error", "exit_controlled", "exit_success", "faceoff", "goal",
    "goal_error", "icing", "infraction", "intercept", "intercept_failed",
    "key_pass_complete", "key_pass_failed", "offside", "pass_complete",
    "pass_failed", "penalty_return", "receive_failed", "scoring_chance",
    "shot_blocked", "shot_missed", "shot_on_target", "steal",
    "stick_check", "turnover",
)


def enrich_stats(events: pd.DataFrame) -> pd.DataFrame:
    events = events[["match_id", "seq", "event_type", "actor_id", "actor_team_id"]].copy()
    events = events.dropna(subset=["match_id", "event_type"])

    # роль берём по первому событию смены actor_id в матче
    shifts = events.loc[events["event_type"].str.startswith("shift_", na=False)]
    shifts = shifts.dropna(subset=["actor_id"])
    shifts = shifts.sort_values(["match_id", "seq"], kind="stable")
    role_map = shifts.drop_duplicates(["match_id", "actor_id"])[["match_id", "actor_id", "event_type"]].copy()
    role_map["role"] = role_map["event_type"].str[6]
    role_map = role_map.drop(columns="event_type")

    # определяем исход по голам в событиях
    team_ids = events.dropna(subset=["actor_team_id"])
    team_ids = team_ids[["match_id", "actor_team_id"]].drop_duplicates()
    
    goal_counts = events.loc[
        events["event_type"].eq("goal") & events["actor_team_id"].notna(),
        ["match_id", "actor_team_id"],
    ]
    goal_counts = goal_counts.groupby(["match_id", "actor_team_id"])
    goal_counts = goal_counts.size().rename("goals")
    
    teams = team_ids.join(goal_counts, on=["match_id", "actor_team_id"])
    teams["goals"] = teams["goals"].fillna(0).astype(int)
    window = teams.groupby("match_id")["actor_team_id"].transform("size").eq(2)
    teams = teams.loc[window]
    teams["max_goals"] = teams.groupby("match_id")["goals"].transform("max")
    teams["min_goals"] = teams.groupby("match_id")["goals"].transform("min")
    teams = teams.loc[teams["max_goals"].ne(teams["min_goals"])].copy()
    teams["win"] = teams["goals"].eq(teams["max_goals"]).astype(int)

    action_counts = events.loc[
        events["event_type"].isin(EVENT_TYPES)
        & events["actor_id"].notna()
        & events["actor_team_id"].notna(),
        ["match_id", "actor_id", "actor_team_id", "event_type"],
    ]
    action_counts = action_counts.groupby(
        ["match_id", "actor_id", "actor_team_id", "event_type"],
        observed=True,
    )
    action_counts = action_counts.size()
    action_counts = action_counts.unstack("event_type", fill_value=0)
    action_counts = action_counts.reindex(columns=EVENT_TYPES, fill_value=0)
    
    win = teams[["match_id", "actor_team_id", "win"]]
    
    player_match = action_counts.reset_index()
    player_match = player_match.merge(role_map, on=["match_id", "actor_id"], how="inner")
    player_match = player_match.merge(win, on=["match_id", "actor_team_id"], how="inner")
    
    return player_match.loc[player_match["role"].isin(["F", "D"])].copy()


def train_weights(player_match: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """Вытащить параметры логистической регрессии"""
    weights: Dict[str, pd.DataFrame] = {}
    
    for role in ("F", "D"):
        frame = player_match.loc[player_match["role"].eq(role)]
        counts = frame.loc[:, list(EVENT_TYPES)]
        active = counts.sum(axis=1).between(30, 270)
        
        X = counts.loc[active]
        y = frame.loc[active, "win"]
        
        model = LogisticRegression(
            max_iter=5000, C=10, solver="liblinear",
            class_weight="balanced", random_state=42,
        )
        model.fit(X, y)
        coefficients = model.coef_[0]

        weights[role] = pd.DataFrame({"event_type": EVENT_TYPES,"weight": coefficients})
        weights[role] = weights[role].sort_values("event_type", kind="stable")
        weights[role] = weights[role].reset_index(drop=True)
        print(f"out/weights_{role}.csv: {len(frame)} игроко-матчей, но учтено {len(X)} после фильтра активности")
    
    return weights




def train_and_export(events: pd.DataFrame) -> dict[str, pd.DataFrame]:
    player_match = enrich_stats(events)
    weights = train_weights(player_match)
    
    prefix = 'out'
    os.makedirs(prefix, exist_ok=True)

    for role in ("F", "D"):
        weights[role].to_csv(f"{prefix}/weights_{role}.csv", index=False)