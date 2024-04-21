import mlflow


def set_or_create_experiment(experiment_name: str) -> str:
    """
    The function of creating an experiment in mlflow

    :param experiment_name: name of the experiment

    :return: -> experiment_id
    """

    try:
        experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id
    except:
        experiment_id = mlflow.create_experiment(
            name=experiment_name,
            tags={'transformer': 'valhalla'}
        )
    finally:
        mlflow.set_experiment(experiment_name=experiment_name)

    return experiment_id
