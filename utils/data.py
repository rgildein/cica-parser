import logging
import os
from typing import List

import pandas as pd

logger = logging.getLogger(__name__)


def save_data(file_name: str, data: List[List[str]]) -> None:
    """save data"""
    df = pd.DataFrame(data=data, columns=["okres", "katastralne uzemie", "prve pismeno", "priezvisko", "vlastnik"])
    df.to_csv(file_name, sep=";", index=False, header=(not os.path.isfile(file_name)), mode="a+")
    logger.info(f"saved {len(data)} owners")
    logger.debug(f"data was saved to {file_name}")


def load_data(file_name: str) -> pd.DataFrame:
    """load csv data to DataFrame"""
    df = pd.read_csv(file_name, header=0, sep=";")
    logger.info(f"load DataFrame of size {df.size}")
    return df


def join_tables(tables: List[pd.DataFrame]) -> pd.DataFrame:
    """join tables and drop duplicity"""
    df = pd.concat(tables, axis=0)
    df.drop_duplicates(inplace=True)
    return df
