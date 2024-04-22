## About

Данный проект представляет собой pet-проект, предназначенный для изучения и применения NLP (Natural Language Processing) моделей в сочетании с такими инструментами, как MLflow, Airflow и Docker. В основе проекта лежит использование готового pipeline от Hugging Face (valhalla/distilbart-mnli-12-1), позволяющего классифицировать crypto-новости по заданным категориям.

## Workflow
Процесс работы с данными в проекте разделён на несколько этапов:
### Сбор данных
load_data.py: Новостные данные в формате RSS с криптовалютных сайтов собираются и загружаются. Возможно использование нескольких источников. Данные сохраняются в data/raw
### Обработка и Классификация
model_prediction.py: Определяются произвольные категории (LABELS), по которым будут классифицироваться новости, и проводится zero-shot classification. Данные сохраняются в файл data/predict
### Вывод результата
Aggreration.py: Данные отбираются в дневном диапазоне (новости старше 1 дня в result не попадают). Данные сохраняются в data/results.

## Airflow:
classificator.py: Автоматический процесс (DAG) управляется через Airflow и включает в себя следующие задачи для оркестрации:
- load_data -> model_prediction -> result_topic, где каждый шаг осуществляется с помощью DockerOperator, а финальный шаг использует PythonOperator. 
<img src="https://i.ibb.co/xzHSsDD/1.png" width="726">

## MLflow
- Задача model_prediction включает исполнение кода в MLflow для создания эксперимента (experiment) и запуска регистрации (run).
- Каждый run регистрируется в модели Crypto_news с сопутствующими метриками и предсказаниями для заданных категорий (LABELS) вместе с реализацией signature данных.
<img src="https://i.ibb.co/J2yZCD7/2.png" width="726">

## Результаты
После выполнения задачи result_topic создается json файл в data/results: 

<img src="https://i.ibb.co/k47rXrr/3.png" width="726">

## Documentation
Настройка:
1. Установите виртуальное окружение и активируйте его
2. Установите mlflow: pip install mlflow
3. Поменяйте путь к mounts source в файле classificator.py на абсолютный путь до вашей папки data
4. При необходимости поменяйте mlflow.set_tracking_uri в файле model_prediction.py

Запуск:
1. Запустите mlflow ui
2. Запустите docker compose up airflow-init
3. Запустите docker compose up --build

Доступ к airflow предоставляется по адресу http://localhost:8080 к mlflow http://localhost:5000
