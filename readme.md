# Локальный запуск

> Проверено на Linux

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

## Вариант 3 - Свои интерпретаторы
1. Зайти в папку `project`
2. Установить зависимости: `. install.sh`
3. (Точка входа 1) Запустить jupyter: `. jupyter.sh` и прогнать `main.ipynb`
4. (Точка входа 2) Выполнить основной скрипт: `python -m main`

-----

# Результаты
Успешные вывод программы будет в папке ``project/out``

|Путь|Источник|Что это|
|:---|:---|:---|
|project/out/plot_1.png|test-датасет|Лидерборд по test-датасету| 
|project/out/test_events.csv|test-датасет|Обогащенная таблица events| 
|project/out/test_stats.csv|test-датасет|Статистика по каждому матчу| 
|project/out/test_ratings.csv|test-датасет|Статистика по каждому игроку| 
|project/out/train_events.csv|train-датасет|Обогащенная таблица events| 
|project/out/train_stats.csv|train-датасет|Статистика по каждому матчу| 
|project/out/weights_D.csv|train-датасет|Веса W для защитника| 
|project/out/weights_F.csv|train-датасет|Веса W для нападающего|

