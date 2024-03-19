"""
This module contains classes for filtering and modifying the labels of the MIMIC-CXR-JPG dataset.
"""

from enum import Enum

import pandas as pd


class Modifier:
    """
    Base class for modifiers.
    """

    def __init__(self):
        pass

    def apply(self, labels: pd.DataFrame) -> pd.DataFrame:
        """
        Applies the modifier to the labels.
        """
        return labels

    def __str__(self):
        return "Filter()"


class ViewPosition(Enum):
    """
    Enum for the X-Ray view position.
    """

    AP = "AP"
    PA = "PA"
    LATERAL = "LATERAL"


class FilterByViewPosition(Modifier):
    """
    Filter the labels based on the X-Ray view position.
    """

    def __init__(self, view_position: ViewPosition):
        self.view_position = view_position

    def apply(self, labels: pd.DataFrame) -> pd.DataFrame:
        return labels[labels["ViewPosition"] == self.view_position.value]

    def __str__(self):
        return f"FilterByViewPosition({self.view_position})"


class Split(Enum):
    """
    Enum for the recommended train/test/val split.
    """

    TRAIN = "train"
    VAL = "validate"
    TEST = "test"


class FilterBySplit(Modifier):
    """
    Filter the labels based on the recommended train/test/val split.
    """

    def __init__(self, split: Split):
        self.split = split

    def apply(self, labels: pd.DataFrame) -> pd.DataFrame:
        return labels[labels["split"] == self.split.value]

    def __str__(self):
        return f"FilterBySplit({self.split})"


class Pathology(Enum):
    """
    Enum for the pathologies.
    """

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
    """
    Binarize the labels of a pathology.
    """

    def __init__(self, pathology: Pathology):
        self.pathology = pathology.value

    def apply(self, labels: pd.DataFrame) -> pd.DataFrame:
        labels[self.pathology] = labels[self.pathology].map(lambda x: 2 if x < 0 else x)
        return labels[labels[self.pathology] != 2]

    def __str__(self):
        return f"BinarizePathology({self.pathology})"
