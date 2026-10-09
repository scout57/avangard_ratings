# Локальный запуск

## Предварительная подготовка
1. Разархивировать датасет в папку `project/source`:
```
project/source/events.parquet
project/source/games.csv
project/source/players.csv
project/source/player_teams.csv
project/source/teams.csv
project/source/rink_geometry.csv
project/source/test/games_test.csv
project/source/test/events_test.parquet
```

## Вариант 1 - Jupyter через docker-compose
1. Скопировать `.env.example` в `.env` (можно изменить порт)
2. Поднять контейнер: `docker compose up -d`
3. Зайти на http://0.0.0.0:7200/tree
4. Запустить **main.ipynb** (тут есть описание ячеек)

## Вариант 2 - One-shot скрипт через Docker
1. Просто выполнить в консоли: `. docker-one-shot.sh`

-----

# Результаты
Успешные вывод программы будет в папке ``project/out``

|Путь|Источник|Что это|
|:---|:---|:---|
|out/plot_1.png|test-датасет|Лидерборд по test-датасету| 
|out/test_events.csv|test-датасет|Обогащенная таблица events| 
|out/test_stats.csv|test-датасет|Статистика по каждому матчу| 
|out/test_ratings.csv|test-датасет|Статистика по каждому игроку| 
|out/train_events.csv|train-датасет|Обогащенная таблица events| 
|out/train_stats.csv|train-датасет|Статистика по каждому матчу| 
|out/weights_D.csv|train-датасет|Веса W для защитника| 
|out/weights_F.csv|train-датасет|Веса W для нападающего|

