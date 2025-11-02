import pytest
from dim_reduce import DimensionReducer
pca_test_cases = [
    [[1,2,3],
     [4,5,6],
     [7,8,9]]
]


@pytest.mark.parametrize("data", pca_test_cases)
def test_pca(data):
    reducer = DimensionReducer(output_dim=2)
    result = reducer.pca(data)
    assert result.shape[1] == 2