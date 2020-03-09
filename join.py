import os
from datetime import datetime

import click

from utils.data import load_data, join_tables


@click.command()
@click.option("--path", "-p", type=click.Path(exists=True), default=os.getcwd())
def join(path: str):
    """join all csv to one"""
    tables = [load_data(file) for file in os.listdir(path) if file.endswith(".csv") and file.startswith("cica-")]
    df = join_tables(tables)
    df.to_csv(f"result-cica-{datetime.now():%Y%m%d-%H%M}.csv", index=False, sep=";")


if __name__ == "__main__":
    join()
