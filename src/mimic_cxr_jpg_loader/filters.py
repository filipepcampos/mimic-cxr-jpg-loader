import math
import pandas as pd

class Modifier():
    def __init__(self):
        pass

    def apply(self, labels: pd.DataFrame, **kwargs) -> pd.DataFrame:
        return labels
    
    def __str__(self):
        return "Filter()"
    
class FilterByViewPosition(Modifier):
    def __init__(self, view_position: str):
        self.view_position = view_position

    def apply(self, labels: pd.DataFrame, **kwargs) -> pd.DataFrame:
        return labels[labels["ViewPosition"] == self.view_position]
    
    def __str__(self):
        return f"FilterByViewPosition({self.view_position})"
    
class FilterBySplit(Modifier):
    def __init__(self, split: str):
        self.split = split

    def apply(self, labels: pd.DataFrame, **kwargs) -> pd.DataFrame:
        return labels[labels["split"] == self.split]
    
    def __str__(self):
        return f"FilterBySplit({self.split})"

class BinarizeCondition(Modifier):
    def __init__(self, condition: str):
        self.condition = condition

    def apply(self, labels: pd.DataFrame, **kwargs) -> pd.DataFrame:
        labels[self.condition] = labels[self.condition].map(
            lambda x: 2 if x < 0 or math.isnan(x) else x
        )
        return labels[labels[self.condition] != 2]
    
    