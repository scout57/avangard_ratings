from abc import ABC, abstractmethod
import pandas as pd

class Enricher(ABC):
  
  @abstractmethod
  def before(self, target: pd.DataFrame):
    '''
      Единожды обновляет весь таргет до перебора матчей
    '''
    pass
  
  @abstractmethod
  def per_match(self, target: pd.DataFrame, match_id: str, match_df: pd.DataFrame) -> None:
    '''
      Обогащает target по срезу events.parquet (match_df), т.е. в рамках матча
    '''
    pass
  
  
  
  @abstractmethod
  def after(self, target: pd.DataFrame):
    '''
      Единожды обновляет весь таргет после перебора матчей
    '''
    pass