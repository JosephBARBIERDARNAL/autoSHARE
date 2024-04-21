import pandas as pd
import numpy as np
import pytest

# module to be tested
from src.data.outliers import OutliersManager


@pytest.fixture
def synthetic_data():
    np.random.seed(0)
    data = pd.DataFrame(
        {
            "normal_dist": np.random.normal(0, 1, 100),
            "extreme_values": np.concatenate(
                [np.random.normal(0, 1, 95), np.random.normal(0, 10, 5)]
            ),
        }
    )
    return data


@pytest.mark.parametrize("threshold_z,expected_outliers_count", [(3, 2), (2, 8)])
def test_find_z_outliers(synthetic_data, threshold_z, expected_outliers_count):
    manager = OutliersManager()
    outliers = manager.find_z_outliers(threshold_z, synthetic_data)
    print(outliers, expected_outliers_count)
    assert (
        len(outliers) == expected_outliers_count
    ), "Incorrect number of outliers identified using Z-score"


@pytest.mark.parametrize("threshold_iqr,expected_outliers_count", [(1.5, 4), (1, 7)])
def test_find_iqr_outliers(synthetic_data, threshold_iqr, expected_outliers_count):
    manager = OutliersManager()
    outliers = manager.find_iqr_outliers(threshold_iqr, synthetic_data)
    assert (
        len(outliers) == expected_outliers_count
    ), "Incorrect number of outliers identified using IQR"


def test_find_outliers_unsupported_method(synthetic_data):
    manager = OutliersManager()
    with pytest.raises(ValueError) as e:
        manager.find_outliers(threshold=1.5, method="Unsupported", df=synthetic_data)
    assert (
        str(e.value) == "Method not supported."
    ), "Unsupported method error not raised as expected"
