import pandas as pd
import numpy as np

from .base import Enricher


class XGFeaturesEnricher(Enricher):
  def before(self, target: pd.DataFrame):
    for col in ("x", "y", "x2", "y2", "net_x", "net_y"):
      target[col] = pd.to_numeric(target[col], errors="coerce")

    target["dist_to_net"] = np.sqrt(
        (target["x"] - target["net_x"]) ** 2 + (target["y"] - target["net_y"]) ** 2
    )
    target["angle_to_net"] = np.arctan2(
        target["y"] - target["net_y"], target["x"] - target["net_x"]
    )


    target["event_type_code"] = target["event_type"].astype("category").cat.codes
    target["zone_code"] = target["zone"].astype("category").cat.codes
    

  def per_match(self, target: pd.DataFrame, match_id: str, match_df: pd.DataFrame) -> None:
    pass
  
  def after(self, target: pd.DataFrame):
    pass


    