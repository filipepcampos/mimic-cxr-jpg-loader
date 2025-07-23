"""
This module contains the MIMIC_Dataset class, which is used to load the dataset.
"""

from pathlib import Path
from typing import List, Optional

import pandas as pd
from PIL import Image

from mimic_cxr_jpg_loader.modifiers import Modifier, Pathology


class MIMICDataset:
    """
    Dataset class for MIMIC-CXR-JPG dataset.
    Each datum is a tuple of an image and a pandas Series containing the labels.
    """

    def __init__(
        self,
        root: str,
        split_path: str,
        modifiers: Optional[List[Modifier]] = None,
        target_pathology: Optional[Pathology] = None,
    ):
        self.root = Path(root)
        self.split_path = Path(split_path)
        self.target_pathology = str(target_pathology) if target_pathology else None

        labels = self.get_labels()

        labels = labels.set_index("dicom_id")

        if modifiers:
            for modifier in modifiers:
                labels = modifier.apply(labels)

        labels["Path"] = labels.apply(self.get_path, axis=1)

        self.labels = labels

    def get_labels(self) -> pd.DataFrame:
        """
        Retrieves the labels from the metadata and chexpert csv files and merges them.
        """
        metadata_labels = pd.read_csv(self.root / "mimic-cxr-2.0.0-metadata.csv")
        chexpert_labels = pd.read_csv(
            self.root / "mimic-cxr-2.0.0-chexpert.csv",
            index_col=["subject_id", "study_id"],
        )
        splits = pd.read_csv(self.split_path)
        labels = metadata_labels.merge(
            chexpert_labels,
            on="study_id",
            how="left",
        ).dropna(subset=["subject_id"])
        labels = labels.merge(
            splits,
            on="dicom_id",
            suffixes=("", "_right"),
            how="left",
        )
        return labels

    def get_path(self, row: pd.Series):
        """
        Returns the path of the image file corresponding to the row.
        """
        dicom_id = str(row.name)
        subject = "p" + str(int(row["subject_id"]))
        study = "s" + str(int(row["study_id"]))
        image_file = dicom_id + ".jpg"
        return self.root / "files" / subject[:3] / subject / study / image_file

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        row = self.labels.iloc[idx]
        img = Image.open(row["Path"]).convert("RGB")

        if self.target_pathology:
            return (img, row[self.target_pathology])
        return (img, row)
