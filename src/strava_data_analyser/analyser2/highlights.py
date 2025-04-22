from typing import Callable

from pandas import DataFrame


class Highlight:
    def __init__(self, name: str, column_name: str, display_function: Callable[[object], str] = lambda x: str(x), ascending_sort_order: bool = False):
        self.name = name
        self.column_name = column_name
        self.display_function = display_function
        self.ascending_sort_order = ascending_sort_order

    def transform(self, df: DataFrame) -> dict:
        highlight = df.sort_values([self.column_name], ascending=self.ascending_sort_order).iloc[0][list(
            {'id', 'name', 'start_date_local', self.column_name})]
        highlight["highlight"] = self.name
        highlight["value"] = self.display_function(highlight[self.column_name])
        return highlight.to_dict()
