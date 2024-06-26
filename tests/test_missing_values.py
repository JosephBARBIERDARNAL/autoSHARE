import pandas as pd
import pytest

# module to be tested
from src.data.missing_values import MissingValuesManager


@pytest.mark.parametrize(
    "input_value,expected_output",
    [
        (
            ["Don't know", "Refusal", "Not applicable"],
            pd.Series([None, None, None], dtype="object"),
        ),
        (["Don't know", "Refusal", 3], pd.Series([None, None, 3], dtype="object")),
        ([1, 2, 3], pd.Series([1, 2, 3], dtype="int64")),
        (["Hello", 2, 3], pd.Series(["Hello", 2, 3], dtype="object")),
    ],
)
def test_replace_missing_codes(input_value, expected_output):
    sample_df = pd.DataFrame({"input": input_value})
    manager = MissingValuesManager()
    modified_df = manager.replace_missing_codes(sample_df)
    pd.testing.assert_series_equal(
        modified_df["input"], expected_output, check_names=False
    )


@pytest.mark.parametrize(
    "input_value,expected_output",
    [
        ([None, None, None], 3),
        ([None, None, 3], 2),
        ([1, 2, 3], 0),
        (["Hello", 2, 3], 0),
    ],
)
def test_make_explicit_na(input_value, expected_output):
    sample_df = pd.DataFrame({"input": input_value})
    manager = MissingValuesManager()
    modified_df = manager.make_explicit_na(sample_df)
    assert (modified_df["input"] == "missing").sum() == expected_output


test_cases = [
    (pd.DataFrame({"A": [1, 2, 3, 4], "B": [None, None, None, None]}), 0, ["B"]),
    (pd.DataFrame({"A": [1, None, 3, 4], "B": [None, 2, None, 4]}), 30, ["B"]),
    (
        pd.DataFrame({"A": [1, None, 3, None], "B": [None, 2, None, 4]}),
        40,
        ["A", "B"],
    ),
]


@pytest.mark.parametrize("df,threshold,expected", test_cases)
def test_count_percent_na_columns(df, threshold, expected):
    manager = MissingValuesManager()
    cols_to_remove = manager.remove_na_columns(df, threshold)
    assert sorted(cols_to_remove) == sorted(
        expected
    ), f"Expected {expected} but got {cols_to_remove}"
