from typing import Dict, List
import pandas as pd
import os

from xG_model import xGModel

from enricher.base import Enricher
from enricher.game_duration import GameDurationEnricher
from enricher.game_win import GameWinEnricher
from enricher.role_duration import RoleDurationEnricher
from enricher.manpower import ManpowerEnricher
from enricher.xg_features import XGFeaturesEnricher
from enricher.xg_target import XGTargetEnricher
from enricher.time_elapsed import TimeElapsedEnricher
from enricher.role import RoleEnricher
from enricher.w_features import WFeaturesEnricher
from enricher.a_total import ATotalEnricher
from enricher.N_total import NTotalEnricher
from enricher.R_total import RTotalEnricher
from enricher.V_total import VTotalEnricher
from enricher.player_match_event_stats import PlayerMatchEventStatsEnricher

import logging
logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s | %(levelname)-7s | %(message)s",
	datefmt="%H:%M:%S",
)
log = logging.getLogger("player_value")


class Pipeline:
    
    def run(self, events: pd.DataFrame, games: pd.DataFrame, model: xGModel = None) -> tuple[xGModel, pd.DataFrame, pd.DataFrame]:
        # Сборка "Events"
        events = events.copy().merge(games, on="match_id", how="left")
        events = events.drop(columns=["n_events", "home_goals", "away_goals", "stage", "rink_type"])
        events_enrichers: List[Enricher] = {
            # Ждет: 		period / clock_s
            # Наполнит: 	clock_match
            TimeElapsedEnricher(),
            
            # Ждет: 		actor_team_id / other_team_id / home_team_id / away_team_id
            # Наполнит: 	actor_team_size / other_team_size / manpower_diff
            ManpowerEnricher(), 

            # Ждет: 		x / y / x2 / y2 / net_x / net_y 
            # Наполнит: 	dist_to_net / angle_to_net / event_type_code / zone_code
            XGFeaturesEnricher(),    

            # Ждет: 		event_type / clock_match
            # Наполнит: 	xg_y
            XGTargetEnricher(), 
        
            # Ждет: 		event_type / actor_id / other_id
            # Наполнит: 	actor_role / other_role
            RoleEnricher(), 
        
            # Ждет: 		event_type / actor_role / other_role
            # Наполнит: 	actor_w / other_w
            WFeaturesEnricher(), 
        }



        # Сборка "Stats"
        stats = events.copy()[["match_id", "actor_id", "actor_team_id"]].drop_duplicates()
        stats = stats.rename(columns={"actor_id": "player_id"}).dropna()
        stats_enricher: List[Enricher] = {
            # Ждет: 		clock_match
            # Наполнит: 	m_dur_s
            GameDurationEnricher(),
            
            # Ждет: 		home_team_id / away_team_id
            # Наполнит: 	is_win
            GameWinEnricher(),

            # Ждет: 		event_type / actor_id / other_id / clock_match 
            # Наполнит: 	p_dur_forward_s / p_dur_defender_s
            RoleDurationEnricher(),
            
            # 
            # Наполнит: count по event_type (120+ столбцов)
            PlayerMatchEventStatsEnricher()
        }

        # Этап 1 - Массовые действия
        for enricher in events_enrichers:
            log.info(f'[1] {enricher.__class__.__name__}')
            enricher.before(events)

        for enricher in stats_enricher:
            log.info(f'[1] {enricher.__class__.__name__}')
            enricher.before(stats)

        i = 0
        for match_id, match_df in events.groupby("match_id"):
            match_df_sorted = match_df.sort_values(by='seq')

            i = i + 1
            if i % 50 == 1:
                log.info(f'[2] - match step - {i-1}')
            
            for enricher in events_enrichers:
                _match_df = events.loc[match_df_sorted.index]
                enricher.per_match(events, match_id, _match_df)

            for enricher in stats_enricher:
                _match_df = events.loc[match_df_sorted.index]
                enricher.per_match(stats, match_id, _match_df)
                
                
        # Этап 3 - Массовые действия
        for enricher in events_enrichers:
            log.info(f'[3] - {enricher.__class__.__name__}')
            enricher.after(events)

        for enricher in stats_enricher:
            log.info(f'[3] - {enricher.__class__.__name__}')
            enricher.after(stats)

        # Дроп мусора - заменили на корректные
        events = events.drop(columns=["n_home","n_away"])
                
        # Этап 4 - Обучить модель, если не передали сверху
        if model == None:
            log.info(f'[4] - model - fit')
            model, U = xGModel().fit(events, events['xg_y'])
            events['U'] = U
        else:
            log.info(f'[4] - model - predict')
            events['U'] = model.predict(events)
            
        # Этап 5 - Подготовка формул в таблице events - расчет A = w * U
        log.info(f'[5] - calc A')
        events['actor_A'] = events['U'] * events['actor_w']
        events['other_A'] = events['U'] * events['other_w']
        
        # Этап 6 - Подготовка формул в таблице stats - расчет A (сумма действий), N (нормирование по TOI), R (индекс устаревания)
        log.info(f'[6] - calc A / N / R - globally')
        ATotalEnricher().before(stats)
        NTotalEnricher().before(stats)
        RTotalEnricher().before(stats)
        
        i = 0
        for match_id, match_df in events.groupby("match_id"):
            match_df_sorted = match_df.sort_values(by='seq')
            i = i + 1
            if i % 50 == 1:
                log.info(f'[6] - calc A / N / R - per_match {i-1}')
            
            ATotalEnricher().per_match(stats, match_id, match_df)
        
        # Этап 7 - Формула - расчет V_impact (за матч), V_priv (аккумуляция), V_pub (аккумуляция со старением)        
        log.info(f'[7] - calc V')
        VTotalEnricher().before(stats)

        return model, events, stats
        