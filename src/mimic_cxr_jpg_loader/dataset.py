from pathlib import Path
from typing import List

import pandas as pd

from mimic_cxr_jpg_loader.modifiers import Modifier


class MIMIC_Dataset:
    def __init__(self, root: str, split_path: str, modifiers: List[Modifier] = []):
        self.root = Path(root)
        self.split_path = Path(split_path)

        labels = self.get_labels()

        for modifier in modifiers:
            labels = modifier.apply(labels)

        labels["Cardiomegaly"] = labels["Cardiomegaly"].map(
            lambda x: 2 if x < 0  else x
        )

        labels = labels.set_index("dicom_id")
        labels["Path"] = labels.apply(self.get_path, axis=1)
        labels = labels[labels['Cardiomegaly']!=2]

        self.labels = labels

    def get_labels(self) -> pd.DataFrame:
        metadata_labels = pd.read_csv(self.root / "mimic-cxr-2.0.0-metadata.csv")
        chexpert_labels = pd.read_csv(
            self.root / "mimic-cxr-2.0.0-chexpert.csv",
            index_col=["subject_id", "study_id"],
        )
        splits = pd.read_csv(self.split_path)
        labels = metadata_labels.merge(
            chexpert_labels, on="study_id", how="left"
        ).dropna(subset=["subject_id"])
        labels = labels.merge(
            splits, on="dicom_id", suffixes=("", "_right"), how="left"
        )
        return labels

    def get_path(self, row: pd.Series):
        dicom_id = str(row.name)
        subject = "p" + str(int(row["subject_id"]))
        study = "s" + str(int(row["study_id"]))
        image_file = dicom_id + ".jpg"
        return self.root / "files" / subject[:3] / subject / study / image_file

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return self.labels.iloc[idx]
