
from typing import Dict, Literal, List, get_args

T_ROLE = Literal['forward', 'defender']

# Есть только actor_id
LINEUP_MAP: Dict[str, T_ROLE] = {
  # 'lineup_G_1':   'forward',	# Состав: вратарь звена 1
  'lineup_LD_1':  'defender',	# Состав: левый защитник звена 1
  'lineup_LW_1':  'forward',	# Состав: левый крайний звена 1
  'lineup_RD_1':  'defender',	# Состав: правый защитник звена 1
  'lineup_C_1':   'forward',	# Состав: центральный звена 1
  'lineup_RW_1':  'forward',	# Состав: правый крайний звена 1

  # 'lineup_G_2':   'forward',	# Состав: вратарь звена 2
  'lineup_LD_2':  'defender',	# Состав: левый защитник звена 2
  'lineup_RD_2':  'defender',	# Состав: правый защитник звена 2
  'lineup_LW_2':  'forward',	# Состав: левый крайний звена 2
  'lineup_RW_2':  'forward',	# Состав: правый крайний звена 2
  'lineup_C_2':   'forward',	# Состав: центральный звена 2

  # 'lineup_G_3':   'forward',	# Состав: вратарь звена 3
  'lineup_LD_3':  'defender',	# Состав: левый защитник звена 3
  'lineup_RD_3':  'defender',	# Состав: правый защитник звена 3
  'lineup_LW_3':  'forward',	# Состав: левый крайний звена 3
  'lineup_RW_3':  'forward',	# Состав: правый крайний звена 3
  'lineup_C_3':   'forward',	# Состав: центральный звена 3

  # 'lineup_G_4':   'forward',	# Состав: вратарь звена 4
  'lineup_LD_4':  'defender',	# Состав: левый защитник звена 4
  'lineup_LW_4':  'forward',	# Состав: левый крайний звена 4
  'lineup_RD_4':  'defender',	# Состав: правый защитник звена 4
  'lineup_C_4':   'forward',	# Состав: центральный звена 4
  'lineup_RW_4':  'forward',	# Состав: правый крайний звена 4

  'lineup_LD_5':  'defender',	# Состав: левый защитник звена 5
  'lineup_RD_5':  'defender',	# Состав: правый защитник звена 5
  'lineup_LW_5':  'forward',	# Состав: левый крайний звена 5
  'lineup_C_5':   'forward',	# Состав: центральный звена 5
  'lineup_RW_5':  'forward',	# Состав: правый крайний звена 5
}

# Есть либо только actor_id, либо в связке с other_id
SHIFTS_MAP: Dict[str, T_ROLE] = {
  # 'shift_G':    'forward',	# Смена: вратарь
  'shift_D1':   'defender',	# Смена: защитник 1
  'shift_D2':   'defender',	# Смена: защитник 2
  'shift_F1':   'forward',	# Смена: форвард 1
  'shift_F2':   'forward',	# Смена: форвард 2
  'shift_F3':   'forward',	# Смена: форвард 3
}