import feedparser
import pandas as pd
from html import *
import click
import re
News_url = 'https://rss.app/feeds/hD0LxHykOExeJL4e.xml'
save_colls = ["id", "published", "title", "summary"]


@click.command()
@click.option("--data_path", help="Path to the input data CSV file")
def data_load(data_path: str) -> None:
    news_feed = feedparser.parse(News_url)
    df = pd.DataFrame(news_feed.entries)[save_colls]
    df["published"] = pd.to_datetime(df["published"])
    df["title"] = df["title"].map(unescape)  # Unicode convert HTMLS str
    df["summary"] = df["summary"].apply(lambda x: re.findall(r'>(.*?)<', x)[2:-1])
    df.to_csv(data_path, sep="\t", index=False)


if __name__ == "__main__":
    data_load()
