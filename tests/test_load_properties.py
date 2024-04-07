import pytest
import pandas as pd
from pandas.testing import assert_frame_equal

# module to be tested
from src.data import load_data_properties

test_cases = [
    (1, True),
    (2, True),
    (3, True),
    (4, True),
    (5, True),
    (6, True),
    (7, True),
    (8, True),
    (9, True),
    (10, False),
]

@pytest.mark.parametrize("wave, expected_success", test_cases)
def test_load_data_properties(wave, expected_success):
    try:
        properties_df = load_data_properties(wave)
        assert isinstance(properties_df, pd.DataFrame), "Returned object is not a DataFrame"
        if expected_success:
            assert not properties_df.empty, "DataFrame is empty but was expected to have data"
        else:
            pytest.fail("Expected failure for this test case, but it succeeded.")
    except Exception as e:
        if expected_success:
            pytest.fail(f"Expected success for wave {wave}, but it failed with exception: {e}")