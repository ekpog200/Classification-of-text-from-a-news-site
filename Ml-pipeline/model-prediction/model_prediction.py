import pandas as pd
from transformers import pipeline
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import click
import mlflow
from mlflow.tracking import MlflowClient
from utils import set_or_create_experiment

LABELS = [
    "Bitcoin",
    "Ethereum",
    "Altcoins",
    "NFTs",
    "AI",
    "Other",
]


@click.command()
@click.option("--data_path", help="Path to the input data CSV file")
@click.option("--predictin_path", help="Path to save the output JSON file")
@click.option("--experiment_name", help="Path to save the output JSON file")
@click.option("--run_name", help="Path to save the output JSON file")
@click.option("--model_name", help="Path to save the output JSON file")
def model_prediction(data_path: str, predictin_path: str, experiment_name: str, run_name: str, model_name: str) -> None:
    """
    A function using the pre-trained Transformer valhalla model to output the text belonging to a specific label
     using the zero-shot-classification method

    :param data_path: the path to the input data
    :param predictin_path: the path to the prediction file
    :param experiment_name: The name of the experiment for mlflow
    :param run_name: The name of the run for mlflow
    :param model_name: The name of the model for mlflow

    :return: -> None
    """

    experiment_id = set_or_create_experiment(experiment_name)
    model_ckpt = "valhalla/distilbart-mnli-12-1"
    model = AutoModelForSequenceClassification.from_pretrained(model_ckpt)
    tokenizer = AutoTokenizer.from_pretrained(model_ckpt)
    df = pd.read_csv(data_path, sep="\t")
    text_for_predictions = (df.title + ". " + df.summary).tolist()
    signature = mlflow.models.signature.infer_signature(text_for_predictions, LABELS)

    with mlflow.start_run(run_name=run_name, experiment_id=experiment_id) as run:
        model_hf = pipeline("zero-shot-classification", model=model, tokenizer=tokenizer, device=-1)
        mlflow.transformers.log_model(
            transformers_model=model_hf,
            artifact_path='model',
            signature=signature,
            registered_model_name=model_name
        )
        predictions = model_hf(text_for_predictions, LABELS, multi_label=False)

        # log metrics
        for dic in predictions:
            mlflow.log_metric(f"label_{dic['labels'][0]}", dic['scores'][0])

        # log description
        mlflow.set_tag("mlflow.note.content", 'This is classifier of crypto news')

    # processing the result and writing to a file
    df['label'] = [x["labels"][0] for x in predictions]
    df.T.to_json(predictin_path)


if __name__ == "__main__":
    # mlflow tracking path. For more information check documentation
    mlflow.set_tracking_uri("http://host.docker.internal:5000")
    model_name = 'Crypto_news'

    model_prediction()

    client = MlflowClient()
    MlflowClient().update_registered_model(
        name=model_name,
        description=
        '''
        The model is designed to store the valhalla_prediction experiment. A version is created every time run is run.
        '''
    )
