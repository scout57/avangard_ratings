from __future__ import annotations

import argparse
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple, Literal

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, roc_auc_score
from sklearn.model_selection import GroupKFold
from xgboost import XGBClassifier

# ---------------------------------------------------------------------------
# Логирование
# ---------------------------------------------------------------------------

logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s | %(levelname)-7s | %(message)s",
	datefmt="%H:%M:%S",
)
log = logging.getLogger("player_value")


TFileNames = Literal[
	# Load
	"train__events",
	"train__games",
	"train__players",
	"train__player_teams",
	"train__teams",
	"train__ring_geometry",
	"test__games",
	"test__events",
]

class Data:

	df: Dict[TFileNames, pd.DataFrame] = {}

	############################################################################################
	# Public
	############################################################################################

	def load(self) -> None:
		"""Читает все таблицы датасета."""
		dir_train = Path("./source")
		dir_test  = Path("./source/test")


		self.df: Dict[TFileNames, pd.DataFrame] = {
				"train__events":				self._read_file(dir_train / 'events.parquet', False),
				"train__games":					self._read_file(dir_train / 'games.csv'),
				"train__players":				self._read_file(dir_train / 'players.csv'),
				"train__player_teams":		self._read_file(dir_train / 'player_teams.csv'),
				"train__teams":					self._read_file(dir_train / 'teams.csv'),
				"train__ring_geometry":		self._read_file(dir_train / 'rink_geometry.csv'),
				"test__games":					self._read_file(dir_test  / 'games_test.csv'),
				"test__events":					self._read_file(dir_test  / 'events_test.parquet', False),
		}

		for name, df in self.df.items():
				log.debug("Загружено %-15s строк: %d", name, len(df))



	############################################################################################
	# Private
	############################################################################################

	def _read_file(self, path: Path, csv: bool = True) -> pd.DataFrame:
		if path.exists():
			return pd.read_csv(path) if csv else pd.read_parquet(path)
		
		log.warning("Файл не найден: %s", path)
		return pd.DataFrame()
