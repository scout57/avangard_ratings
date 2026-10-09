from matplotlib.axes import Axes
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class Plotter:
  def plot_player_ratings(self,
                          ax: Axes,
                          df: pd.DataFrame, 
                          rating_col,
                          error_low_col='ci_low',
                          error_high_col='ci_high',
                          player_col='player_id',
                          toi_col='total_toi_s',
                          top_n=30,
                          title='Рейтинг игроков'):
      # Копия и сортировка
      data = df.copy()
      data = data.sort_values(rating_col, ascending=False).head(top_n).reset_index(drop=True)
      
      # Расчёт ошибок для errorbar
      if error_low_col in data.columns and error_high_col in data.columns:
          yerr_low = data[rating_col] - data[error_low_col]
          yerr_high = data[error_high_col] - data[rating_col]
          yerr = np.array([yerr_low.values, yerr_high.values])
      else:
          yerr = None
      
      # Размер точек пропорционален времени на льду
      if toi_col in data.columns and data[toi_col].max() > 0:
          sizes = 50 + 400 * (data[toi_col] / data[toi_col].max())
      else:
          sizes = 100
      
      # Цвет по значению рейтинга
      norm = plt.Normalize(data[rating_col].min(), data[rating_col].max())
      colors = plt.cm.RdYlGn(norm(data[rating_col].values))
      
      # Построение
      y_pos = np.arange(len(data))
      ax.errorbar(
          data[rating_col].values,
          y_pos,
          xerr=yerr,
          fmt='o',
          ecolor='gray',
          elinewidth=1.2,
          capsize=3,
          markersize=0,
          alpha=0.6,
          zorder=2
      )
      
      ax.scatter(
          data[rating_col].values,
          y_pos,
          s=sizes,
          c=colors,
          edgecolors='black',
          linewidths=0.6,
          zorder=3
      )
      
      # Подписи
      ax.set_yticks(y_pos)
      ax.set_yticklabels(data[player_col].astype(str))
      ax.invert_yaxis()
      
      ax.set_xlabel(rating_col, fontsize=11)
      ax.set_ylabel('Игрок', fontsize=11)
      ax.set_title(title, fontsize=13, fontweight='bold')
      
      # Средняя линия
      mean_val = data[rating_col].mean()
      ax.axvline(mean_val, color='red', linestyle='--', alpha=0.5,
                label=f'Среднее: {mean_val:.2f}')
      
      # Медиана линия
      median_val = data[rating_col].median()
      ax.axvline(median_val, color='orange', linestyle='--', alpha=0.5,
                label=f'Медиана: {median_val:.2f}')
      
      ax.legend(loc='lower right')
      
      ax.xaxis.grid(alpha=0.3)
      ax.yaxis.grid(alpha=0.3, linestyle="--")
      sns.despine(left=True)
      
      plt.tight_layout()
