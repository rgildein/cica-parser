import logging
import os
from typing import List

import pandas as pd

logger = logging.getLogger(__name__)


def save_data(file_name: str, data: List[List[str]]) -> None:
    """save data"""
    df = pd.DataFrame(data=data, columns=["okres", "katastralne uzemie", "prve pismeno", "priezvisko", "vlastnik"])
    df.to_csv(file_name, sep=";", index=False, header=(not os.path.isfile(file_name)), mode="a+")
    logger.debug(f"data was saved to {file_name}")
