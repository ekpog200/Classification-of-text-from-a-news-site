import json
from datetime import timedelta, datetime
from collections import defaultdict

timedeltas = timedelta(days=1)
labels = defaultdict(list)


def pred_agr(predictin_path: str, result_path: str) -> None:
    """
    :param predictin_path: the path to the prediction file
    :param result_path: the path to the results file

    :return: -> None

    """

    with open(predictin_path, 'r') as prediction:
        news = json.load(prediction)

    # We check if the received news differs from the current date by 1 day, then it is considered old and we do not
    # include it.
    for i in news.values():
        news_datetime = datetime.strptime(i["published"], "%Y-%m-%d %H:%M:%S")
        if datetime.now() - news_datetime < timedeltas:
            labels[i['label']].append(i['summary'])

    with open(result_path, "w") as f:
        json.dump(labels, f)
