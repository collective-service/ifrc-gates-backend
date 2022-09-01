from typing import NamedTuple, Tuple, List

from django.db.models import Avg
from django.db.models.aggregates import StdDev

from apps.data.models import IndicatorData

from .models import ImportUserDataPreview


class OutlierCompareData(NamedTuple):
    mean: float
    std: float


def get_outlier_compare_data_for_indicator_data() -> dict[str, OutlierCompareData]:
    return dict(
        percentage=OutlierCompareData(
            **IndicatorData.objects.aggregate(
                # https://docs.djangoproject.com/en/4.1/ref/models/querysets/#avg
                mean=Avg('indicator_value'),
                # https://docs.djangoproject.com/en/4.1/ref/models/querysets/#stddev
                std=StdDev('indicator_value'),
            )
        )
    )


OUTLIER_COMPARE_DATA_GENERATOR = {
    ImportUserDataPreview: get_outlier_compare_data_for_indicator_data
}


def detect_outliers(
    df,
    model,
    threshold=3,
) -> Tuple[dict, List[int]]:
    def flatten(array):
        return [
            item for sublist in array for item in sublist
        ]
    outlier_col_indices = {}
    list_of_indices = []
    if model in OUTLIER_COMPARE_DATA_GENERATOR:
        columns_meta = OUTLIER_COMPARE_DATA_GENERATOR[model]()
        for col, agg in columns_meta.items():
            df[f"z_score_{col}"] = (df[col] - agg.mean) / (agg.std or 0.1)
        for col in columns_meta.keys():
            outlier_col_indices[col] = set(
                df[
                    (df[f"z_score_{col}"] > threshold) | (df[f"z_score_{col}"] < -threshold)
                ].index
            )
        list_of_indices = list(
            set(
                flatten(
                    list(
                        outlier_col_indices.values()
                    )
                )
            )
        )
        return outlier_col_indices, list_of_indices
    return outlier_col_indices, list_of_indices
