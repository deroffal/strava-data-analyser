from typing import Callable

from pandas import DataFrame


class Highlight:
    def __init__(self, name: str, column_name: str, display_function: Callable[[object], str] = lambda x: str(x), ascending_sort_order: bool = False):
        self.name = name
        self.column_name = column_name
        self.display_function = display_function
        self.ascending_sort_order = ascending_sort_order

    def transform(self, df: DataFrame) -> dict:
        column_name = self.column_name
        ascending = self.ascending_sort_order

        highlight = df.sort_values([column_name], ascending=ascending).iloc[0][['id', 'name', 'start_date_local', column_name]]
        highlight["highlight"] = self.name

        display_function = self.display_function

        highlight["value"] = display_function(highlight[column_name])

        return highlight
