import math
from enum import Enum

import pandas as pd


class Modifier:
    def __init__(self):
        pass

    def apply(self, labels: pd.DataFrame, **kwargs) -> pd.DataFrame:
        return labels

    def __str__(self):
        return "Filter()"


class ViewPosition(Enum):  # TODO: Check for all view positions
    AP = "AP"
    PA = "PA"


class FilterByViewPosition(Modifier):
    def __init__(self, view_position: ViewPosition):
        self.view_position = view_position

    def apply(self, labels: pd.DataFrame, **kwargs) -> pd.DataFrame:
        return labels[labels["ViewPosition"] == self.view_position.value]

    def __str__(self):
        return f"FilterByViewPosition({self.view_position})"


class Split(Enum):
    TRAIN = "train"
    VAL = "validate"
    TEST = "test"


class FilterBySplit(Modifier):
    def __init__(self, split: str):
        self.split = split

    def apply(self, labels: pd.DataFrame, **kwargs) -> pd.DataFrame:
        return labels[labels["split"] == self.split.value]

    def __str__(self):
        return f"FilterBySplit({self.split})"


class Pathology(Enum):
    CARDIOMEGALY = "Cardiomegaly"
    CONSOLIDATION = "Consolidation"
    EDEMA = "Edema"
    ENLARGED_CARDIOMEDIASTINUM = "Enlarged Cardiomediastinum"
    FRACTURE = "Fracture"
    LUNG_LESION = "Lung Lesion"
    LUNG_OPACITY = "Lung Opacity"
    NO_FINDING = "No Finding"
    PLEURAL_EFFUSION = "Pleural Effusion"
    PLEURAL_OTHER = "Pleural Other"
    PNEUMONIA = "Pneumonia"
    PNEUMOTHORAX = "Pneumothorax"
    SUPPORT_DEVICES = "Support Devices"


class BinarizePathology(Modifier):
    def __init__(self, condition: str):
        self.condition = condition

    def apply(self, labels: pd.DataFrame, **kwargs) -> pd.DataFrame:
        labels[self.condition] = labels[self.condition].map(
            lambda x: 2 if x < 0 or math.isnan(x) else x
        )
        return labels[labels[self.condition] != 2]
