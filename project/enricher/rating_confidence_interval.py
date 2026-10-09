"""Поматчевые bootstrap-интервалы для итоговых рейтингов игроков."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .base import Enricher


class RatingConfidenceIntervalEnricher(Enricher):
    """Оценка разброса итогового рейтинга при помощи бутстрэпа"""

    def __init__(
        self,
        match_stats: pd.DataFrame | str | Path,
    ) -> None:
        self.match_stats = (
            match_stats if isinstance(match_stats, pd.DataFrame)
            else pd.read_csv(match_stats)
        )
        self.confidence = 0.95
        self.n_bootstrap = 2000
        self.min_matches = 3
        self.random_state = 42

    def before(self,target: pd.DataFrame) -> None:
        total_col = 'rating_total'
        rating_cols = ("V_forward_pub", "V_defender_pub", total_col)

        output_cols = tuple(
            f"{rating}_{bound}"
            for rating in rating_cols
            for bound in ("ci_low", "ci_high")
        )
        for column in output_cols:
            target[column] = np.nan

        stats_by_player = self.match_stats.groupby("player_id", sort=False)
        rng = np.random.default_rng(self.random_state)
        alpha = (1 - self.confidence) / 2

        for idx, rating in target.iterrows():
            player_id = rating["player_id"]
            if player_id not in stats_by_player.groups:
                continue
            matches = stats_by_player.get_group(player_id).sort_values("match_seq")
            if len(matches) < self.min_matches:
                continue

            impacts = matches[["V_forward_impact", "V_defender_impact"]].to_numpy(dtype=float)
            last_r = float(matches["R"].iloc[-1])
            if not np.isfinite(impacts).all() or not np.isfinite(last_r) or last_r <= 0:
                continue

            published = pd.to_numeric(
                rating[["V_forward_pub", "V_defender_pub"]], errors="coerce"
            ).to_numpy(dtype=float)

            sample_idx = rng.integers(0, len(matches), size=(self.n_bootstrap, len(matches)))
            sampled_rating = impacts[sample_idx].sum(axis=1) / last_r
            role_bounds = np.quantile(sampled_rating, [alpha, 1 - alpha], axis=0)
            for role_idx, column in enumerate(rating_cols[:2]):
                target.at[idx, f"{column}_ci_low"] = min(role_bounds[0, role_idx], published[role_idx])
                target.at[idx, f"{column}_ci_high"] = max(role_bounds[1, role_idx], published[role_idx])

            forward_toi = float(rating["p_dur_forward_s"])
            defender_toi = float(rating["p_dur_defender_s"])
            total_toi = forward_toi + defender_toi
            if total_toi <= 0 or pd.isna(rating[total_col]):
                continue
            forward_share = forward_toi / total_toi
            defender_share = defender_toi / total_toi
            published_total = float(rating[total_col])
            sampled_total = sampled_rating[:, 0] * forward_share + sampled_rating[:, 1] * defender_share
            low, high = np.quantile(sampled_total, [alpha, 1 - alpha])
            target.at[idx, f"{total_col}_ci_low"] = min(low, published_total)
            target.at[idx, f"{total_col}_ci_high"] = max(high, published_total)

    def per_match(
        self, target: pd.DataFrame, match_id: str, match_df: pd.DataFrame
    ) -> None:
        pass

    def after(self, target: pd.DataFrame):
        pass