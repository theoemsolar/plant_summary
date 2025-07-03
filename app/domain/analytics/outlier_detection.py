import numpy as np


def detect_outliers(list_of_values: list, factor: float = 0.3) -> list:
    data = [float(item["FieldValue"]) for item in list_of_values]
    q1 = np.quantile(data, 0.25)
    q3 = np.quantile(data, 0.75)
    iqr = q3 - q1
    lower_bound = q1 - factor * iqr

    return [x for x in data if x < lower_bound]
